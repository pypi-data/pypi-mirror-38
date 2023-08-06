from distutils.core import setup

def __rld():
    try:
        import os.path
        with open(os.path.join(os.path.dirname(__file__), "readme.rst")) as file:
            return file.read()
    except Exception as ex:
        return "(could not load readme: {})".format(ex)
    
setup( name = "neocommand",
       url = "https://bitbucket.org/mjr129/neocommand",
       version = "0.0.0.41",
       description = "intermake extension for creating Neo4j driven applications.",
       long_description = __rld(),
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       python_requires = ">=3.6",
       
       packages = \
           [
               "neocommand",
               "neocommand.application",
               "neocommand.neoconnection",
               "neocommand.neoconnection.drivers",
               "neocommand.commands",
               "neocommand.neocsv",
               "neocommand.data",
               "neocommand.endpoints",
               "neocommand.helpers"
           ],
       
       entry_points = \
           {
               "console_scripts": ["neocommand = neocommand.__main__:main"]
           },
       
       
       install_requires = \
           [
               "PyQt5",
               "mgraph",
               "typing",
               "keyring",
               "colorama",
               "py-flags",
               "mhelper",
               "progressivecsv",
               "neo4j-driver",
               "py2neo",
               "editorium",
               "intermake",
               'stringcoercion'
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
