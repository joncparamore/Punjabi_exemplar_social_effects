#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 11:31:18 2025




@author: SteffiK12
"""






#---------------Imports--------------#




import sys, csv, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QColor






import pandas as pd
import random






ato_audio_directory = "2025_pan_AT0"
ak_audio_directory= "2025_pan_AK1"


CSV_FILE = "tokens_shahmukhi_ipa.csv"




#pan_stimuli_df = pd.read_csv("pan_stimuli.csv")  # Read the CSV into a DataFrame
##pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()


eng_stimuli_df = pd.read_csv("eng_test_words.csv")  # Read the CSV into a DataFrame
eng_stimuli = eng_stimuli_df.iloc[:, 0].tolist()


app = QApplication([])





#-----------GET AUDIO FILES-----------#

from collections import defaultdict

dictionary_csv_file = "tokens_shahmukhi_ipa.csv"


# Map the IPA words to Shahmukhi

ipa_to_shahmukhi = {}
with open(dictionary_csv_file, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ipa = row["IPA"].strip()    #Get the IPA column, use .strip to remove extra characters/spaces
        shahmukhi = row[list(reader.fieldnames)[0]].strip()     #Get the corresponding Shahnukhi
        ipa_to_shahmukhi[ipa] = shahmukhi

# Get audio files from both directories and map them back to Shahmukhi
def load_audio_files(directory, source_label):
    audio_entries = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".wav"):              #Go through each folder and get all the audio files
            ipa_audio_name = file_name.split("_")[-1].replace(".wav", "").strip()           #Extract the IPA word from the file
            if ipa_audio_name in ipa_to_shahmukhi:
                shahmukhi = ipa_to_shahmukhi[ipa_audio_name]
                full_path = os.path.join(directory, file_name)
                audio_entries.append((shahmukhi, full_path, source_label))
            else:
                print(f"IPA '{ipa_audio_name}' not found in CSV.")
    return audio_entries

# Load audio from each directory
ak1_words = load_audio_files(ak_audio_directory, "AK1")
ato_words = load_audio_files(ato_audio_directory, "ATO")


random.shuffle(ato_words)
random.shuffle(ak1_words)

block1 = ato_words[:12]
block2 = ak1_words[:12]
block3 = ato_words[12:]  # Remaining 13 words in second block
block4 = ak1_words[12:]  # Remaining 13

#Build Audio Word List with the section headers
audio_word_list = []

audio_word_list += [("Section 1", "ATO")] + block1
audio_word_list += [("Section 2", "AK1")] + block2
audio_word_list += [("Section 3", "ATO")] + block3
audio_word_list += [("Section 4", "AK1")] + block4


audio_word_list += [("Section 5", "ATO")] + block1
audio_word_list += [("Section 6", "AK1")] + block2
audio_word_list += [("Section 7", "ATO")] + block3
audio_word_list += [("Section 8", "AK1")] + block4


audio_word_list += [("Section 9", "ATO")] + block1
audio_word_list += [("Section 10", "AK1")] + block2
audio_word_list += [("Section 11", "ATO")] + block3
audio_word_list += [("Section 12", "AK1")] + block4

audio_word_list += [("Section 13: Missed Words", "Missed Words")]

sound = QSoundEffect()
word_num = 0  





#---------------Wordlist Variables---------------#


'''
word_num = 0


#word_list = pan_stimuli
#word_list = eng_stimuli
word_list = ["ant", "bear", "cat", "dog", "elephant", "flamingo", "goat", "horse", "iguana", "jellyfish", "koala", "lion", "monkey", "narwhal", "orca", "panda", "quail", "rhino"]
random.shuffle(word_list)
'''


word_points_left = 90
feedback_shown = False




#Used to export and keep track of word order
phase3_word_order_list = []




#---------------Create Window---------------#


class MainWindow(QWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showMaximized()

window = MainWindow()

#window = QWidget()
#main_layout = QVBoxLayout(window)






#---------------Define Window Layout---------------#


layout = QVBoxLayout() #automatically stacks and centers items in the center of the space
layout.setAlignment(Qt.AlignCenter)




window.setWindowTitle("Phase 3 Window")
window.setLayout(layout)
window.showFullScreen()








#----------------Get User ID on first screen-------------#




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




#Add the ID elements to a container that way it's easier to make them all disappear
id_container = QWidget(window)
id_layout = QVBoxLayout(id_container)
id_layout.setAlignment(Qt.AlignCenter)




id_layout.addSpacing(200)
id_layout.addWidget(id_label, alignment=Qt.AlignCenter)
id_layout.addSpacing(60)
id_layout.addWidget(id_input, alignment=Qt.AlignCenter)
id_layout.addSpacing(60)
id_layout.addWidget(continue_button,alignment=Qt.AlignCenter)




layout.addWidget(id_container, alignment=Qt.AlignCenter)




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
total_points.hide()
total_points_top_bar = QHBoxLayout()
total_points_top_bar.setContentsMargins(0, 60, 155, 0)  # top, right padding
layout.addLayout(total_points_top_bar)
layout.setAlignment(Qt.AlignTop)


total_points_top_bar.addStretch()   #pushes contents to the right
total_points_top_bar.addWidget(total_points)








point_countdown = QLabel("", window)    #Point countdown box that constantly decreases next to the clock
point_countdown.setAlignment(Qt.AlignCenter)
point_countdown.setFixedSize(200, 80)
point_countdown.setFont(QFont("Verdana", 22))
point_countdown.setStyleSheet("background-color: lightgrey; padding: 20px; border: 2 px; border-radius: 5px")
point_countdown.hide()




#---------------Setup Timer---------------#


timer=QTimer()
timer.setInterval(100)      #Use 1 decisecond = 100 milliseconds
deciseconds_left = 30




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


layout.addSpacerItem(QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Preferred))   #Space from Clock/Point countdown to the point_popup
layout.addWidget(point_popup, alignment=Qt.AlignCenter)
layout.addSpacerItem(QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Preferred))




#---------------Add Images---------------#




#Create a layout that contains both images, that way we can alternate between them later without doing .hide() and .show() which messes with the layout


image_label = QLabel(window)
image_label.setFixedSize(300, 300) 
image_label.setAlignment(Qt.AlignCenter)
image_label.hide()


layout.addWidget(image_label, alignment=Qt.AlignCenter)
layout.addSpacerItem(QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Preferred)) #spacing between point popup and curent word






#---------------Create main text label---------------#




current_word = QLabel("Phase 3: Listen and Respond", window)
current_word.setFont(QFont("Verdana", 45))
current_word.adjustSize()
current_word.setAlignment(Qt.AlignCenter)
current_word.setContentsMargins(40, 0, 40, 0)  # 40px side padding
current_word.hide()


layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred)) #spacing between point popup and curent word
layout.addWidget(current_word, alignment=Qt.AlignCenter)
layout.addSpacerItem(QSpacerItem(0, 200, QSizePolicy.Minimum, QSizePolicy.Preferred))   #Space from Clock/Point countdown to the point_popup




#---------------Create Instructions for the first screen only---------------#


instructions = QLabel("Good work! Thanks to your help in the previous game, Rafiq has learned to read his words, and Dr. Ali has added them to the official Punjabi dictionary. Now, Rafiq and Dr. Ali will each say their words aloud, one at a time. After hearing each word, your task is to repeat it as quickly and clearly as possible to earn points. You will have three seconds to say the word aloud and then click the “Done” button once you finish speaking. When you're ready, click the “Next” button to move on to the next word.", window)
instructions.setFont(QFont("Verdana", 14))
instructions.setStyleSheet("line-height: 150%")
instructions.setWordWrap(True)
instructions.setFixedSize(800,300)
instructions.setAlignment(Qt.AlignCenter)
instructions.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))
layout.addWidget(instructions, alignment=Qt.AlignCenter)


instructions.hide()






#---------------Create Start Button---------------#




start_button = QPushButton("Start", window)
start_button.setFont(QFont("Verdana", 22))
start_button.adjustSize()
start_button.setFixedSize(120, 50)
start_button.setStyleSheet("background-color: lightgreen; font-size: 18px; ")
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


layout.addSpacerItem(QSpacerItem(0, 150, QSizePolicy.Minimum, QSizePolicy.Preferred)) #Adds vertical space between teh Current Word and the done and next buttons
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
  next_word()      #Automatically triggers the first word to appear








#---------------Function to Display Feedback---------------#


#Function that gives feedback to the user after each word (awards points), triggered whenever the Done button is clicked.


def show_feedback():
   global current_word, points, word_num, deciseconds_left, feedback_shown, laborer_image, scholar_image


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
      point_popup.setFont(QFont("Verdana", 30))
      point_popup.adjustSize()
      audio_word_list.append(audio_word_list[word_num])          #To ensure every word is recorded, participant must redo the word at the end of the list
      total_points.setText("Total Points: " + str(points))         #Update the Total Points in the top right corner
      total_points.adjustSize()
      QTimer.singleShot(3000, next_button.show)            #Briefly pause after the points have been displayed to allow for processing, then show Next Button to move on
   elif word_num in (3, 7, 12,18,28,37,54):          #May give random message
      points -=30
      point_countdown.setText("-30  pts")
      point_popup.setText("-30   Alert: Please Speak Clearly")
      point_popup.setWordWrap(True)
      point_popup.setStyleSheet("color: FireBrick")
      point_popup.setFont(QFont("Verdana", 30))
      point_popup.adjustSize()
      total_points.setText("Total Points: " + str(points))
      total_points.adjustSize()
      QTimer.singleShot(3000, next_button.show)
   else:
       points += word_points_left
       point_popup.setFont(QFont("Verdana", 35))
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




#---------------Function that Speaks the Word---------------#


#Function that causes each new word to be displayed after the "Next" button is pressed. Resets the format and shows the new word






def next_word():
   global current_word, points, word_num, deciseconds_left, feedback_shown, laborer_image, scholar_image
   feedback_shown=False
   done_button.setEnabled(False)
   next_button.hide()
   point_popup.setText("")
   deciseconds_left = 30        #reset the clock and the points
   word_points_left = 90
  
   if word_num >= len(audio_word_list):                     #Ending screen that only occurs once all words in the list have been said
        timer.stop()
        clock.hide()
        next_button.hide()
        done_button.hide()
        #laborer_image.show()
        image_label.hide()
        #scholar_image.hide()
        point_countdown.hide()


        current_word.setText("All finished!")
        current_word.setFont(QFont("Verdana", 40))
        current_word.adjustSize()


        total_points.setFont(QFont("Verdana", 24))
        total_points.setStyleSheet("background-color: lightgreen; border: 2 px; padding: 10px; border-radius: 5px")
        total_points.adjustSize()
        layout.addWidget(total_points, alignment=Qt.AlignCenter) 
        layout.addSpacerItem(QSpacerItem(0, 540, QSizePolicy.Minimum, QSizePolicy.Preferred))
        


      
        filename = f"{user_id}_phase3_shadow_word_order.csv"   #Download the .csv of all of the words once you have reached the end of the list
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Shahmukhi Word", "Audio File Path", "Speaker Source"])
            for word in phase3_word_order_list:
               writer.writerow(word)

        return


   #If a section divider has been reached
   elif "Section" in audio_word_list[word_num][0]:
        image_label.hide
        clock.hide()
        point_countdown.hide()
        next_button.hide()
        done_button.hide()
        start_button.show()                     #To move to the next button they click "start" which then runs the same starting function as before to set up for the words
        current_word.setFont(QFont("Verdana", 18))
        current_word.setWordWrap(True)
        current_word.setFixedWidth(2000)
        current_word.adjustSize()
        if "AK1" in audio_word_list[word_num][1]:
           pixmap = QPixmap("laborer.jpg").scaled(300, 300, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
           image_label.setPixmap(pixmap)
           image_label.show()
           current_word.setText(audio_word_list[word_num][0] + " of helping Rafiq is about to begin. Remember, after Rafiq speaks each word, acknowledge the word by clearly saying it back.")
           current_word.show()
        elif "ATO" in audio_word_list[word_num][1]:
           pixmap = QPixmap("scholar.jpg").scaled(250, 250, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
           image_label.setPixmap(pixmap)
           image_label.show()
           current_word.setText(audio_word_list[word_num][0] + " of helping Dr. Ali is about to begin. Remember, after Dr. Ali speaks each word, acknowledge the word by clearly saying it back.")
           current_word.show()
        else:
            image_label.hide()
            current_word.setText(audio_word_list[word_num][0] + " is about to begin. If you ran out of time to say any words, you will have a chance to listen to them and redo them here.")
            current_word.show()

        
        word_num += 1 
        return






   if word_num < len(audio_word_list):
       clock.setText("3.0   sec")                    #Reset the clock, begin the clock on the subsequent line
       point_countdown.setText("90  pts")
       current_word.setText(audio_word_list[word_num][0])        #Do we want to show the word on the screen too?
       current_word.setFont(QFont("Jameel Noori Nastaleeq", 45))
       phase3_word_order_list.append(audio_word_list[word_num])     #output word order into csv for later analysis
       word, path, source = audio_word_list[word_num]
       #phase3_word_order_list.append(word)


       sound.setSource(QUrl.fromLocalFile(path))
       sound.play()


       # Show appropriate image based on source
       if source == "AK1":
           pixmap = QPixmap("laborer.jpg").scaled(300, 300, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
           image_label.setPixmap(pixmap)
           image_label.show()
       elif source == "ATO":
           pixmap = QPixmap("scholar.jpg").scaled(250, 250, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
           image_label.setPixmap(pixmap)
           image_label.show()
  


       def on_audio_finished():        #Only start clock and point countdown after the sound plays
           if not sound.isPlaying():
               done_button.setFont(QFont("Verdana", 22))
               done_button.setStyleSheet("background-color: lightblue; padding: 20px; border: 2 px; border-radius: 5px")        #Reset Done button
               done_button.show()
               timer.start()
               done_button.setEnabled(True)
               sound.playingChanged.disconnect(on_audio_finished)
      
       sound.playingChanged.connect(on_audio_finished)










#---------------Buttons that trigger the program to run---------------#


start_button.clicked.connect(start_program)     #When "Start" is clicked, the GUI sets up to the word configuration (mostly just aesthetic stuff (dis)appearing)
done_button.clicked.connect(show_feedback)      #When "Done" is clicked, signalling the participant has said the word, feedback/points are given
next_button.clicked.connect(next_word)    #When "Next" is clicked, the screen moves on to the next word






window.show()
app.exec_()
