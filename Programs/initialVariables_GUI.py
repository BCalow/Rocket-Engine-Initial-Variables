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
							QSpacerItem,
)
from PyQt6.QtGui import(
							QFontMetrics
)
from PyQt6.QtCore import(
							Qt,
							pyqtSignal
)
import sys


#TEMP
#Variables left to find
R = 0
M = 0
T_s = 0
T_c = 0
T_t = 0
T_e = 0
P_s = 0
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
	["Ratio of Specific Heats", "gamma",        "(-)"     ],
	["Specific Gas Constant",   "R",        "(-)"     ],
]

allInputs_vars = [
	chamberInputs_vars,
	throatInputs_vars,
	exitInputs_vars,
	stagnationInputs_vars,
	generalInputs_vars
]


#Equation Variable Lists
eqVars = [
    frozenset({"R", "M"}),                         	 			# eq 1.1
    frozenset({"T_0", "T_c"}),                      			# eq 1.4 @ Chamber
    frozenset({"T_0", "T_t", "gamma"}),                 		# eq 1.4 @ Throat
    frozenset({"T_0", "T_e", "Ma_e", "gamma"}),         		# eq 1.4 @ Exit
    frozenset({"P_0", "P_c"}),                      			# eq 1.5 @ Chamber
    frozenset({"P_0", "P_t", "gamma"}),                 		# eq 1.5 @ Throat
    frozenset({"P_0", "P_e", "Ma_e", "gamma"}),         		# eq 1.5 @ Exit
    frozenset({"A_e", "A_t", "Ma_e", "gamma"}),         		# eq 1.6 Throat+Exit
    frozenset({"v_e", "R", "T_0", "P_e", "P_0", "gamma"}),  	# eq 2.1
    frozenset({"mdot", "A_t", "P_0", "R", "T_0", "gamma"}), 	# eq 2.2
    frozenset({"F", "mdot", "v_e", "P_e", "P_a", "A_e"})		# eq 2.3
]


#Input Section
class dataInput(QWidget):
	toggled = pyqtSignal(str, bool)

	def __init__(self, text=None, widths=None, parent=None):
		super().__init__(parent)
		layout = QGridLayout(self)

		self.var_id = text[1] if text else ""

		self.checkbox = QCheckBox()
		self.checkbox.setChecked(False)
		self.checkbox.toggled.connect(lambda checked: self.toggled.emit(self.var_id, checked))

		self.name = QLabel(text[0] if text else "")

		self.symbol = QLabel(text[1] if text  else "")

		self.unit = QLabel(text[2] if text else "")

		self.input = QLineEdit()
		self.input.setEnabled(False)
		self.input.setFixedWidth(120)
		self.input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
		self.input.setAlignment(Qt.AlignmentFlag.AlignRight)

		if widths:
			self.name.setFixedWidth(widths[0])
			self.symbol.setFixedWidth(widths[1])
			self.unit.setFixedWidth(widths[2])

		layout.addWidget(self.checkbox, 0, 0, 1, 1)
		layout.addWidget(self.name, 0, 1, 1, 1)
		layout.addWidget(self.symbol, 0, 2, 1, 1)
		layout.addWidget(self.unit, 0, 3, 1, 1)		
		layout.addWidget(self.input, 0, 4, 1, 1)

		layout.setHorizontalSpacing(20)
		layout.setVerticalSpacing(5)

		self.checkbox.stateChanged.connect(self.inputToggle)

	def setSelectable(self, enabled: bool):
		if not self.checkbox.isChecked():
			self.setEnabled(enabled)

	def setDerived(self):
		self.checkbox.setChecked(False)
		self.checkbox.setEnabled(False)
		self.input.setEnabled(False)
		self.input.setText(None)
		self.setStyleSheet("color: #6a6a6a;")

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

		self.inputValues: dict[str, dataInput] = {}
		self.derived: set[str] = set()

		mainLayout = QHBoxLayout()

		gridLayout = QGridLayout()

		fm = QFontMetrics(QLabel().font())

		self.column_widths = (
			max(fm.horizontalAdvance(row[0]) for group in allInputs_vars for row in group) + 20,
			max(fm.horizontalAdvance(row[1]) for group in allInputs_vars for row in group) + 20,
			max(fm.horizontalAdvance(row[2]) for group in allInputs_vars for row in group) + 20
		)

		def addGroup(layout, row, col, title, data):
			group = QGroupBox(title)
			groupLayout = QVBoxLayout()
			group.setLayout(groupLayout)

			for i, vars in enumerate(data):
				section = dataInput(vars, self.column_widths)
				section.toggled.connect(self.onToggle)
				self.inputValues[section.var_id] = section
				groupLayout.addWidget(section)

			group.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

			layout.addWidget(group, row, col)

		addGroup(gridLayout, 0, 0, "Chamber", chamberInputs_vars)
		addGroup(gridLayout, 1, 0, "Throat", throatInputs_vars)
		addGroup(gridLayout, 2, 0, "Exit", exitInputs_vars)
		addGroup(gridLayout, 3, 0, "Stagnation", stagnationInputs_vars)
		addGroup(gridLayout, 4, 0, "General", generalInputs_vars)

		mainLayout.addLayout(gridLayout)
		mainLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
		
		self.setLayout(mainLayout)
	
	def selectedSet(self) -> set[str]:
		return {var_id for var_id, widget in self.inputValues.items() if widget.isChecked()}
	
	def onToggle(self, var_id: str, checked: bool):
		print(f"{var_id} toggled -> {checked}")
		print("Now selected: ", self.selectedSet())


#Main	
def main():
    app = QApplication(sys.argv)

    window = mainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()