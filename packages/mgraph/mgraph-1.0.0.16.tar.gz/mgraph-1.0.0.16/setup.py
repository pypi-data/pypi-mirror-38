from distutils.core import setup

def __rld():
    try:
        import os.path
        with open(os.path.join(os.path.dirname(__file__), "readme.rst")) as file:
            return file.read()
    except Exception as ex:
        return "(could not load readme: {})".format(ex)
    
setup( name = "mgraph",
       url = "https://bitbucket.org/mjr129/mgraph",
       version = "1.0.0.16",
       description = "Yet another graphing library. This library supports `Groot`:t:, providing functionality for dealing with graphs somewhere on the phylogenetic tree/network border.",
       long_description = __rld(),
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       python_requires = ">=3.6",
       packages = \
           [
               "mgraph"
           ],

       install_requires = \
           [
               "ete3",
               "mhelper"
           ],

       classifiers = \
           [
               "Development Status :: 3 - Alpha",
        
               "Topic :: Software Development :: Libraries",
               "Topic :: Software Development :: Libraries :: Python Modules",
        
               "Operating System :: OS Independent",
        
               "Intended Audience :: Science/Research",
               "Intended Audience :: Developers",
        
               "Topic :: Scientific/Engineering",
               "Topic :: Scientific/Engineering :: Bio-Informatics",
               "Topic :: Multimedia :: Graphics :: Presentation",
        
               "License :: OSI Approved :: GNU Affero General Public License v3",
               "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        
               "Natural Language :: English",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3",
               "Programming Language :: Python :: 3 :: Only"
           ]
       )
