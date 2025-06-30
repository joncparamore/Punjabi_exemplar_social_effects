#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 11:31:18 2025


@author: joncparamore
"""

#Imports
import sys
from PyQt5.QtWidgets import (
   QApplication, QWidget, QLabel, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt


app = QApplication([])

#Wordlist Variables
word_num = 0
word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala"]



#Create Window
window = QWidget()
window.setWindowTitle("Phase 1: Baseline Window")
window.setGeometry(100,100,800,500)

#Create Main Text Label

current_word = QLabel("Phase 1: Baseline Reading", window)
current_word.setFont(QFont("Verdana", 34))
current_word.adjustSize()
current_word.move((window.width()-current_word.width())//2, 100)


#Create Instructions for the first screen only

instructions = QLabel("This phase will test your language speaking abilities. You will see a series of words on the screen. Read each word aloud as fastly and clearly as possible.", window)
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



#Setup Timer
timer=QTimer()
timer.setInterval(100)      #Use 1 decisecond = 100 milliseconds
elapsed_deciseconds = 0

clock = QLabel("", window)
clock.setAlignment(Qt.AlignCenter)
clock.resize(95, 30)  
clock.setFont(QFont("Verdana", 17))
clock.setStyleSheet("background-color: lightgrey; border: 2 px; padding: 6px; border-radius: 5px")
clock.move(window.width()//2-clock.width()//2, 100)
clock.hide()


def update_time():
    global elapsed_deciseconds
    elapsed_deciseconds +=1
    seconds = elapsed_deciseconds / 10
    clock.setText(f"{seconds:01}" + "   sec")


timer.timeout.connect(update_time) #After every decisecond passes, the update_time function is called
actually_timed = False      #Used to make sure the first word times correctly


#Create Points
points = 0
point_popup = QLabel("", window)
point_popup.setAlignment(Qt.AlignCenter)
point_popup.resize(80, 50)  
point_popup.setFont(QFont("Verdana", 25))





#Function that works the program, triggered whenever the Next button is clicked. Adjusts timer and points

def setup_next_word():
    global elapsed_deciseconds, current_word, points, word_num, actual_time
    instructions.hide()
    timer.stop()
    point_popup.move(window.width()//2 + current_word.width()//2+50, 202)
'''
   import random

   #set probability ex: 20%
   probability = 0.20

   #float between 0.0 and 1.0
   if random.random() < probability:
    print("Speak clearer")
    points -= 20
   else:
       pass
   '''
 #May give random message
    random_msg_num = random.randint(1,10)
    if word_num=3 or word_num=4 or word_num = 9 or word_num=22 and actually_timed is True:
        points +=0
        point_popup.setText("+0   Please Speak Clearly")
        point_popup.setStyleSheet("color: FireBrick")
        QTimer.singleShot(1000, display_next_word) 
    elif elapsed_deciseconds<12 and actually_timed is True:
            points += 50
            point_popup.setText("+50")
            point_popup.setStyleSheet("color:green")
            QTimer.singleShot(1000, display_next_word) 
    elif elapsed_deciseconds<20 and actually_timed is True:
            points += 20
            point_popup.setText("+20")
            point_popup.setStyleSheet("color:DarkOliveGreen")
            QTimer.singleShot(1000, display_next_word) 
    elif elapsed_deciseconds<30 and actually_timed is True:
            points += 5
            point_popup.setText("+5")
            point_popup.setStyleSheet("color: DarkGoldenrod")
            QTimer.singleShot(1000, display_next_word) 
    elif actually_timed is True:
            points += 0
            point_popup.setText("+0")
            point_popup.setStyleSheet("color: FireBrick")
            QTimer.singleShot(1000, display_next_word) 
    else:
        display_next_word()
    

#Function that causes each new word to be displayed

def display_next_word():
    point_popup.setText("")
    global elapsed_deciseconds, current_word, points, word_num, actually_timed
    elapsed_deciseconds=0
    
    
    if word_num < len(word_list):
        current_word.setText(word_list[word_num]) 
        current_word.setFont(QFont("Verdana", 44))
        current_word.adjustSize()
        current_word.move((window.width()-current_word.width())//2, 200)
        word_num+=1

        clock.show()
        clock.setText("0.0   sec")
        timer.start()
        actually_timed = True

    else:
        timer.stop()
        clock.hide()
        next_button.hide()
        current_word.setText("All finished!")
        current_word.adjustSize()
        current_word.move((window.width()-current_word.width())//2, 200)
        window.final_points = QLabel("Total Points: " + str(points),window)
        window.final_points.setFont(QFont("Verdana", 17))
        window.final_points.setStyleSheet("background-color: lightgreen; border: 2 px; padding: 6px; border-radius: 5px")
        window.final_points.adjustSize()
        window.final_points.move((window.width()-window.final_points.width())//2, 100)
        window.final_points.show()


    

#Next button triggers the functions, causes the program to run

next_button.clicked.connect(setup_next_word)



window.show()
app.exec_()


