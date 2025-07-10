#---------------Import Packages---------------#
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout,
    QTextEdit, QVBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
import csv

#---------------Global Storage---------------#
question_data = {
    "ID": "", "initial_thoughts": "", "study_purpose": "", "attention": "",
    "clarity": "", "followup": ""
}

#---------------Initialize app and window---------------#
class Questionnaire_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Post-experiment Questionnaire")
        self.showFullScreen()

    #escape button
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showMaximized()

app = QApplication([])
window = Questionnaire_Window()

layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)
window.setLayout(layout)

#---------------Helper: Clear Layout---------------#
def clear_layout():
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)
            widget.deleteLater()

#---------------Questionnaire---------------#
def show_questionnaire_form():
    clear_layout()

    #input widgets
    id_input = QLineEdit()
    initial_thoughts = QTextEdit()
    study_purpose = QTextEdit()
    attention = QTextEdit()
    clarity = QTextEdit()
    followup = QLineEdit()


    #layout for questionnaire
    layout.addWidget(QLabel("Enter participant User ID:")); layout.addWidget(id_input)
    layout.addWidget(QLabel("Do you have any initial thoughts or reactions about this experiment?")); layout.addWidget(initial_thoughts)
    layout.addWidget(QLabel("What do you think this study was about?")); layout.addWidget(study_purpose)
    layout.addWidget(QLabel("At any point in the study, did you find yourself struggling to pay attention? If so, when?")); layout.addWidget(attention)
    layout.addWidget(QLabel("Were any of the activity instructions unclear? If so, which ones?")); layout.addWidget(clarity)
    layout.addWidget(QLabel("Would you like to receive updates once the results of the study are published? If so, please provide your email.")); layout.addWidget(followup)
    
    finish_button = QPushButton("Finish")
    finish_button.setStyleSheet("background-color: lightgreen; font-size: 18px; font-weight: bold;")
    finish_button.setFixedSize(180, 50)
    
    # center-align the button inside an HBox
    button_container = QHBoxLayout()
    button_container.addStretch()
    button_container.addWidget(finish_button)
    button_container.addStretch()
    layout.addLayout(button_container)

    #finish button
    def handle_finish():
        
        question_data["ID"] = id_input.text()
        question_data["initial_thoughts"] = initial_thoughts.toPlainText()
        question_data["study_purpose"] = study_purpose.toPlainText()
        question_data["attention"] = attention.toPlainText()
        question_data["clarity"] = clarity.toPlainText()
        question_data["followup"] = followup.text()
        

        #must fill out all fields
        if not question_data["ID"].strip():
            QMessageBox.warning(window, "Missing Info", "Please fill out the ID text field.")
            return
        
        #add question answers to csv
        with open("questionnairre.csv", "a", newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(list(question_data.keys()))
            writer.writerow(list(question_data.values()))
        
        QMessageBox.information(window, "Submitted", "Your response has been recorded.")
        window.close()

    finish_button.clicked.connect(handle_finish)

show_questionnaire_form()
window.showFullScreen()
window.show()
app.exec_()