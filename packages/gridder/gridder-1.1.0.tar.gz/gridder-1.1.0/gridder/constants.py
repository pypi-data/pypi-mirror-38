"""Gridder is a program to generate an image containing a grid according to provided settings.
    Copyright (C) 2018  Federico Salerno <itashadd+gridder[at]gmail.com>

    Data module with constants used throughout the program.


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>
"""

from gridder.drawer import Drawer, SHAPE_METHOD_PREFIX
import re


# Remember to update in setup.py.
VERSION = "1.1.0"
"""Current version of gridder.

The version is given in major.minor.patch format.
The following format applies consistently starting with
version 1.1.0:
- major is a version with significant changes that breaks 
    compatibility with previous versions.
- minor is a version with improvements and additions that 
    do not break compatibility with previous versions.
- patch is a version similar to the major.minor, with 
    bug fixes and minor changes that remain compatible.
"""

# Note: change drawer.py too if the pattern changes.
# Both files cannot link to each other recursively.
shape_name_pattern = re.compile(SHAPE_METHOD_PREFIX)
shape_method_pattern = re.compile(SHAPE_METHOD_PREFIX + r"[^_]+")
SUPPORTED_SHAPES = [shape_name_pattern.split(name)[1].lower()
                    for name in Drawer.__dict__.keys()
                    if shape_method_pattern.fullmatch(name)]
"""All the grid shapes supported by gridder.

Supported grid shapes are automatically extrapolated by 
introspection into the Drawer class depending on what 
draw methods it implements.
"""
