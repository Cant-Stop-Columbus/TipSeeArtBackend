#! NB: After adding new Schema classes, make sure to add them here so they can be accessible to other modules!
#!     If adding a new class to an existing file in this folder, use the following syntax:
#!       `from .{existing_filename_without_dot_py} import ExistingClassName, {NewClassName}`
#!     And if you've just created a new file containing at least one new class to import:
#!       `from .{new_filename_without_dot_py} import {NewClassName}`
from .artist import *
from .user import *
from .crossovers import *
from .media import *
