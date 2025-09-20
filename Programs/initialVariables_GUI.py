from PyQt6.QtWidgets import (
QApplication, QWidget, QVBoxLayout,
QCheckBox, QLabel
)
import sys


chamberInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
    ["Chamber Temperature",     "T_c",      "°C"    ],
    ["Chamber Pressure",        "P_c",      "kPa"   ],
]

throatInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
    ["Throat Area",             "A_t",      "m²"    ],
    ["Throat Temperature",      "T_t",      "°C"    ],
    ["Throat Pressure",         "P_t",      "kPa"   ],
]

exitInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
    ["Exit Area",               "A_e",      "m²"    ],
    ["Exit Temperature",        "T_e",      "°C"    ],
    ["Exit Pressure",           "P_e",      "kPa"   ],
    ["Exit Mach Number",        "Ma_e",     "-"     ],
    
]

generalInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
    ["Ratio of Specific Heats", "γ",        "-"     ],
    ["Specific Gas Constant",   "R",        "-"     ],
]