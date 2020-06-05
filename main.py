import pprint
import sys
import typing as tp

import lark
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QTextEdit

from Parser import Parser
from PyplotBuilder import PyplotBuilder as Builder
from spec import SPEC


python_text = """
X = np.linspace(-np.pi, np.pi, 50)
Y1 = -np.cos(X)
Y2 = np.cos(X)
"""

code_text = """
Line(
    x: X,
    y: Y1,
    width: 5,
),
Line(
    x: X,
    y: Y2,
),
title: "test",
"""

grammar = open("grammar.ebnf").read()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.lark_parser = lark.Lark(grammar)
        self.ast_parser = Parser(SPEC)
        self.builder = Builder()

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)

        self.setMinimumSize(QSize(800, 600))    
        self.setWindowTitle("uplot")

        self.python_edit = QTextEdit()
        self.python_edit.setFont(QFont("Monaco"))
        self.python_edit.insertPlainText(python_text.strip())

        self.code_edit = QTextEdit()
        self.code_edit.setFont(QFont("Monaco"))
        self.code_edit.insertPlainText(code_text.strip())

        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.update)

        lbox = QVBoxLayout()
        lbox.addWidget(self.python_edit)
        lbox.addWidget(self.code_edit)
        lbox.addWidget(update_btn)

        widget = QWidget()
        widget.setLayout(lbox)

        self.box = QHBoxLayout()
        self.box.addWidget(widget)
        self.box.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(self.box)
        self.setCentralWidget(widget)
        
        self.update()


    def update(self):
        self.fig.clf()

        ast = self.lark_parser.parse(self.code_edit.toPlainText())
        data = self.ast_parser.parse(ast)

        self.builder.build(data, self.python_edit.toPlainText(), self.fig)

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())