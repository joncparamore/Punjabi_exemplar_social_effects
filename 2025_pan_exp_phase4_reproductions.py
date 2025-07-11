#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 11:31:18 2025


@author: joncparamore
"""




#---------------Imports--------------#

import sys
import csv


from PyQt5.QtWidgets import (
QApplication, QWidget, QLabel, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QLineEdit

import pandas as pd
import random

pan_stimuli_df = pd.read_csv("pan_stimuli.csv")  # Read the CSV into a DataFrame
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()

eng_stimuli_df = pd.read_csv("eng_test_words.csv")  # Read the CSV into a DataFrame
eng_stimuli = eng_stimuli_df.iloc[:, 0].tolist()


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

app = QApplication([])


#---------------Wordlist Variables---------------#


word_num = 0

word_list = pan_stimuli
#word_list = eng_stimuli
#word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]
random.shuffle(word_list)


word_points_left = 60
feedback_shown = False


#Used to export and keep track of word order
phase4_word_order_list = []


#---------------Create Window---------------#

class MainWindow(QWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showMaximized()

window = MainWindow()

#main_layout = QVBoxLayout(window)



#---------------Define Window Layout---------------#

layout = QVBoxLayout() #automatically stacks and centers items in the center of the space
layout.setAlignment(Qt.AlignCenter) 


window.setWindowTitle("Phase 4 Window")
window.setLayout(layout)
window.showFullScreen()


#----------------Get User ID on prior screen-------------#


user_id = "participant"     #variable to store it

id_label = QLabel("Please enter your Name or ID to begin:", window)
id_label.setFont(QFont("Verdana", 24))
id_label.setAlignment(Qt.AlignCenter)

id_input = QLineEdit(window)
id_input.setFont(QFont("Verdana", 20))
id_input.setFixedWidth(400)
id_input.setPlaceholderText("e.g., jsmith123")
id_input.setAlignment(Qt.AlignCenter)

continue_button = QPushButton("Continue", window)
continue_button.setFont(QFont("Verdana", 22))
continue_button.setFixedSize(180, 50)
continue_button.setStyleSheet("background-color: lightgreen; font-size: 18px;")


# Container widget and layout for centering
id_container = QWidget(window)
id_layout = QVBoxLayout(id_container)
id_layout.setAlignment(Qt.AlignCenter)


id_layout.addSpacing(200)
id_layout.addWidget(id_label, alignment=Qt.AlignCenter)
id_layout.addSpacing(60)
id_layout.addWidget(id_input, alignment=Qt.AlignCenter)
id_layout.addSpacing(60)
id_layout.addWidget(continue_button,alignment=Qt.AlignCenter)


layout.addStretch() 
layout.addWidget(id_container, alignment=Qt.AlignCenter)
layout.addStretch() 


def proceed_to_main_window():
    global user_id
    entered_id = id_input.text().strip()
    if entered_id:
        user_id = entered_id
        layout.removeWidget(id_container)
        id_container.deleteLater()  
        instructions.show()
        current_word.show()
        start_button.show()   
    else:     
        return

continue_button.clicked.connect(proceed_to_main_window)


#---------------Create Points---------------#


points = 0


total_points = QLabel("Total Points: " + str(points),window)
total_points.setFont(QFont("Verdana", 22))
total_points.setStyleSheet("color:DarkSlateGray")
total_points.adjustSize()

total_points_top_bar = QHBoxLayout()
total_points_top_bar.setContentsMargins(0, 60, 155, 0)  # top, right padding
layout.addLayout(total_points_top_bar)
layout.setAlignment(Qt.AlignTop)

total_points_top_bar.addStretch()   #pushes contents to the right
total_points_top_bar.addWidget(total_points)
total_points.hide()




point_countdown = QLabel("", window)    #Point countdown box that constantly decreases next to the clock
point_countdown.setAlignment(Qt.AlignCenter)
point_countdown.setFixedSize(200, 80)
point_countdown.setFont(QFont("Verdana", 22))
point_countdown.setStyleSheet("background-color: lightgrey; padding: 20px; border: 2 px; border-radius: 5px")
point_countdown.hide()


#---------------Setup Timer---------------#

timer=QTimer()
timer.setInterval(100)      #Use 1 decisecond = 100 milliseconds
deciseconds_left = 20


clock = QLabel("", window)
clock.setAlignment(Qt.AlignCenter)
clock.setFont(QFont("Verdana", 22))
clock.setStyleSheet("background-color: lightgrey; border: 2 px; padding: 20px; border-radius: 5px")
clock.setFixedSize(200, 80)
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
       show_feedback()           #If time runs out, trigger the function that awards points, as if automatically pushing the "Done" button


timer.timeout.connect(update_time) #After every decisecond passes, the update_time function is called



#---------------Clock and Point Countown Layout---------------#


#Clock and Point are at the same vertical level, so added to the same horizontal layout

clock_point_container = QWidget(window) 
clock_point_layout = QHBoxLayout(clock_point_container)       #Add it to a Horizontal Layout
clock_point_layout.setSpacing(60)                    #Create a 60 px space between the Clock and Point Countdown


clock_point_layout.addStretch()
clock_point_layout.addWidget(clock)        # Add to the layout
clock_point_layout.addWidget(point_countdown)
clock_point_layout.addStretch()

layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))      #Space from top of screen to Clock/Point Countdown
layout.addWidget(clock_point_container, alignment=Qt.AlignCenter)                   #Causes the container of buttons to be centrally aligned


#---------------Point Popup Text---------------#



point_popup = QLabel("", window)    #Point popup text that appears after clicking "next"
point_popup.setFixedSize(2000, 80)
point_popup.setAlignment(Qt.AlignCenter)

layout.addSpacerItem(QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Preferred))   #Space from Clock/Point countdown to the point_popup
layout.addWidget(point_popup, alignment=Qt.AlignCenter)



#---------------Create main text label---------------#


current_word = QLabel("Phase 4: Read Aloud", window)
current_word.setFont(QFont("Verdana", 50))
current_word.setAlignment(Qt.AlignCenter)
current_word.setContentsMargins(40, 0, 40, 0)  # 40px side padding
current_word.adjustSize()
current_word.hide()

layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred)) #spacing between point popup and curent word 
layout.addWidget(current_word)



#---------------Create Instructions for the first screen only---------------#

instructions = QLabel("The following game will test your fluency in Punjabi. You will see a series of Punjabi words on the screen. Read each word aloud as quickly and clearly as possible to earn points. You will have 2 seconds to read each word aloud and click the 'Done' button after you are finished speaking. Click the 'Next' button to move onto the next word", window)
instructions.setFont(QFont("Verdana", 20))
instructions.setStyleSheet("line-height: 150%") 
instructions.setWordWrap(True)
instructions.setFixedSize(800,300)
instructions.setAlignment(Qt.AlignCenter)
instructions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
instructions.hide()
layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))
layout.addWidget(instructions, alignment=Qt.AlignCenter)





#---------------Create Start Button---------------#


start_button = QPushButton("Start", window)
start_button.setFont(QFont("Verdana", 22))
start_button.adjustSize()
start_button.setFixedSize(120, 50)
start_button.setStyleSheet("background-color: lightblue; font-size: 18px; ")
layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))
layout.addWidget(start_button, alignment=Qt.AlignCenter)
start_button.hide()


#---------------Create Done Button---------------#
done_button = QPushButton("Done", window)
done_button.setFont(QFont("Verdana", 22))
done_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")
done_button.adjustSize()
done_button.hide()


#---------------Create Next Button---------------#
next_button = QPushButton("Next", window)
next_button.setFont(QFont("Verdana", 22))
next_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")
next_button.adjustSize()
next_button.hide()


#---------------Done and Next Button Layout---------------#

#Button Layout. Purpose is so that the buttons can dynamically move positions to stay centered. The "Done" button will be centered when by itself, and remain centered once the "Next" button appears to the right


button_container = QWidget(window)     #Create a container with just the Done and Next buttons 
button_layout = QHBoxLayout(button_container)       #Add it to a Horizontal Layout
button_layout.setSpacing(60)                    #Create a 60 px space between the buttons


button_layout.addStretch()
button_layout.addWidget(done_button)        # Add buttons to the layout
button_layout.addWidget(next_button)
button_layout.addStretch()

layout.addSpacerItem(QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Preferred)) #Adds vertical space between teh Current Word and the done and next buttons
layout.addWidget(button_container, alignment=Qt.AlignCenter)                   #Causes the container of buttons to be centrally aligned

layout.addSpacerItem(QSpacerItem(0, 250, QSizePolicy.Minimum, QSizePolicy.Preferred))     #Adds space at bottom of screen underneath the Done and Next Buttons




#---------------Function to Start the Program---------------#

#function that runs when the "Start" button is pressed. Simply reconfigures the GUI for aethetic reasons (like removing instructions, adding the clock)

def start_program():
   instructions.hide()
   start_button.hide()
   point_countdown.show()
   clock.show()
   done_button.show()
   total_points.show()
   display_next_word()      #Automatically triggers the first word to appear




#---------------Function to Display Feedback---------------#

#Function that gives feedback to the user after each word (awards points), triggered whenever the Done button is clicked. 

def show_feedback():
   global current_word, points, word_num, point_popup, word_points_left, deciseconds_left, feedback_shown
   
   phase4_word_order_list.append(word_list[word_num])     #output word order into csv for later analysis
   
   done_button.setEnabled(False)
   if feedback_shown is True:
        return  # Prevent double execution where a user clicks "Done" multiple times
   else:   
         feedback_shown = True  
   
   done_button.setFont(QFont("Verdana", 22))
   done_button.setStyleSheet("background-color: lightgrey; padding: 20px; border: 2 px; border-radius: 5px")        #Fade out the Done button
   timer.stop()            #When Done button is pressed, stop the timer so we know how long it took
   
   if deciseconds_left <= 0:
       points -=30
       point_countdown.setText("-30  pts")
       point_popup.setText("-30  Out of Time")
       point_popup.setStyleSheet("color: FireBrick")
       point_popup.setFont(QFont("Verdana", 35))
       point_popup.adjustSize()
       word_list.append(word_list[word_num])          #To ensure every word is recorded, participant must redo the word at the end of the list
 
       total_points.setText("Total Points: " + str(points))         #Update the Total Points in the top right corner
       total_points.adjustSize()
       QTimer.singleShot(3000, next_button.show)            #Briefly pause after the points have been displayed to allow for processing, then show Next Button to move on
   elif word_num in (3, 7, 12,18,28,37,54):          #May give random message
       points -=30
       point_countdown.setText("-30  pts")
       point_popup.setText("-30   Alert: Please Speak Clearly")
       point_popup.setWordWrap(True)
       point_popup.setStyleSheet("color: FireBrick")
       point_popup.setFont(QFont("Verdana", 35))
       point_popup.adjustSize()
       total_points.setText("Total Points: " + str(points))
       total_points.adjustSize()
       QTimer.singleShot(3000, next_button.show)
   else:
        points += word_points_left
        point_popup.setFont(QFont("Verdana", 40))
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
        QTimer.singleShot(2000, next_button.show)
     
     
     
   #After showing feedback, increase the index to trigger the next word in the list
     
   word_num+=1

 
 

 #---------------Function to Display Next Word---------------#
#Function that causes each new word to be displayed after the "Next" button is pressed. Resets the format and shows the new word


def display_next_word():
    global current_word, points, word_num, deciseconds_left, feedback_shown
    feedback_shown=False
    done_button.setEnabled(True)
    done_button.show()
    done_button.setFont(QFont("Verdana", 22))
    done_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")        #Reset Done button
    next_button.hide()
    point_popup.setText("")
    deciseconds_left = 20        #reset the clock and the points
    word_points_left = 60
  
    if word_num < len(word_list):                                   #if we are still in the bounds of the list
      current_word.setText(word_list[word_num])
      current_word.setFont(QFont("Jameel Noori Nastaleeq", 80))
      current_word.adjustSize()

      clock.setText("2.0   sec")                    #Reset the clock, begin the clock on the subsequent line
      timer.start()


    else:                        #Ending screen that only occurs once all words in the list have been said
      timer.stop()
      clock.hide()
      next_button.hide()
      done_button.hide()
      point_countdown.hide()

      current_word.setText("All finished!")
      current_word.setFont(QFont("Verdana", 60))
      current_word.adjustSize()

      total_points.setFont(QFont("Verdana", 24))
      total_points.setStyleSheet("background-color: lightgreen; border: 2 px; padding: 10px; border-radius: 5px")
      total_points.adjustSize()
      layout.addWidget(total_points, alignment=Qt.AlignCenter)  
      layout.addSpacerItem(QSpacerItem(0, 540, QSizePolicy.Minimum, QSizePolicy.Preferred)) 

      filename = f"{user_id}_phase4_reproductions_word_order.csv"   #Download the .csv of all of the words once you have reached the end of the list
      with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for word in phase4_word_order_list:
                writer.writerow([word])






#---------------Buttons that trigger the program to run---------------#

start_button.clicked.connect(start_program)     #When "Start" is clicked, the GUI sets up to the word configuration (mostly just aesthetic stuff (dis)appearing)
done_button.clicked.connect(show_feedback)      #When "Done" is clicked, signalling the participant has said the word, feedback/points are given
next_button.clicked.connect(display_next_word)    #When "Next" is clicked, the screen moves on to the next word


window.showFullScreen()
window.show()
app.exec_()
