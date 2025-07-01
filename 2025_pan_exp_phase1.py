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
word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]
word_points_left = 50


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



#Create Points


points = 0

point_countdown = QLabel("", window) #Point countdown box that constantly decreases next to the clock
point_countdown.setAlignment(Qt.AlignCenter)
point_countdown.resize(95, 30) 
point_countdown.setFont(QFont("Verdana", 17))
point_countdown.setStyleSheet("background-color: lightgrey; border: 2 px; padding: 6px; border-radius: 5px")
point_countdown.move(430, 100)
point_countdown.hide()


point_popup = QLabel("", window)    #Point popup text that appears after clicking "next"
point_popup.setAlignment(Qt.AlignCenter)
point_popup.resize(80, 50) 
point_popup.setFont(QFont("Verdana", 25))



#Setup Timer
timer=QTimer()
timer.setInterval(100)      #Use 1 decisecond = 100 milliseconds
elapsed_deciseconds = 0



clock = QLabel("", window)
clock.setAlignment(Qt.AlignCenter)
clock.resize(95, 30) 
clock.setFont(QFont("Verdana", 17))
clock.setStyleSheet("background-color: lightgrey; border: 2 px; padding: 6px; border-radius: 5px")
clock.move(270, 100)
clock.hide()



def update_time():
   global elapsed_deciseconds, word_points_left
   elapsed_deciseconds +=1
   seconds = elapsed_deciseconds / 10
   word_points_left = 50 - elapsed_deciseconds
   point_countdown.setText(f"{word_points_left:01}" + "   pts")
   clock.setText(f"{seconds:01}" + "   sec")




timer.timeout.connect(update_time) #After every decisecond passes, the update_time function is called
actually_timed = False      #Used for the sole purpose of making sure the first word doesn't display feedback yet



#Function that works the program, triggered whenever the Next button is clicked. Adjusts timer and points. Rationale is that once the Next button is clicked points must first be awarded before moving to next word

def setup_next_word():
    global elapsed_deciseconds, current_word, points, word_num, actual_time, point_popup, word_points_left
    point_countdown.show()
    instructions.hide()
    timer.stop()            #When Next button is pressed, stop the timer so we know how long it took
             
    if word_num in (3, 7, 11,18,28,54) and actually_timed is True:          #May give random message
       points -=10
       point_popup.setText("-10   Alert: Please Speak Clearly")
       point_popup.setWordWrap(True)
       point_popup.setStyleSheet("color: FireBrick")
       point_popup.setFont(QFont("Verdana", 20))
       point_popup.adjustSize()
       QTimer.singleShot(3000, display_next_word)
    elif actually_timed is True:
        points += word_points_left
        point_popup.setFont(QFont("Verdana", 25))
        point_popup.setText("+" + f"{word_points_left}")
        point_popup.adjustSize()
        point_popup.move(window.width()//2 + current_word.width()//2+50, 202)
        point_popup.setWordWrap(False)
        if word_points_left>0:
            point_popup.setText("+" + f"{word_points_left}")
            if  word_points_left>35:
                point_popup.setStyleSheet("color:green")
            elif word_points_left>25:
                point_popup.setStyleSheet("color:DarkOliveGreen")
            elif word_points_left>15:
                point_popup.setStyleSheet("color:DarkGoldenrod")
            else:
                point_popup.setStyleSheet("color: DarkSalmon")
        else:
            point_popup.setText(f"{word_points_left}")
            point_popup.setStyleSheet("color: Firebrick")
       
        QTimer.singleShot(1000, display_next_word)
    else:
        display_next_word()
   
   
#Function that causes each new word to be displayed


def display_next_word():
   global elapsed_deciseconds, current_word, points, word_num, actually_timed
   point_popup.setText("")
   elapsed_deciseconds=0
   word_points_left = 50
  
  
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
       point_countdown.hide()
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




