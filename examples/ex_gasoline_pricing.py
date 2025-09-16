#!/usr/bin/env python3

"""
ex_gasoline_pricing.py
Gasoline price converter
"""

import sys
from pyx import *

sys.path.insert(0, "..")
from pynomo.nomographer import *

# allow latex commands in PyX such as \frac{a}{b}
pyx.text.set(text.LatexEngine)

N_params_1 = {
    "u_min": 1.1,
    "u_max": 1.6,
    "function": lambda u: u,
    "title": r"$\frac{CAD} {L}$",
    "tick_levels": 4,
    "tick_text_levels": 3,
    "text_format": r"$\$%3.3f$",
    "scale_type": "linear smart",
    "tick_side": "left",
}

N_params_2 = {
    "u_min": 1.0,
    "u_max": 1.5,
    "function": lambda u: u,
    "title": r"$\frac {CAD} {USD}$",
    "tick_levels": 4,
    "tick_text_levels": 3,
    "text_format": r"$%3.4f$",
    "scale_type": "linear smart",
    "title_x_shift": 0.5,
    "title_rotate_text": True,
}

N_params_3 = {
    "u_min": 3.0,
    "u_max": 5.0,
    "function": lambda u: u / 3.78541,
    "title": r"$\frac {USD}  {US Gal}$",
    "tick_levels": 4,
    "tick_text_levels": 2,
    "scale_type": "linear smart",
    "text_format": r"$\$%3.3f$",
}

block_1_params = {
    "block_type": "type_2",
    "f1_params": N_params_1,
    "f2_params": N_params_2,
    "f3_params": N_params_3,
    "isopleth_values": [[1.3, 1.4, "x"]],
}

main_params = {
    "filename": "ex_gasoline_pricing.pdf",

    # paper size is US letter, halved
    "paper_height": 11.0 * 2.54 / 2.0,
    "paper_width": 8.5 * 2.54 / 2.0,

    "block_params": [block_1_params],
    "transformations": [("rotate", 0.01), ("scale paper",)],
    "title_str": r"\huge \textbf{Gas Price Converter}",
    "title_y": 13.50,
    "title_box_width": 15.0,
    "extra_texts": [
        {
            "x": 1.0,
            "y": 12.5,
            "text": r"\noindent Is gasoline cheaper \
            south of the 49\textsuperscript{th}? Use this gas price \
            converter to be sure. In the example shown, \
            \$1.300 $\frac{CAD}{L}$ is the same price as \
            \$3.52 $\frac{USD}{US}$ \
            if the exchange rate is 1.40 $\frac{CAD}{USD}$.",
            "width": 8.0,
        },
        {
            "text": r"\copyright Daniel Boulet (2019-2021)",
            "x": 3.0,
            "y": -0.0,
        },
    ],
}

Nomographer(main_params)

################## end of can.py ################
