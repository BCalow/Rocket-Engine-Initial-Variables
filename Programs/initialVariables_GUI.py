from PyQt6.QtWidgets import (
							QApplication, 
							QWidget, 
							QVBoxLayout,
							QCheckBox, 
							QLabel,
							QGridLayout,
							QHBoxLayout,
							QLineEdit,
							QGroupBox,
							QSizePolicy,
							
)
from PyQt6.QtGui import(
						QFontMetrics
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

chamberInputs_vars = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Chamber Temperature",     "T_c",      "(°C)"    ],
	["Chamber Pressure",        "P_c",      "(kPa)"   ],
]

throatInputs_vars = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Throat Area",             "A_t",      "(m²)"    ],
	["Throat Temperature",      "T_t",      "(°C)"    ],
	["Throat Pressure",         "P_t",      "(kPa)"   ],
]

exitInputs_vars = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Exit Area",               "A_e",      "(m²)"    ],
	["Exit Temperature",        "T_e",      "(°C)"    ],
	["Exit Pressure",           "P_e",      "(kPa)"   ],
	["Exit Mach Number",        "Ma_e",     "(-)"     ],
]

stagnationInputs_vars = [
   #["Name",                    "Symbol",   "Unit"  ],
	["Stagnation Temperature",  "T_0",      "(°C)"    ],
	["Stagnation Pressure",     "P_0",      "(kPa)"   ],
]

generalInputs_vars = [
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

class dataInput(QWidget):
	def __init__(self, text=None, parent=None):
		super().__init__(parent)
		layout = QGridLayout(self)

		self.checkbox = QCheckBox()
		self.checkbox.setChecked(False)

		self.name = QLabel(text[0] if text and len(text) > 1 else "")

		self.unit = QLabel(text[2] if text and len(text) > 1 else "")

		self.input = QLineEdit()
		self.input.setEnabled(False)
		self.input.setFixedWidth(80)
		self.input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

		layout.addWidget(self.checkbox, 0, 0, 1, 1)
		layout.addWidget(self.name, 0, 1, 1, 1)
		layout.addWidget(self.input, 0, 2, 1, 1)
		layout.addWidget(self.unit, 0, 3, 1, 1)

		layout.setColumnStretch(1, 1)
		layout.setColumnStretch(2, 0)
		layout.setColumnStretch(3, 0)

		self.checkbox.stateChanged.connect(self.inputToggle)

	def inputToggle(self):
		self.input.setEnabled(self.checkbox.isChecked())

	def disable(self):
		self.setEnabled(False)
	
	def enable(self):
		self.setEnabled(True)

	def isChecked(self):
		return self.checkbox.isChecked()
	
	def inputValue(self):
		return self.input.text()


#Main Window

class mainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Initial Variable Calculation")
		self.resize(1000, 500)

		mainLayout = QGridLayout()

		def addGroup(layout, row, col, title, data):
			group = QGroupBox(title)
			groupLayout = QVBoxLayout()
			group.setLayout(groupLayout)

			for i, vars in enumerate(data):
				section = dataInput(vars)
				groupLayout.addWidget(section)

			layout.addWidget(group, row, col)

		addGroup(mainLayout, 0, 0, "Chamber", chamberInputs_vars)
		addGroup(mainLayout, 1, 0, "Throat", throatInputs_vars)
		addGroup(mainLayout, 2, 0, "Exit", exitInputs_vars)
		addGroup(mainLayout, 0, 1, "Stagnation", stagnationInputs_vars)
		addGroup(mainLayout, 1, 1, "General", generalInputs_vars)

		self.setLayout(mainLayout)


#Main
		
def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()