"""
This module contains the primary `Bio42`:t: test case, this processes a large
dataset and exemplifies most of the commands within `Bio42`:t: and
`NeoCommand`:t:.

* Before commencing the test ensure Neo4j is installed and working!
* You'll need the `Paris Plasmids` dataset. 

No binary is created to run this test suite, to run it please invoke Python::

    python -m bio42_tests xxx
    
Where xxx is the directory containing the dataset.
    
If you get an `ExistsError` it's because the test has already been run.
You'll need to clean up manually before starting again.
    
The `__main__.py` contains the import script - this is documented, for example
purposes, inline. 
"""
