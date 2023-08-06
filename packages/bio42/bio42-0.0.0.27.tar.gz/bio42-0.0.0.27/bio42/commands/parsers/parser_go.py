from mhelper import isFilename, EFileMode, string_helper
import intermake
import neocommand

from bio42.application import app
from bio42 import schema


_OWL_EXT = ".owl"


@app.command( folder = "import" )
def import_go( endpoint: neocommand.Destination,
               file_name: isFilename[EFileMode.READ, _OWL_EXT] ) -> None:
    """
    Imports GO terms from the GO database.
    
    :param endpoint: Where to send the data to. 
    :param file_name:   Where to get the data from 
    """
    from xml.etree import ElementTree
    from xml.etree.ElementTree import Element
    
    _GO_ID_PREFIX = "GO:"
    
    with intermake.pr.pr_action( "Parsing GO tree" ):
        tree = ElementTree.parse( file_name )
    
    root = tree.getroot()
    
    CLASS_ID = '{http://www.w3.org/2002/07/owl#}Class'
    CLASS_SUBCLASS_ID = '{http://www.w3.org/2000/01/rdf-schema#}subClassOf'
    CLASS_SUBCLASS_RESOURCE_ID = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource'
    CLASS_ID_ID = '{http://www.geneontology.org/formats/oboInOwl#}id'
    GO_SUBCLASS_ID_REMOVE = 'http://purl.obolibrary.org/obo/GO_'
    
    
    def remove_namespace( tag ):
        tag = str( tag )
        
        if "}" in tag:
            return tag[tag.index( "}" ) + 1:]
        
        return tag
    
    
    with endpoint.open_writer() as writer:
        with intermake.pr.pr_action( "Parsing GO nodes" ) as action:
            for element in root:
                if not isinstance( element, Element ):
                    continue
                
                action.increment()
                
                if element.tag == CLASS_ID:
                    class_subclass = []
                    class_misc = { }
                    class_id = None
                    
                    for sub_element in element:
                        if not isinstance( element, Element ):
                            continue
                        
                        if sub_element.tag == CLASS_SUBCLASS_ID:
                            resource_id = sub_element.get( CLASS_SUBCLASS_RESOURCE_ID )
                            if resource_id:
                                class_subclass.append( string_helper.remove_prefix( resource_id, GO_SUBCLASS_ID_REMOVE ) )
                            continue
                        elif sub_element.tag == CLASS_ID_ID:
                            class_id = string_helper.remove_prefix( sub_element.text, _GO_ID_PREFIX )
                            continue
                        else:
                            key = remove_namespace( sub_element.tag )
                        
                        if key == "IAO_0000115":  # because it's ridiculous
                            key = "description"
                        elif key == "hasOBONamespace":  # because it's also quite silly
                            key = "namespace"
                        elif key == "label":  # because having "node.label" and "node.data.label" as two different things is confusing
                            key = "name"
                        elif key.startswith( "has" ):  # because this makes it sound like a boolean, but it isn't, it's the value
                            key = key[len( "has" ):]
                        
                        key = key.lower()
                        
                        if sub_element.text:
                            text = sub_element.text.strip()
                            
                            if text:
                                if key in class_misc:
                                    if not isinstance( class_misc[key], list ):
                                        class_misc[key] = [class_misc[key]]
                                    
                                    class_misc[key].append( text )
                                else:
                                    class_misc[key] = text
                    
                    if class_id:
                        writer.create_node( label = schema.Go,
                                            uid = class_id,
                                            properties = class_misc )
                        
                        for subclass in class_subclass:
                            writer.create_edge( label = schema.GoClassContainsGoClass,
                                                start_uid = subclass,
                                                end_uid = class_id,
                                                properties = { } )
