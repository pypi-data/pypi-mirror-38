"""
Colourz
=======

Colourz allows console text to appear with additional style

Usage
-----

Print strings with colour;

`Colourz.normal("Print this in red", "RED")`

Print strings in bold;
`Colourz.bold("Print this in bold")`

Combine the two and print in bold with colour;
`Colourz.bold("Print this in bold red", "RED")`
"""

from .colourz import normal, bold
from .spinners import Bullets