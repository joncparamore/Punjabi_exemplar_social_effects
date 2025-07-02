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
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy


import pandas as pd
import random

pan_stimuli_df = pd.read_csv("pan_stimuli.csv")  # Read the CSV into a DataFrame
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()
random.shuffle(pan_stimuli)

app = QApplication([])



#Wordlist Variables
word_num = 0
#word_list = pan_stimuli
word_points_left = 60
word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]




#Create Window
window = QWidget()
main_layout = QVBoxLayout(window)
window.setWindowTitle("Phase 1: Baseline Window")


screen_geometry = app.primaryScreen().geometry()
screen_width = screen_geometry.width()
screen_height = screen_geometry.height()


window.setGeometry(0, 0, screen_width, screen_height)



#Create Main Text Label


current_word = QLabel("Phase 1: Baseline Reading", window)
current_word.setFont(QFont("Verdana", 50))
current_word.adjustSize()
current_word.move((window.width()-current_word.width())//2, 240)



#Create Instructions for the first screen only

instructions = QLabel("This phase will test your language speaking abilities. You will see a series of words on the screen. Read each word aloud as quickly and clearly as possible to earn points. You will have 2 seconds to read each word aloud and click the 'Done' button after you are finished speaking. Click the 'Next' button to move onto the next word", window)
instructions.setFont(QFont("Verdana", 20))
instructions.setStyleSheet("line-height: 150%") 
instructions.setWordWrap(True)
instructions.setFixedWidth(600)
instructions.adjustSize()
instructions.move(window.width()//2-instructions.width()//2, 380)


#Create Start Button
start_button = QPushButton("Start", window)
start_button.setFont(QFont("Verdana", 22))
start_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")
start_button.adjustSize()
start_button.move(window.width()//2-start_button.width()//2, 600)


#Create Done Button
done_button = QPushButton("Done", window)
done_button.setFont(QFont("Verdana", 22))
done_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")
done_button.adjustSize()
done_button.hide()


#Create Next Button
next_button = QPushButton("Next", window)
next_button.setFont(QFont("Verdana", 22))
next_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")
next_button.adjustSize()
next_button.hide()


#Button Layout. Purpose is so that the buttons can dynamically move positions to stay centered. The "Done" button will be centered when by itself, and remain centered once the "Next" button appears to the right

button_container = QWidget(window) #Create a container with just the Done and Next buttons 
button_layout = QHBoxLayout(button_container)       #Add it to a Horizontal Layout
button_layout.setSpacing(60)                    #Create a 60 px space between the buttons


button_layout.addStretch()
button_layout.addWidget(done_button)        # Add buttons to the layout
button_layout.addWidget(next_button)
button_layout.addStretch()

main_layout.addSpacerItem(QSpacerItem(0, 400, QSizePolicy.Fixed, QSizePolicy.Fixed)) #Adds vertical space above the buttons so they are 400 pixels from top of screen
main_layout.addWidget(button_container, alignment=Qt.AlignCenter)                   #Causes the container of buttons to be centrally aligned


#Create Points

points = 0

point_countdown = QLabel("", window)    #Point countdown box that constantly decreases next to the clock
point_countdown.setAlignment(Qt.AlignCenter)
point_countdown.resize(135, 66)
point_countdown.setFont(QFont("Verdana", 22))
point_countdown.setStyleSheet("background-color: lightgrey; padding: 20px; border: 2 px; border-radius: 5px")
point_countdown.move(window.width() // 2 + 80, 180)
point_countdown.hide()


point_popup = QLabel("", window)    #Point popup text that appears after clicking "next"
point_popup.setAlignment(Qt.AlignCenter)


total_points = QLabel("Total Points: " + str(points),window)
total_points.setFont(QFont("Verdana", 22))
total_points.setStyleSheet("color:DarkSlateGray")
total_points.adjustSize()
total_points.move(window.width()-250, 80)



#Setup Timer
timer=QTimer()
timer.setInterval(100)      #Use 1 decisecond = 100 milliseconds
deciseconds_left = 20


clock = QLabel("", window)
clock.setAlignment(Qt.AlignCenter)
clock.setFont(QFont("Verdana", 22))
clock.setStyleSheet("background-color: lightgrey; border: 2 px; padding: 20px; border-radius: 5px")
clock.resize(135, 66)
clock.move(window.width() // 2 - 200, 180)
clock.hide()


def update_time():
   global word_points_left, deciseconds_left, points
   deciseconds_left -=1
   seconds_left = deciseconds_left/10
   word_points_left = 3*deciseconds_left
   point_countdown.setText(f"{word_points_left:01}" + "   pts")
   clock.setText(f"{seconds_left:01}" + "   sec")


   if deciseconds_left<=0:         #If time runs out, this is the only function that is constantly keeping track of time. It stops the timer
       timer.stop()
       word_list.append(word_list[word_num-1])          #To ensure every word is recorded, participant must redo the word at the end of the list
       show_feedback()           #If time runs out, trigger the function that awards points, as if automatically pushing the "Done" button


timer.timeout.connect(update_time) #After every decisecond passes, the update_time function is called


#function that runs when the "Start" button is pressed. Simply reconfigures the GUI for aethetic reasons (like removing instructions, adding the clock)

def start_program():
   instructions.hide()
   start_button.hide()
   point_countdown.show()
   clock.show()
   done_button.show()
   display_next_word()      #Automatically triggers the first word to appear



#Function that gives feedback to the user after each word (awards points), triggered whenever the Done button is clicked. 

def show_feedback():
   global current_word, points, word_num, point_popup, word_points_left, deciseconds_left
   done_button.setFont(QFont("Verdana", 22))
   done_button.setStyleSheet("background-color: lightgrey; padding: 20px; border: 2 px; border-radius: 5px")        #Fade out the Done button
   timer.stop()            #When Done button is pressed, stop the timer so we know how long it took
   if deciseconds_left <= 0:
       points -=30
       point_countdown.setText("-30  pts")
       point_popup.setText("-30  Out of Time")
       point_popup.setStyleSheet("color: FireBrick")
       point_popup.setFont(QFont("Verdana", 30))
       point_popup.adjustSize()
       point_popup.move(window.width()//2 + current_word.width()//2+120, 350)       
       total_points.setText("Total Points: " + str(points))         #Update the Total Points in the top right corner
       total_points.adjustSize()
       QTimer.singleShot(2000, next_button.show)            #Briefly pause after the points have been displayed to allow for processing, then show Next Button to move on
   elif word_num in (3, 7, 12,18,28,37,54):          #May give random message
       points -=30
       point_countdown.setText("-30  pts")
       point_popup.setText("-30   Alert: Please Speak Clearly")
       point_popup.setWordWrap(True)
       point_popup.setStyleSheet("color: FireBrick")
       point_popup.setFont(QFont("Verdana", 30))
       point_popup.move(window.width()//2 + current_word.width()//2+120, 350)
       point_popup.adjustSize()
       total_points.setText("Total Points: " + str(points))
       total_points.adjustSize()
       QTimer.singleShot(2000, next_button.show)
   else:
        points += word_points_left
        point_popup.setFont(QFont("Verdana", 40))
        point_popup.move(window.width()//2 + current_word.width()//2+100, 370)
        point_popup.setText("+" + f"{word_points_left}")
        point_popup.adjustSize()
        if  word_points_left>30:
           point_popup.setStyleSheet("color:green")
        elif  word_points_left>20:
           point_popup.setStyleSheet("color:DarkOliveGreen")
        elif word_points_left>10:
           point_popup.setStyleSheet("color:DarkGoldenrod")
        elif word_points_left>0:
           point_popup.setStyleSheet("color:#CC6600")
        total_points.setText("Total Points: " + str(points))
        total_points.adjustSize()
        QTimer.singleShot(1000, next_button.show)

 
 
#Function that causes each new word to be displayed after the "Next" button is pressed. Resets the format and shows the new word


def display_next_word():
    global current_word, points, word_num, deciseconds_left
    done_button.show()
    done_button.setFont(QFont("Verdana", 22))
    done_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")        #Reset Done button
    next_button.hide()
    point_popup.setText("")
    deciseconds_left = 20
    word_points_left = 60
  
    if word_num < len(word_list):                                   #if we are still in the bounds of the list
      current_word.setText(word_list[word_num])
      current_word.setFont(QFont("Verdana", 110))
      current_word.adjustSize()
      current_word.move((window.width()-current_word.width())//2, 360)
      word_num+=1


      clock.setText("0.0   sec")                    #Reset the clock, begin the clock on the subsequent line
      timer.start()


    else:                        #Ending screen that only occurs once all words in the list have been said
      timer.stop()
      clock.hide()
      next_button.hide()
      done_button.hide()
      point_countdown.hide()
      total_points.hide()

      current_word.setText("All finished!")
      current_word.setFont(QFont("Verdana", 60))
      current_word.adjustSize()
      current_word.move((window.width()-current_word.width())//2, 360)
      window.final_points = QLabel("Total Points: " + str(points),window)
      window.final_points.setFont(QFont("Verdana", 24))
      window.final_points.setStyleSheet("background-color: lightgreen; border: 2 px; padding: 10px; border-radius: 5px")
      window.final_points.adjustSize()
      window.final_points.move((window.width()-window.final_points.width())//2, 200)
      window.final_points.show()




###Buttons that trigger the program to run###

start_button.clicked.connect(start_program)     #When "Start" is clicked, the GUI sets up to the word configuration (mostly just aesthetic stuff (dis)appearing)
done_button.clicked.connect(show_feedback)      #When "Done" is clicked, signalling the participant has said the word, feedback/points are given
next_button.clicked.connect(display_next_word)    #When "Next" is clicked, the screen moves on to the next word




window.show()
app.exec_()

