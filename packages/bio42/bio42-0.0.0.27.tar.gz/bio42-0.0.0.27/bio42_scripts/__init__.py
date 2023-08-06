"""
Includes a set of default scripts for B42.

These are loaded when starting `FrmQueryBrowser` in the intermake.GUI, or may be loaded, in
intermake.CLI or Python proper, by using `import bio42_scrips`.

Note that the scripts are registered with the application - they are not "exported" as Python
variables (though from intermake.PYI they *will* be available as defined locals).
"""

from bio42_scripts import scripts as _scripts
