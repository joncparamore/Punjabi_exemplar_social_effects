#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:06:37 2025

@author: gina
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---------------Import Packages---------------#
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import random
#---------------------------------------------#

#---------------Import Stimuli and Shuffle Order---------------#
pan_stimuli_df = pd.read_csv("pan_stimuli.csv")
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()
random.shuffle(pan_stimuli)
#Wordlist Variables
word_num = 0
word_list = pan_stimuli
#---------------------------------------------#

#---------------initialize app and window---------------#
app = QApplication([])
window = QWidget()
window.setWindowTitle("Warmup")
window.showFullScreen()
#---------------------------------------------#


#---------------Define Window Layout---------------#
layout = QVBoxLayout() #automatically stacks and centers items in the center of the space
layout.setAlignment(Qt.AlignCenter)

#item 1: instructions
instructions = QLabel("In this phase, you will see a series of words on the screen. Please silently read each word.")
instructions.setFont(QFont("Verdana", 20))
instructions.setWordWrap(True)
instructions.setAlignment(Qt.AlignCenter)
instructions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
layout.addWidget(instructions, alignment=Qt.AlignCenter)

#item 2: current_word
current_word = QLabel("")
current_word.setFont(QFont("Noto Nastaliq Urdu", 75))
current_word.setAlignment(Qt.AlignCenter)
current_word.setContentsMargins(40, 0, 40, 0)  # 40px side padding
layout.addWidget(current_word)

#item 3: spacing between current_word and next button
layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))

#item 4: Next button
next_button = QPushButton("Next")
next_button.setFixedSize(120, 50)
next_button.setStyleSheet("background-color: lightblue; font-size: 18px; font-weight: bold;")
layout.addWidget(next_button, alignment=Qt.AlignCenter)
#---------------------------------------------#


#---------------Define Functions for iterating through words---------------#
#Function that causes each new word to be displayed
def display_next_word():
   global word_num

   if word_num < len(word_list):
       current_word.setText(word_list[word_num])
       word_num+=1
   else:
       next_button.hide()
       current_word.setText("All finished!")

#Function that works the program, triggered whenever the Next button is clicked. Adjusts timer and points. Rationale is that once the Next button is clicked points must first be awarded before moving to next word
def setup_next_word():
    instructions.hide()
    display_next_word()
#---------------------------------------------#

#---------------Execute Script---------------#
next_button.clicked.connect(setup_next_word)
window.setLayout(layout)
window.show()
app.exec_()
#---------------------------------------------#