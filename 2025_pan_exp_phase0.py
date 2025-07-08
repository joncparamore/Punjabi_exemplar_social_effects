#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:06:37 2025
@author: gina
"""

#---------------Import Packages---------------#
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import pandas as pd
import random
import csv

#---------------Import Stimuli and Shuffle Order---------------#
pan_stimuli_df = pd.read_csv("pan_stimuli.csv")
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()

random.shuffle(pan_stimuli)

# Wordlist Variables
word_num = 0
word_list = pan_stimuli
random.shuffle(word_list)

#---------------Initialize app and window---------------#
app = QApplication([])
window = QWidget()
window.setWindowTitle("Warmup")
window.showFullScreen()

layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)
window.setLayout(layout)

#---------------Global Storage---------------#
phase0_word_order_list = []
demographic_data = {
    "name": "", "age": "", "sex": "", "native_lang": "",
    "langs_spoken": [], "birthplace": "", "currenttown": "",
    "speaker_id": "", "grew_up": "", "punjabi_use": "",
    "profession": "", "education": "", "father_profession": ""
}
user_id = "participant"

#---------------Helper: Clear Layout---------------#
def clear_layout():
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()

#---------------User ID Screen---------------#
def show_user_id_screen():
    clear_layout()

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

    def proceed():
        global user_id
        entered_id = id_input.text().strip()
        if entered_id:
            user_id = entered_id
            show_demographic_form_page1()
        else:
            QMessageBox.warning(window, "Missing ID", "Please enter a valid name or ID.")

    continue_button.clicked.connect(proceed)

    #layout for user id
    layout.addSpacing(200)
    layout.addWidget(id_label, alignment=Qt.AlignCenter)
    layout.addSpacing(60)
    layout.addWidget(id_input, alignment=Qt.AlignCenter)
    layout.addSpacing(60)
    layout.addWidget(continue_button, alignment=Qt.AlignCenter)

#---------------Demographics Page 1---------------#
def show_demographic_form_page1():
    clear_layout()

    #dropdown options
    years = [str(x) for x in range(1930, 2010)]
    languages = ['Punjabi', 'Urdu', 'English', 'Mankiyali', 'Pashto', 'Saraiki', 'Hindko', 'Sindhi', 'Balochi', 'Other']
    genders = ['male', 'female']

    #input widgets
    name_input = QLineEdit()
    age_input = QComboBox(); age_input.addItems(years)
    sex_input = QComboBox(); sex_input.addItems(genders)
    natlang_input = QComboBox(); natlang_input.addItems(languages)

    langs_input = QListWidget()
    langs_input.setSelectionMode(QListWidget.MultiSelection)
    for lang in languages:
        langs_input.addItem(QListWidgetItem(lang))

    birth_input = QLineEdit()
    current_input = QLineEdit()

    #layout for page 1
    layout.addWidget(QLabel("Enter your full name:")); layout.addWidget(name_input)
    layout.addWidget(QLabel("Year of birth:")); layout.addWidget(age_input)
    layout.addWidget(QLabel("Sex:")); layout.addWidget(sex_input)
    layout.addWidget(QLabel("Native language:")); layout.addWidget(natlang_input)
    layout.addWidget(QLabel("Languages you speak:")); layout.addWidget(langs_input)
    layout.addWidget(QLabel("City/town where you were born:")); layout.addWidget(birth_input)
    layout.addWidget(QLabel("City/town where you currently live:")); layout.addWidget(current_input)

    next_button = QPushButton("Next")
    next_button.setStyleSheet("background-color: lightgreen; font-size: 18px; font-weight: bold;")
    layout.addWidget(next_button)

    #next button
    def handle_next():
        selected_langs = [item.text() for item in langs_input.selectedItems()]
        if "Other" in selected_langs:
            other_lang, ok = QInputDialog.getText(window, "Other Languages", "Please specify:")
            if ok and other_lang:
                selected_langs = [l if l != "Other" else other_lang for l in selected_langs]

        demographic_data["name"] = name_input.text().strip()
        demographic_data["age"] = age_input.currentText()
        demographic_data["sex"] = sex_input.currentText()
        demographic_data["native_lang"] = natlang_input.currentText()
        demographic_data["langs_spoken"] = selected_langs
        demographic_data["birthplace"] = birth_input.text().strip()
        demographic_data["currenttown"] = current_input.text().strip()
        demographic_data["speaker_id"] = f"{user_id}"

        #must fill out all fields
        if not demographic_data["name"] or not demographic_data["birthplace"] or not demographic_data["currenttown"]:
            QMessageBox.warning(window, "Missing Info", "Please fill out all text fields.")
            return
        if len(demographic_data["langs_spoken"]) == 0:
            QMessageBox.warning(window, "Missing Info", "Please select at least one spoken language.")
            return

        show_demographic_form_page2()

    next_button.clicked.connect(handle_next)

#---------------Demographics Page 2---------------#
def show_demographic_form_page2():
    clear_layout()

    grew_up_input = QLineEdit()
    punjabi_use_input = QComboBox()
    punjabi_use_input.addItems(["Never", "Rarely", "Sometimes", "Often", "Daily", "All the time"])
    profession_input = QLineEdit()
    education_input = QLineEdit()
    father_input = QLineEdit()

    #layout page 2
    layout.addWidget(QLabel("Where did you grow up?")); layout.addWidget(grew_up_input)
    layout.addWidget(QLabel("How often do you use Punjabi in everyday life?")); layout.addWidget(punjabi_use_input)
    layout.addWidget(QLabel("What is your profession?")); layout.addWidget(profession_input)
    layout.addWidget(QLabel("What is your education level?")); layout.addWidget(education_input)
    layout.addWidget(QLabel("What is your father’s profession?")); layout.addWidget(father_input)

    continue_button = QPushButton("Next")
    continue_button.setStyleSheet("background-color: lightgreen; font-size: 18px; font-weight: bold;")
    layout.addWidget(continue_button)

    #next button
    def handle_continue():
        demographic_data["grew_up"] = grew_up_input.text().strip()
        demographic_data["punjabi_use"] = punjabi_use_input.currentText()
        demographic_data["profession"] = profession_input.text().strip()
        demographic_data["education"] = education_input.text().strip()
        demographic_data["father_profession"] = father_input.text().strip()

        required = ["grew_up", "profession", "education", "father_profession"]
        for field in required:
            if demographic_data[field] == "":
                QMessageBox.warning(window, "Missing Info", "Please complete all fields before continuing.")
                return
        
        #add demographic to csv
        with open("demographics.csv", "a", newline='') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(list(demographic_data.keys()))
            writer.writerow(list(demographic_data.values()))

        show_instruction_screen()

    continue_button.clicked.connect(handle_continue)

#---------------Instructions and Word Trial---------------#
instructions = QLabel(
    "In this phase, you will see a series of Punjabi words on the screen. "
    "Please silently read each word to ensure you are familiar with each one."
)
instructions.setFont(QFont("Verdana", 20))
instructions.setWordWrap(True)
instructions.setAlignment(Qt.AlignCenter)
instructions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
instructions.setMaximumWidth(1000)

current_word = QLabel("")
current_word.setFont(QFont("Jameel Noori Nastaleeq", 75))
current_word.setAlignment(Qt.AlignCenter)
current_word.setContentsMargins(40, 0, 40, 0)
current_word.hide()

start_button = QPushButton("Start")
start_button.setFixedSize(140, 60)
start_button.setStyleSheet("background-color: lightgreen; font-size: 20px; font-weight: bold;")

back_button = QPushButton("Back")
back_button.setFixedSize(120, 50)
back_button.setStyleSheet("background-color: lightgray; font-size: 18px; font-weight: bold;")
back_button.hide()

next_button = QPushButton("Next")
next_button.setFixedSize(120, 50)
next_button.setStyleSheet("background-color: lightblue; font-size: 18px; font-weight: bold;")
next_button.hide()

button_layout = QHBoxLayout()
button_layout.setSpacing(60)
button_layout.setAlignment(Qt.AlignCenter)
button_layout.addWidget(back_button)
button_layout.addWidget(next_button)

def show_instruction_screen():
    clear_layout()
    layout.addWidget(instructions)
    layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Preferred))
    layout.addWidget(start_button, alignment=Qt.AlignCenter)
    layout.addWidget(current_word)
    layout.addLayout(button_layout)

#---------------Word Trial Logic---------------#
def display_next_word():
    global word_num
    total_words = len(word_list)

    if word_num < total_words:
        current_word.setText(word_list[word_num])
        phase0_word_order_list.append(word_list[word_num])
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

        filename = f"{user_id}_phase0_warmup_word_order.csv"
        with open(filename, 'w', newline='') as file:
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

#---------------Connect Buttons---------------#
start_button.clicked.connect(start_experiment)
next_button.clicked.connect(setup_next_word)
back_button.clicked.connect(setup_previous_word)

#---------------Run App---------------#
show_user_id_screen()
window.show()
app.exec_()