#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:06:37 2025

@author: gina
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import (
 QApplication, QWidget, QLabel, QPushButton
)
from PyQt5.QtGui import QFont

import pandas as pd
pan_stimuli_df = pd.read_csv("pan_stimuli.csv")  # Read the CSV into a DataFrame
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()



app = QApplication([])




#Wordlist Variables
word_num = 0
word_list = pan_stimuli
#word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]



#Create Window
window = QWidget()
window.setWindowTitle("Phase 0 Window")
window.setGeometry(100,100,800,500)


#Create Main Text Label


current_word = QLabel("Phase 0: Reading", window)
current_word.setFont(QFont("Verdana", 34))
current_word.adjustSize()
current_word.move((window.width()-current_word.width())//2, 100)



#Create Instructions for the first screen only


instructions = QLabel("In this phase, you will see a series of words on the screen. Please silently read each word.", window)
instructions.setFont(QFont("Verdana", 15))
instructions.setWordWrap(True)
instructions.setFixedWidth(400)
instructions.adjustSize()
instructions.move(window.width()//2-instructions.width()//2, 200)




#Create Next Button
next_button = QPushButton("Next", window)
next_button.adjustSize()
next_button.move(window.width()//2-next_button.width()//2, 300)
next_button.setStyleSheet("background-color: lightblue")




#Function that works the program, triggered whenever the Next button is clicked. Adjusts timer and points. Rationale is that once the Next button is clicked points must first be awarded before moving to next word

def setup_next_word():
    global current_word, word_num
    instructions.hide()
    display_next_word()
   
   
#Function that causes each new word to be displayed


def display_next_word():
   global current_word, word_num
  
  
   if word_num < len(word_list):
       current_word.setText(word_list[word_num])
       current_word.setFont(QFont("Verdana", 44))
       current_word.adjustSize()
       current_word.move((window.width()-current_word.width())//2, 200)
       word_num+=1



   else:
       next_button.hide()
       current_word.setText("All finished!")
       current_word.adjustSize()
       current_word.move((window.width()-current_word.width())//2, 200)
  


#Next button triggers the functions, causes the program to run


next_button.clicked.connect(setup_next_word)



window.show()
app.exec_()
