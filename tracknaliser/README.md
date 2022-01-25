
# Greetings!

This is a package produced by group 8

## Installation

```bash
navigate to tracknaliser folder
pip install .
```

## Usage
    
Invoke the tool with `greentrack -S X Y -E X Y --simple`:

example: "greentrack --start 5 6  --end 5 7 --verbose"

or use it on your own library:

See "library_interface_example.py" for an example


## Editing code (Notes for Team 8)
Messages from Arosi:
All the classes are now in the folder "tracknaliser_library". This is necessary for creation of the package and CLI

Don't forget that if you refer to other classes, e.g. from "clustering.py", you must now use "from .clustering import ..." observe the "."
This is used for relative imports. Alternatively, you can write something similar to "tracknaliser_library.clustering" for the absolute path

When running tests, navigate to tracknaliser_library and run "pytest". No other argument needed.

