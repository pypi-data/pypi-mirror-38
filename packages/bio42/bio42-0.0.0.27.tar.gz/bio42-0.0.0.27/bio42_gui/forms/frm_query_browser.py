from itertools import chain
from os import path
from typing import Optional, cast, List
from PyQt5.QtWidgets import QTreeWidget, QGridLayout, QTreeWidgetItem
from bio42 import Application

from mhelper import ArgInspector, ArgValueCollection, Sentinel, SwitchError, ansi_format_helper, file_helper, ignore, io_helper

import re
import editorium as ed
import intermake
import intermake_qt
import mgraph as mg
import neocommand as nc
import mhelper_qt as qt

from bio42_gui.forms.designer import frm_query_browser_designer
from bio42_gui.forms.designer.resources import resources
from bio42_gui.forms.frm_b42_base import AbstractB42SubWindow
from bio42_gui.controller.controller import B42GuiController


CUSTOM_QUERY = Sentinel( "(Custom query)" )
GUI_EP = Sentinel( "(GUI)" )


class GuiEndpoint( nc.MGraphEndpoint ):
    def __init__( self ):
        super().__init__( "GuiEndpoint" )


@Application.INSTANCE.command( visibility = intermake.visibilities.INTERNAL )
def _load_scripts() -> None:
    # Ensure Scripts are loaded
    import bio42_scripts
    ignore( bio42_scripts )


class FrmQueryBrowser( AbstractB42SubWindow ):
    """
    Allows the user to execute and view Cypher queries.
    """
    
    
    def __init__( self, parent: qt.QWidget ):
        """
        CONSTRUCTOR
        """
        super().__init__( parent )
        self.ui = frm_query_browser_designer.Ui_Dialog( self )
        self.setWindowTitle( "Query" )
        self.ui.PAGER_SET.setCurrentIndex( 0 )
        
        # Remove designing styles
        self.ui.FRA_TREE_HOLDER.setStyleSheet( "" )
        self.ui.FRA_BROWSER_HOLDER.setStyleSheet( "" )
        
        # Queries (populated later)
        self.queries = qt.ComboBoxWrapper( self.ui.CMB_QUERY, [] )
        self.queries.enabled = False
        
        # Browser
        self.browser_ctrl = None
        self.browser_page = None
        self.is_browser = False
        
        if B42GuiController.get_settings().enable_browser:
            self.enable_browser()
        
        # Received status
        self.received_html = ""
        self.received_map = { }
        self.received_root = None
        
        # Sent status
        self.editing_script: nc.ScriptCommand = None
        
        # Arguments
        self.editorium = ed.EditoriumGrid( self.ui.LAY_PARAMETERS, self.main_window.controller.editorium )
        self.editorium.fn_arg = self.__editorium_fn_arg
        
        # Signals
        self.ignore_changes = False
        self.ui.CMB_QUERY.currentIndexChanged[int].connect( self.__on_CMB_QUERY_currentIndexChanged )
        self.ui.TXT_CYPHER.textChanged.connect( self.__on_TXT_CYPHER_textChanged )
        
        # Tree view
        lay = QGridLayout()
        self.ui.FRA_TREE_HOLDER.setLayout( lay )
        self.results_tree = QTreeWidget()
        lay.addWidget( self.results_tree )
        
        # Sources
        self.sources = qt.ComboBoxWrapper( self.ui.CMB_SOURCE, (x for x in nc.get_core().endpoint_manager if isinstance( x, nc.DatabaseEndpoint )) )
        
        if len( self.sources ) == 0:
            qt.QMessageBox.warning( parent, "Oops", "You haven't defined any database endpoints. You won't be able to issue a query until you do so." )
        
        # Destinations
        self.destinations = qt.ComboBoxWrapper( self.ui.CMB_DESTINATION,
                                                chain( [GUI_EP],
                                                       (x for x in nc.get_core().endpoint_manager if isinstance( x, nc.Destination )) ) )
        
        # Browser?
        self.__scripts_loaded = False
        self.ui.CHK_ENABLE_BROWSER.setChecked( self.gui.get_settings().enable_browser )
        self.ui.CHK_ENABLE_BROWSER.stateChanged[int].connect( self.__on_CHK_ENABLE_BROWSER_stateChanged )
        self.ui.CHK_B42_SCRIPTS.setChecked( self.gui.b42_gui_settings.auto_load_bio42_scripts )
        self.ui.CHK_B42_SCRIPTS.stateChanged[int].connect( self.__on_CHK_B42_SCRIPTS_stateChanged )
    
    
    def btn_style( self, button: qt.QToolButton ):
        button.setFixedSize( qt.QSize( qt.QWIDGETSIZE_MAX, qt.QWIDGETSIZE_MAX ) )
        button.setIconSize( qt.QSize( 16, 16 ) )
        button.setToolButtonStyle( qt.Qt.ToolButtonFollowStyle )
        button.setProperty( "style", "sidearea" )
        button.setStyleSheet( "" )
    
    
    @property
    def gui( self ) -> B42GuiController:
        return cast( B42GuiController, intermake.Controller.ACTIVE )
    
    
    def __on_CHK_ENABLE_BROWSER_stateChanged( self, _ ):
        self.gui.get_settings().enable_browser = self.ui.CHK_ENABLE_BROWSER.isChecked()
    
    
    def __on_CHK_B42_SCRIPTS_stateChanged( self, _ ):
        self.gui.b42_gui_settings.auto_load_bio42_scripts = self.ui.CHK_B42_SCRIPTS.isChecked()
        
        if self.ui.CHK_B42_SCRIPTS.isChecked():
            self.__request_load_scripts_library()
    
    
    def on_shown( self ):
        if self.gui.b42_gui_settings.auto_load_bio42_scripts:
            self.__request_load_scripts_library()
        else:
            self.populate_scripts()
    
    
    def __request_load_scripts_library( self ):
        if not self.__scripts_loaded:
            def ___callback( result: intermake.Result ):
                assert result.command is intermake.BasicCommand.retrieve( _load_scripts ), result.command
                self.populate_scripts()
            
            
            self.__scripts_loaded = True
            intermake.Controller.ACTIVE.acquire( command = _load_scripts, window = self ).run().listen( ___callback )
    
    
    def apply_view( self, html = "", node_map = None, root: intermake.Result = None ):
        self.received_html = html
        self.received_map = node_map
        self.received_root = root
        
        # Tree
        if self.received_root is not None and self.received_root.is_success:
            self.__set_results_view_on( self.received_root.result )
        else:
            self.__set_results_view_on( None )
        
        # HTML
        if self.is_browser:
            from PyQt5.QtWebEngineWidgets import QWebEnginePage
            wep: QWebEnginePage = self.browser_page
            file_name = self.write_html_to_file()
            wep.load( qt.QUrl.fromLocalFile( file_name ) )  # nb. setHtml doesn't work with visjs, so we always need to use a temporary file
    
    
    def list_list_queries( self ):
        return file_helper.list_dir( self.get_query_folder() )
    
    
    def populate_scripts( self ):
        self.queries = qt.ComboBoxWrapper( self.ui.CMB_QUERY,
                                           tuple( chain( [CUSTOM_QUERY],
                                                         self.list_list_queries(),
                                                         (x for x in intermake.Controller.ACTIVE.app.commands if isinstance( x, nc.ScriptCommand )) ) ) )
        
        self.queries.enabled = True
        self.queries.selected = CUSTOM_QUERY
    
    
    def __editorium_fn_arg( self, arg: ArgInspector ) -> Optional[ArgInspector]:
        if arg.name in (nc.ScriptCommand.ARG_DATABASE,
                        nc.ScriptCommand.ARG_OUTPUT,
                        nc.ScriptCommand.ARG_QUIET,
                        nc.ScriptCommand.ARG_RETRIES,
                        nc.ScriptCommand.ARG_TIMEOUT,
                        nc.ScriptCommand.ARG_DUMP):
            return None
        
        return arg
    
    
    def __on_TXT_CYPHER_textChanged( self ):
        if self.ignore_changes:
            return
        
        self.ignore_changes = True
        self.ui.CMB_QUERY.setCurrentIndex( 0 )
        self.ignore_changes = False
        self.__on_CMB_QUERY_currentIndexChanged( 0 )
    
    
    def __on_CMB_QUERY_currentIndexChanged( self, _ ):
        if self.ignore_changes:
            return
        
        # Find the script!
        q: object = self.queries.selected
        
        # Textbox
        self.ignore_changes = True
        
        if q is CUSTOM_QUERY:
            self.set_script( nc.ScriptCommand( cypher = self.ui.TXT_CYPHER.toPlainText(),
                                               name = "custom_query",
                                               filename = self.editing_script.filename if self.editing_script is not None else None ),
                             update_text = False )
        elif isinstance( q, str ):
            self.load_file( q )
        elif isinstance( q, nc.ScriptCommand ):
            self.set_script( q )
        elif q is not None:
            raise SwitchError( "self.queries.selected", q, instance = True )
        
        self.ignore_changes = False
        
        # Arguments
        if isinstance( self.editing_script, nc.ScriptCommand ):
            self.editing_args = ArgValueCollection( self.editing_script.args )
        else:
            self.editing_args = None
        
        self.editorium.target = self.editing_args
        self.editorium.recreate()
    
    
    def __format_node( self, node: mg.MNode ):
        ent: nc.NcNode = node.data
        return nc.get_core().schema.describe( ent )
    
    
    def write_html_to_file( self ):
        file_name = path.join( intermake.Controller.ACTIVE.app.local_data.local_folder( intermake.constants.FOLDER_TEMPORARY ), "temp.html" )
        file_helper.write_all_text( file_name, self.received_html )
        return file_name
    
    
    def enable_browser( self ):
        from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
        
        owner = self
        
        
        class MyPage( QWebEnginePage ):
            def javaScriptConsoleMessage( self, level, message: str, lineNumber: int, source_id: str ):
                owner.handle_web_interaction( message )
        
        
        self.browser_ctrl = QWebEngineView()
        self.browser_ctrl.setVisible( True )
        self.browser_page = MyPage()
        self.browser_ctrl.setPage( self.browser_page )
        self.ui.GRID_BROWSER_HOLDER.addWidget( self.browser_ctrl )
        self.is_browser = True
    
    
    def handle_web_interaction( self, message ):
        """
        Handles messages RECEIVED FROM the web-browser. 
        :param message: 
        :return: 
        """
        
        # MGRAPH sends messages always start with "MGRAPH". 
        if not message.startswith( "MGRAPH " ):
            return
        
        # The command is of the form MGRAPH command ( args )
        m1 = re.search( "MGRAPH ([a-zA-Z_]+) *\((.+)\)", message )
        
        if not m1:
            return
        
        command = m1.group( 1 )
        args = m1.group( 2 ).strip()
        
        if command == "SELECT_NODE":
            # A node or nodes has been selected
            node_ids = [int( x.strip() ) for x in args.split( "," )]
            
            if len( node_ids ) != 1:
                return
            
            # NeoCommand's created MGraph stores the actual node in `x~~MNode::data~~NodeTag::entity~~MNode`
            node_id = node_ids[0]
            node: mg.MNode = self.received_map.get( node_id )
            
            if node is None:
                return
            
            self.__set_results_view_on( node.data )
    
    
    @qt.exqtSlot()
    def on_BTN_SYSTEM_BROWSER_clicked( self ) -> None:
        """
        Signal handler:
        """
        file_name = self.write_html_to_file()
        io_helper.system_open( file_name )  # `webbrowser` is for URLs, use `open` instead.
    
    
    @qt.exqtSlot()
    def on_BTN_SEND_TO_clicked( self ) -> None:
        """
        Signal handler:
        """
        if not isinstance( self.received_root, nc.Origin ):
            qt.QMessageBox.warning( self, "Oops", "The current data ({}) isn't exportable because it can't act as a data-source. Make sure you have received some data and that you have selected an exportable destination for your query.".format( self.received_root ) )
            return
        
        from .frm_transfer import FrmTransfer
        FrmTransfer.request( self, source = self.received_root )
    
    
    @qt.exqtSlot()
    def on_BTN_EXPORT_AS_clicked( self ) -> None:
        """
        Signal handler:
        """
        if not isinstance( self.received_root, GuiEndpoint ):
            qt.QMessageBox.warning( self,
                                    "Oops",
                                    "The current data ({}) isn't a graph. "
                                    "Make sure that you have selected a graph destination for your query and try again."
                                    .format( self.received_root ) )
            return
        
        graph = self.received_root.read_graph()
        
        if len( graph.nodes ) == 0:
            qt.QMessageBox.warning( self,
                                    "Oops",
                                    "The current graph isn't exportable because it doesn't contain any nodes. "
                                    "Make sure you have received some graph data first." )
        
        file_name = qt.qt_gui_helper.browse_save( self, ";;".join( "{} (*{})".format( x[1][0], x[0] ) for x in mg.exporting.EXTENSION_MAP.items() ) )
        
        if file_name is not None:
            mg.exporting.export_file( graph,
                                      file_name,
                                      fprops = lambda x: cast( x.data, mg.MNode ).properties )
    
    
    @qt.exqtSlot()
    def on_BTN_CUSTOM_LIBRARIES_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.show_command( intermake.import_python_module )
    
    
    @qt.exqtSlot()
    def on_BTN_SAVE_clicked( self ) -> None:
        """
        Signal handler:
        """
        save_over_current = "Save"
        save_to_list = "Save to list..."
        remove_from_list = "Delete"
        save_to_file = "Save to file..."
        opts = [save_over_current, save_to_list, remove_from_list, save_to_file]
        
        sel = qt.menu_helper.show_menu( self, opts )
        
        file_name = self.editing_script.filename if self.editing_script is not None else None
        
        if sel is save_over_current:
            if not file_name:
                qt.QMessageBox.information( self,
                                            self.windowTitle(),
                                            "You must “<i>save to list...</i>” or “<i>save as...</i>” before you can use “<i>save</i>”." )
                return
            
            self.save_file( file_name )
        
        if sel is save_to_list:
            if not self.editing_script:
                qt.QMessageBox.information( self,
                                            self.windowTitle(),
                                            "You must “<i>save to list...</i>” or “<i>save as...</i>” before you can use “<i>save</i>”." )
                return
            
            query_name, ok = qt.QInputDialog.getText( self, "Save query", "Please name your query" )
            
            if ok:
                self.save_file( self.list_name_to_file_name( query_name ) )
        elif sel is remove_from_list:
            if not file_name:
                qt.QMessageBox.information( self,
                                            self.windowTitle(),
                                            "This script is not associated with a file that can be deleted." )
                return
            
            if qt.QMessageBox.question( self,
                                        self.windowTitle(),
                                        "Are you sure that you wish to delete this file?\n{}".format( self.editing_script.filename ),
                                        qt.QMessageBox.Ok | qt.QMessageBox.Cancel
                                        ) != qt.QMessageBox.Ok:
                return
            
            file_helper.recycle_file( self.editing_script.filename )
            self.editing_script.filename = None
        elif sel is save_to_file:
            file_name, _ = qt.QFileDialog.getSaveFileName( self, "Save query", filter = "Queries (*.cypher)" )
            
            if file_name:
                self.save_file( file_name )
        elif sel is not None:
            raise SwitchError( "sel", sel )
    
    
    def save_file( self, file_name: str ):
        if isinstance( file_name, str ):
            self.editing_script = nc.ScriptCommand( cypher = self.ui.TXT_CYPHER.toPlainText(), 
                                                    filename = file_name )
            file_helper.write_all_text( file_name, self.ui.TXT_CYPHER.toPlainText() )
            self.update_title()
        else:
            raise ValueError( "Cannot save - no filename." )
    
    
    def load_file( self, file_name: str ):
        script = nc.ScriptCommand( cypher = file_helper.read_all_text( file_name ),
                                   name = file_helper.get_filename_without_extension( file_name ), 
                                   filename = file_name )
        self.set_script( script )
    
    
    def set_script( self, script: nc.ScriptCommand, update_text: bool = True ):
        if update_text:
            self.ui.TXT_CYPHER.setPlainText( script.plain_text )
        self.editing_script = script
        self.update_title()
    
    
    def update_title( self ):
        self.setWindowTitle( "Query - {} - {}".format( self.editing_script.name, self.editing_script.filename or "(no_file)" ) )
    
    
    def list_name_to_file_name( self, n ):
        return path.join( self.get_query_folder(), n + ".cypher" )
    
    
    def get_query_folder( self ):
        return intermake.Controller.ACTIVE.app.local_data.local_folder( "queries" )
    
    
    @qt.exqtSlot()
    def on_BTN_LOAD_clicked( self ) -> None:
        """
        Signal handler:
        """
        file_name, _ = qt.QFileDialog.getOpenFileName( self, "Open query", filter = "Queries (*.cypher)" )
        
        if file_name:
            self.load_file( file_name )
    
    
    def on_BTN_SHOW_ADVANCED_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.ui.PAGER_SET.setCurrentIndex( 1 )
    
    
    @qt.exqtSlot()
    def on_BTN_BACK_TO_QUERY_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.ui.PAGER_SET.setCurrentIndex( 0 )
    
    
    @qt.exqtSlot()
    def on_BTN_LOCAL_BROWSER_clicked( self ) -> None:
        """
        Signal handler:
        """
        # TODO: these resources placeholders only and are wrong
        self.ui.FRA_BROWSER_HOLDER_BASE.setVisible( not self.ui.FRA_BROWSER_HOLDER_BASE.isVisible() )
        self.ui.BTN_LOCAL_BROWSER.setIcon( resources.next.icon() if self.ui.FRA_BROWSER_HOLDER_BASE.isVisible() else resources.view_list.icon() )
    
    
    @qt.exqtSlot()
    def on_BTN_TREE_clicked( self ) -> None:
        """
        Signal handler:
        """
        self.ui.FRA_TREE_HOLDER_BASE.setVisible( not self.ui.FRA_TREE_HOLDER_BASE.isVisible() )
        self.ui.BTN_TREE.setIcon( resources.next.icon() if self.ui.FRA_TREE_HOLDER_BASE.isVisible() else intermake_qt.view_list.expanddown.icon() )
    
    
    @qt.exqtSlot()
    def on_BTN_EXECUTE_clicked( self ) -> None:
        """
        Signal handler:
        """
        
        # Database
        database: nc.DatabaseEndpoint = self.sources.selected
        
        if database is None:
            qt.QMessageBox.warning( self, "Oops", "A source must be specified." )
            return
        
        # Destination
        destination = self.destinations.selected
        
        if destination is GUI_EP:
            destination = GuiEndpoint()
        elif destination is None:
            qt.QMessageBox.warning( self, "Oops", "A destination must be specified." )
            return
        
        self.apply_view( html = "<html><body>Please wait...</body></html>" )
        
        self.editing_args.set_value( nc.ScriptCommand.ARG_DATABASE, database )
        self.editing_args.set_value( nc.ScriptCommand.ARG_OUTPUT, destination )
        
        intermake.acquire( command = self.editing_script,
                           window = self,
                           auto_close = True,
                           ).run( **self.editing_args.tokwargs() ).listen( self.__execute_complete )
    
    
    def __execute_complete( self, result: intermake.Result ):
        if result.is_error:
            # Display errors directly
            self.apply_view( html = qt.qt_gui_helper.ansi_to_html( ansi_format_helper.format_traceback( result.exception, result.traceback ) ),
                             root = result )
        elif isinstance( result.result, nc.DbStats ) and isinstance( result.result.endpoint, GuiEndpoint ):
            # Result as a `GuiEndpoint`
            if len( result.result.endpoint.graph.nodes ) != 0:
                map = { }
                self.apply_view( html = mg.exporting.export_vis_js( result.result.endpoint.graph,
                                                                    fnode = self.__format_node,
                                                                    rooted = False,
                                                                    map = map ),
                                 root = result,
                                 node_map = map )
            else:
                self.apply_view( html = self.__extra_data_to_html( result.result.endpoint.extra_data ),
                                 root = result )
        else:
            self.apply_view( html = str( result.result ),
                             root = result )
    
    
    def __extra_data_to_html( self, items: List[object] ):
        r = []
        r.append( "<html><title>Result of query</title><body>" )
        
        r.append( "Query result does not contain a graph." )
        
        r.append( "<ul>" )
        
        if len( items ) == 0:
            r.append( "<li>No items</li>" )
        
        for item in items:
            r.append( "<li>" )
            
            if isinstance( item, nc.NcData ):
                r.append( "{} = {}".format( item.varname, item.value ) )
            else:
                r.append( "{}".format( item ) )
            
            r.append( "</li>" )
        
        r.append( "</ul></body></html>" )
        
        return "\n".join( r )
    
    
    def __set_results_view_on( self, x ):
        self.results_tree.clear()
        
        self.results_tree.setHeaderItem( QTreeWidgetItem() )
        self.results_tree.headerItem().setText( 0, "name" )
        self.results_tree.headerItem().setText( 1, "type" )
        self.results_tree.headerItem().setText( 2, "value" )
        
        if isinstance( x, nc.NcEntity ):
            self.results_tree.addTopLevelItem( self.__make_tree_node( x.varname, x ) )
        else:
            self.results_tree.addTopLevelItem( self.__make_tree_node( "untitled", x ) )
    
    
    def __make_tree_node( self, n, x ):
        item = QTreeWidgetItem()
        
        if isinstance( x, mg.MNode ):
            x = x.data
        elif isinstance( x, mg.MEdge ):
            x = x.data
        
        if isinstance( x, nc.DbStats ):
            item.setText( 0, n )
            item.setText( 1, "Result" )
            item.setText( 2, str( x ) )
            
            for k, v in x.__dict__.items():
                if not k.startswith( "_" ):
                    item.addChild( self.__make_tree_node( ".{}".format( k ), v ) )
        elif isinstance( x, intermake.Result ):
            item.setText( 0, n )
            item.setText( 1, "Result" )
            item.setText( 2, x.command )
            item.addChild( self.__make_tree_node( "value", x.result ) )
        elif isinstance( x, GuiEndpoint ):
            item.setText( 0, n )
            item.setText( 1, "Endpoint" )
            item.setText( 2, str( x ) )
            item.addChild( self.__make_tree_node( "value", x.graph ) )
        elif isinstance( x, mg.MGraph ):
            item.setText( 0, n )
            item.setText( 1, "Graph" )
            item.setText( 2, str( x ) )
            
            for i, v in enumerate( x.nodes ):
                item.addChild( self.__make_tree_node( "node{}".format( i ), v ) )
            
            for i, v in enumerate( x.edges ):
                item.addChild( self.__make_tree_node( "edge{}".format( i ), v ) )
        elif isinstance( x, nc.NcNode ):
            item.setText( 0, n )
            item.setText( 1, "Node" )
            item.setText( 2, x.label )
            
            for k, v in x.properties.items():
                item.addChild( self.__make_tree_node( ".{}".format( k ), v ) )
        elif isinstance( x, nc.NcEdge ):
            item.setText( 0, n )
            item.setText( 1, "Edge" )
            item.setText( 2, x.label )
            
            item.addChild( self.__make_tree_node( "start", x.start ) )
            item.addChild( self.__make_tree_node( "end", x.end ) )
            
            for k, v in x.properties.items():
                item.addChild( self.__make_tree_node( ".{}".format( k ), v ) )
        elif isinstance( x, nc.NcData ):
            item.setText( 0, n or x.varname )
            item.setText( 1, "Data" )
            item.setText( 2, str( x.value ) )
        else:
            item.setText( 0, n )
            item.setText( 1, "Object" )
            item.setText( 2, str( x ) )
        
        return item
