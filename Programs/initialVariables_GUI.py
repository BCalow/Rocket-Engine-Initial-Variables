from PyQt6.QtWidgets import (
							QApplication, 
							QWidget, 
							QVBoxLayout,
							QCheckBox, 
							QLabel,
							QGridLayout,
							QHBoxLayout
)
import sys


#TEMP
#Variables left to find
R = 0
M = 0
T_0 = 0
T_c = 0
T_t = 0
T_e = 0
P_0 = 0
P_c = 0
P_t = 0
P_e = 0
gamma = 0
Ma_e = 0
A_e = 0
A_t = 0
v_e = 0
mdot = 0
F = 0
P_a = 0


#Input Variables

chamberInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Chamber Temperature",     "T_c",      "(°C)"    ],
	["Chamber Pressure",        "P_c",      "(kPa)"   ],
]

throatInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Throat Area",             "A_t",      "(m²)"    ],
	["Throat Temperature",      "T_t",      "(°C)"    ],
	["Throat Pressure",         "P_t",      "(kPa)"   ],
]

exitInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Exit Area",               "A_e",      "(m²)"    ],
	["Exit Temperature",        "T_e",      "(°C)"    ],
	["Exit Pressure",           "P_e",      "(kPa)"   ],
	["Exit Mach Number",        "Ma_e",     "(-)"     ],
]

stagnationInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Stagnation Temperature",  "T_0",      "(°C)"    ],
	["Stagnation Pressure",     "P_0",      "(kPa)"   ],
]

generalInputs = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Ratio of Specific Heats", "γ",        "(-)"     ],
	["Specific Gas Constant",   "R",        "(-)"     ],
]


#Equation Variable Lists

equationVariables = [
	[R, M],                             #eq 1.1

	[T_0, T_c],                         #eq 1.4 @ Chamber
	[T_0, T_t, gamma],                  #eq 1.4 @ Throat
	[T_0, T_e, Ma_e, gamma],            #eq 1.4 @ Exit

	[P_0, P_c],                         #eq 1.5 @ Chamber
	[P_0, P_t, gamma],                  #eq 1.5 @ Throat
	[P_0, P_e, Ma_e, gamma],            #eq 1.5 @ Exit

	[A_e, A_t, Ma_e, gamma],            #eq 1.6 @ Throat + Exit

	[v_e, R, T_0, P_e, P_0, gamma],     #eq 2.1

	[mdot, A_t, P_0, R, T_0, gamma],    #eq 2.2

	[F, mdot, v_e, P_e, P_a, A_e],      #eq 2.3
]


#Functions

def checkConstraint(equationVariables, selectedVariables):
	knownVariables = set(selectedVariables)
	changed = True

	while changed:
		changed = False
		for group in equationVariables:
			missingVariables = group - knownVariables
			if len(missingVariables) == 1:
				newVariable = missingVariables.pop()
				if newVariable not in knownVariables:
						knownVariables.add(newVariable)
						changed = True
			if len(missingVariables) == 0:
				return False
	
	return  knownVariables


#Input Section

class dataInput(QCheckBox, QLabel):
	def __init__(self, text="", parent=None):
		super.__init__(text, parent)
		layout = QHBoxLayout(self)

		self.checkbox = QCheckBox()
		self.setChecked(False)

		self.label = QLabel()

	def disable(self):
		self.setEnabled(False)
	
	def enable(self):
		self.setEnabled(True)


#Main Window

class mainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Initial Variable Calculation")
		self.resize(1000, 500)

		layout = QGridLayout()
