import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QColor
import pandas as pd

#wordlist
pan_stimuli_df = pd.read_csv("pan_stimuli.csv")
pan_stimuli = pan_stimuli_df.iloc[:, 0].tolist()

#split wordlist into 4 blocks (A1, B1, A2, B2)
def build_trial_blocks(word_list):
    half = len(word_list) // 2
    A_trials = word_list.copy()
    B_trials = word_list.copy()
    trials = []
    for word in A_trials[:half]:
        trials.append(("A", word))
    for word in B_trials[:half]:
        trials.append(("B", word))
    for word in A_trials[half:]:
        trials.append(("A", word))
    for word in B_trials[half:]:
        trials.append(("B", word))
    return trials

#main GUI
class TileGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phase 2: Listening Task")
        self.setGeometry(100, 100, 900, 700)
        
        #dictionaries storing character info
        self.scenarios = {
            "A": {
                "name": "Person A",
                "starting_points": 1000,
                "timeout_msg": "He couldn't learn that word.",
                "wrong_msg": "He learned the wrong spelling."
            },
            "B": {
                "name": "Person B",
                "starting_points": 100000,
                "timeout_msg": "That word couldn't be added to the dictionary.",
                "wrong_msg": "The wrong spelling was added to the dictionary."
            }
        }

        #randomize the wordlist, track trials
        self.word_list = pan_stimuli.copy()
        random.shuffle(self.word_list)
        self.trials = build_trial_blocks(self.word_list)
        self.total_trials = len(self.trials)
        self.trial_counter = 0

        #score tracking
        self.points = 0
        self.character_points = {
            "A": self.scenarios["A"]["starting_points"],
            "B": self.scenarios["B"]["starting_points"]
        }
        self.max_points_per_trial = 50
        self.tile_buttons = []

        self.setup_ui()


    def setup_ui(self):
        #title
        self.phase2_title = QLabel("Phase 2: Listening", self)
        self.phase2_title.setFont(QFont("Verdana", 34))
        self.phase2_title.adjustSize()
        self.phase2_title.move((self.width() - self.phase2_title.width()) // 2, 250)

        #instructions
        self.instructions = QLabel("", self)
        self.instructions.setFont(QFont("Verdana", 15))
        self.instructions.setWordWrap(True)
        self.instructions.setFixedWidth(600)
        self.instructions.move((self.width() - 600) // 2, 380)
        self.instructions.hide()

        #next button
        self.next_button = QPushButton("Start", self)
        self.next_button.adjustSize()
        self.next_button.move((self.width() - self.next_button.width()) // 2, 500)
        self.next_button.setStyleSheet("background-color: lightblue")
        self.next_button.clicked.connect(self.start_first_instruction)
        self.next_button.show()

        #character points
        self.char_points_label = QLabel(self)
        self.char_points_label.setFont(QFont("Verdana", 14))
        self.char_points_label.move(20, 20)
        self.char_points_label.resize(300, 30)
        self.char_points_label.hide()

        #character placeholder
        icon_size = 100
        self.char_icon = QLabel(self)
        self.char_icon.resize(icon_size, icon_size)
        self.char_icon.hide()

        #total player points
        self.total_points_label = QLabel(f"Total Points: {self.points}", self)
        self.total_points_label.setFont(QFont("Verdana", 16))
        self.total_points_label.move(680, 20)
        self.total_points_label.resize(200, 30)
        self.total_points_label.hide()

        #timer visual
        self.clock = QLabel("", self)
        self.clock.setFont(QFont("Verdana", 17))
        self.clock.setStyleSheet("background-color: lightgrey; border: 2px solid gray; padding: 8px; border-radius: 5px;")
        self.clock.resize(110, 35)
        self.clock.move(680, 60)
        self.clock.hide()

        #remaining points
        self.point_countdown = QLabel("", self)
        self.point_countdown.setFont(QFont("Verdana", 17))
        self.point_countdown.setStyleSheet("background-color: lightgrey; border: 2px solid gray; padding: 8px; border-radius: 5px;")
        self.point_countdown.resize(110, 35)
        self.point_countdown.move(680, 110)
        self.point_countdown.hide()

        #T/F feedback
        self.points_label = QLabel("", self)
        self.points_label.setFont(QFont("Verdana", 16))
        self.points_label.resize(700, 40)
        self.points_label.move((self.width() - 500) // 2, 200)

        #timer setup
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_deciseconds = 0

    #hide title, show instructions
    def start_first_instruction(self):
        self.phase2_title.hide()
        self.show_block_instruction()

    def show_block_instruction(self):
        block_size = len(self.word_list) // 2
        
        #if start of new block
        if self.trial_counter % block_size == 0 and self.trial_counter < self.total_trials:
            self.clear_existing_tiles()
            self.timer.stop()
            self.points_label.clear()

            self.current_speaker, _ = self.trials[self.trial_counter]

            if self.current_speaker == "A":
                text = ("You will hear a series of spoken words. After each word, click the matching word tile "
                        "to help Person A identify the word and achieve his goal of learning to read. ")
            else:
                text = ("You will hear a series of spoken words. After each word, click the matching word tile "
                        "to help Person B identify the word and achieve his goal of adding words to a dictionary. ")

            #instruction text
            self.instructions.setText(text)
            self.instructions.adjustSize()
            self.instructions.show()
            
            #hides timer and points during instructions
            self.clock.hide()
            self.point_countdown.hide()
            self.char_points_label.hide()
            self.total_points_label.hide()

            #placeholder icon
            self.char_icon.move((self.width() - self.char_icon.width()) // 2, 100)
            pixmap = QPixmap(self.char_icon.size())
            pixmap.fill(QColor("darkgray"))
            self.char_icon.setPixmap(pixmap)
            self.char_icon.show()

            #change start to next button
            self.next_button.setText("Next")
            self.next_button.show()
            self.next_button.clicked.disconnect()
            self.next_button.clicked.connect(self.start_block)
        else:
            self.start_block()

    def start_block(self):
        #hide icons
        self.instructions.hide()
        self.next_button.hide()
        self.char_icon.hide()

        #show relevant icons
        self.char_points_label.show()
        self.total_points_label.show()
        self.clock.show()
        self.point_countdown.show()

        #move image
        self.char_icon.move(20, 60)
        #placeholder
        pixmap = QPixmap(self.char_icon.size())
        pixmap.fill(QColor("darkgray"))
        self.char_icon.setPixmap(pixmap)
        self.char_icon.show()
        
        #load next word
        self.next_trial()

    def next_trial(self):
        #if game done
        if self.trial_counter >= self.total_trials:
            #hide all trial icons
            self.points_label.setText("")
            self.clear_existing_tiles()
            self.timer.stop()
            self.clock.hide()
            self.point_countdown.hide()
            self.char_icon.hide()
            self.char_points_label.hide()
            self.total_points_label.hide()

            #final message
            self.final_message = QLabel("All finished!", self)
            self.final_message.setFont(QFont("Verdana", 28))
            self.final_message.adjustSize()
            self.final_message.move((self.width() - self.final_message.width()) // 2, 80)
            self.final_message.show()

            #shows character scores
            y_base = 160
            for label_text in [
                    f"Your Points: {self.points}",
                    f"Person A: {self.character_points['A']}",
                    f"Person B: {self.character_points['B']}"
            ]:
                    label = QLabel(label_text, self)
                    label.setFont(QFont("Verdana", 17))
                    label.setStyleSheet("background-color: lightgreen; padding: 6px; border-radius: 5px")
                    label.adjustSize()
                    label.move((self.width() - label.width()) // 2, y_base)
                    label.show()
                    y_base += 60
            return

        #next speaker
        self.current_speaker, self.target_word = self.trials[self.trial_counter]
        scenario = self.scenarios[self.current_speaker]
        self.char_points_label.setText(f"{scenario['name']} Points: {self.character_points[self.current_speaker]}")
        self.total_points_label.setText(f"Total Points: {self.points}")

        #prep for next trial, resetting
        self.trial_counter += 1
        self.points_label.setText("")
        self.elapsed_deciseconds = 0
        self.clock.setText("0.0 sec")
        self.point_countdown.setText(f"{self.max_points_per_trial} pts")

        #setup icons
        self.create_tiles()
        self.clock.show()
        self.point_countdown.show()
        self.timer.start()

    def create_tiles(self):
        #word selection
        self.clear_existing_tiles()
        distractors = random.sample([w for w in pan_stimuli if w != self.target_word], 15)
        self.tile_words = distractors + [self.target_word]
        random.shuffle(self.tile_words)

        #grid layout
        cols = 4
        tile_width = 180
        tile_height = 60
        x_margin = 60
        y_margin = 290

        #make and display tile 
        for i, word in enumerate(self.tile_words):
            tile = QPushButton(word, self)
            tile.resize(tile_width, tile_height)
            tile.setFont(QFont("Verdana", 14))
            tile.setStyleSheet("background-color: lightgray; border-radius: 12px;")
            row = i // cols
            col = i % cols
            tile.move(x_margin + col * (tile_width + 10), y_margin + row * (tile_height + 20))
            tile.clicked.connect(lambda checked, w=word, btn=tile: self.check_tile_click(w, btn))
            tile.show()
            self.tile_buttons.append(tile)

    def update_timer(self):
        #update time
        self.elapsed_deciseconds += 1
        seconds = self.elapsed_deciseconds / 10
        self.clock.setText(f"{seconds:.1f} sec")
        #update points
        pts_left = max(self.max_points_per_trial - self.elapsed_deciseconds, 0)
        self.point_countdown.setText(f"{pts_left} pts")
        
        #timeout
        if self.elapsed_deciseconds >= 50:
            self.timer.stop()
            self.disable_tiles()
            msg = self.scenarios[self.current_speaker]["timeout_msg"]
            self.points_label.setText(f" {msg} (0 pts)")
            QTimer.singleShot(1500, self.show_block_instruction)

    #check T/F
    def check_tile_click(self, selected_word, tile_button):
        self.timer.stop()
        self.disable_tiles()
        pts_left = max(self.max_points_per_trial - self.elapsed_deciseconds, 0)

        if selected_word == self.target_word:
            self.points += pts_left
            self.character_points[self.current_speaker] += pts_left
            tile_button.setStyleSheet("background-color: green; color: white; font-size: 16px; border-radius: 12px;")
            self.points_label.setText(f"✅ Correct: +{pts_left} pts")
        else:
            self.points -= 50
            self.character_points[self.current_speaker] -= 50
            tile_button.setStyleSheet("background-color: red; color: white; font-size: 16px; border-radius: 12px;")
            msg = self.scenarios[self.current_speaker]["wrong_msg"]
            self.points_label.setText(f"❌ {msg} (-50 pts)")

        self.total_points_label.setText(f"Total Points: {self.points}")
        self.char_points_label.setText(f"{self.scenarios[self.current_speaker]['name']} Points: {self.character_points[self.current_speaker]}")
        QTimer.singleShot(1500, self.show_block_instruction)

    def disable_tiles(self):
        for tile in self.tile_buttons:
            tile.setEnabled(False)
    
    #deletes tiles
    def clear_existing_tiles(self):
        for tile in self.tile_buttons:
            tile.setParent(None)
            tile.deleteLater()
        self.tile_buttons.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TileGame()
    window.show()
    sys.exit(app.exec_())
