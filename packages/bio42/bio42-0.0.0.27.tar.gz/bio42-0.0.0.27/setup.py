from distutils.core import setup

def __rld():
    try:
        import os.path
        with open(os.path.join(os.path.dirname(__file__), "readme.rst")) as file:
            return file.read()
    except Exception as ex:
        return "(could not load readme: {})".format(ex)

setup( name = "bio42",
       url = "https://bitbucket.org/mjr129/bio42",
       version = "0.0.0.27",
       description = "Bio42. Analyser and database manager and for large biological networks stored in Neo4j.",
       long_description = __rld(),
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       python_requires = ">=3.6",
       
       entry_points = \
           {
               "console_scripts": ["bio42 = bio42.__main__:main"]
           },
       
       packages = \
           [
               "bio42",
               "bio42.application",
               "bio42.commands",
               "bio42.commands.downloads",
               "bio42.commands.parsers",
               "bio42_gui",
               "bio42_gui.controller",
               "bio42_gui.controls",
               "bio42_gui.forms",
               "bio42_gui.forms.designer",
               "bio42_gui.forms.designer.resources",
               "bio42_scripts",
               "bio42_tests"
           ],

       install_requires = \
           [
               "uniprot",
               "typing",
               "py-flags",
               "colorama",
               "editorium",
               "stringcoercion",
               "keyring",
               "progressivecsv",
               "biopython",
               "intermake",
               "mhelper",
               "PyQt5",
               "neocommand",
               'mgraph'
           ],
       
       classifiers = \
           [
               "Development Status :: 3 - Alpha",
        
               "Environment :: Console",
               "Environment :: Win32 (MS Windows)",
               "Environment :: X11 Applications :: Qt",
               "Environment :: MacOS X",
               "Operating System :: OS Independent",
               "Operating System :: Microsoft :: Windows",
               "Operating System :: MacOS",
               "Operating System :: POSIX :: Linux",
        
               "Intended Audience :: Science/Research",
               "Topic :: Database",
               "Topic :: Scientific/Engineering",
               "Topic :: Scientific/Engineering :: Bio-Informatics",
               "Topic :: Utilities",
               "Topic :: Multimedia :: Graphics :: Presentation",
        
               "License :: OSI Approved :: GNU Affero General Public License v3",
               "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        
               "Natural Language :: English",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3 :: Only"
           ]
       )
