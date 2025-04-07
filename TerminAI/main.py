from PyQt5.QtWidgets import QApplication
import sys

from TerminAI.display.gui import ModernTerminal

def run():
	app = QApplication(sys.argv)
	terminal = ModernTerminal()
	terminal.show()
	sys.exit(app.exec_())