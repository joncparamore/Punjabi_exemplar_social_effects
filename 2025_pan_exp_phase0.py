#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:06:37 2025
@author: gina
"""

#---------------Import Packages---------------#
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import random
import csv
#---------------------------------------------#

#---------------Import Stimuli and Shuffle Order---------------#
pan_stimuli_df = pd.read_csv("pan_stimuli.csv")
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()
random.shuffle(pan_stimuli)

# Wordlist Variables
word_num = 0
word_list = pan_stimuli
#word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]
random.shuffle(word_list)

#---------------------------------------------#

#---------------Initialize app and window---------------#
app = QApplication([])
window = QWidget()
window.setWindowTitle("Warmup")
window.showFullScreen()
#---------------------------------------------#

#---------------Define Window Layout---------------#
layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)

#Used to export and keep track of word order
phase0_word_order_list = []


# Instructions label
instructions = QLabel("In this phase, you will see a series of Punjabi words on the screen. Please silently read each word to ensure you are familiar with each one.")
instructions.setFont(QFont("Verdana", 20))
instructions.setWordWrap(True)
instructions.setAlignment(Qt.AlignCenter)
instructions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
layout.addWidget(instructions, alignment=Qt.AlignCenter)

# Word display label
current_word = QLabel("")
current_word.setFont(QFont("Noto Nastaliq Urdu", 75))
current_word.setAlignment(Qt.AlignCenter)
current_word.setContentsMargins(40, 0, 40, 0)
current_word.hide()  # hide on start
layout.addWidget(current_word)

# Spacer
layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))

# Start button
start_button = QPushButton("Start")
start_button.setFixedSize(140, 60)
start_button.setStyleSheet("background-color: lightgreen; font-size: 20px; font-weight: bold;")
layout.addWidget(start_button, alignment=Qt.AlignCenter)

# Space out back and next buttons
button_layout = QHBoxLayout()
button_layout.setSpacing(60)  # Set the gap between the buttons
button_layout.setAlignment(Qt.AlignCenter)  # Center the whole group

# Back button
back_button = QPushButton("Back")
back_button.setFixedSize(120, 50)
back_button.setStyleSheet("background-color: lightgray; font-size: 18px; font-weight: bold;")
back_button.hide()
button_layout.addWidget(back_button)

# Next button
next_button = QPushButton("Next")
next_button.setFixedSize(120, 50)
next_button.setStyleSheet("background-color: lightblue; font-size: 18px; font-weight: bold;")
next_button.hide()
button_layout.addWidget(next_button)

layout.addLayout(button_layout)
#---------------------------------------------#

#---------------Functions to Show Words---------------#
def display_next_word():
    global word_num
    total_words = len(word_list)

    if word_num < total_words:
        current_word.setText(word_list[word_num])
        phase0_word_order_list.append(word_list[word_num])     #output word order into csv for later analysis
   
        word_num += 1
        
        back_button.show()
        next_button.show()

        if word_num == total_words:
            next_button.setText("Finish")
            next_button.setStyleSheet("background-color: lightgreen; font-size: 18px; font-weight: bold;")
        else:
            next_button.setText("Next")
            next_button.setStyleSheet("background-color: lightblue; font-size: 18px; font-weight: bold;")
    else:
        current_word.setText("All done!")
        back_button.hide()
        next_button.hide()


        with open('phase0_warmup_word_order.csv', 'w', newline='') as file:      #Download the .csv of all of the words once you have reached the end of the list
            writer = csv.writer(file)
            for word in phase0_word_order_list:
                writer.writerow([word])

def start_experiment():
    instructions.hide()
    start_button.hide()
    current_word.show()
    display_next_word()

def setup_next_word():
    display_next_word()

def setup_previous_word():
    global word_num
    if word_num > 1:
        word_num -= 2
    elif word_num == 1:
        word_num -= 1
    display_next_word()
#---------------------------------------------#

#---------------Connect Buttons---------------#
start_button.clicked.connect(start_experiment)
next_button.clicked.connect(setup_next_word)
back_button.clicked.connect(setup_previous_word)

#---------------Run Application---------------#
window.setLayout(layout)
window.show()
app.exec_()
#---------------------------------------------#
