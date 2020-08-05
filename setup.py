# flake8: noqa
from cx_Freeze import setup, Executable

base = None    

executables = [Executable("sce.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "sce",
    options = options,
    version = "1.0",
    description = 'lmao',
    executables = executables
)