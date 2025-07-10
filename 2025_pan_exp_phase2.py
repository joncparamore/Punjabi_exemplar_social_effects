import sys, csv, os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtMultimedia import QSoundEffect
from collections import defaultdict
import pandas as pd


def build_trial_blocks(speaker_a_words, speaker_b_words, block_size=5):

    # Create 3 repetitions for each word
    speaker_a_trials = [("A", word) for word in speaker_a_words for _ in range(3)]
    speaker_b_trials = [("B", word) for word in speaker_b_words for _ in range(3)]

    # Shuffle trials for each speaker
    random.shuffle(speaker_a_trials)
    random.shuffle(speaker_b_trials)

    # Interleave in blocks of 5, Scholar first
    trials = []
    total_blocks = len(speaker_a_trials) // block_size 

    for i in range(total_blocks):
        b_block = speaker_b_trials[i * block_size:(i + 1) * block_size]
        a_block = speaker_a_trials[i * block_size:(i + 1) * block_size]
        trials.extend(b_block)
        trials.extend(a_block)

    return trials



class TileGame(QWidget):
    def __init__(self):
        super().__init__()
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.screen_width = size.width()
        self.screen_height = size.height()

        self.setWindowTitle("Phase 2: Listening Task")
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        #character info
        self.scenarios = {
            "A": {"name": "Laborer", "starting_points": 1000,
                  "timeout_msg": "He couldn't learn that word.",
                  "wrong_msg": "He learned the wrong spelling."},
            "B": {"name": "Scholar", "starting_points": 100000,
                  "timeout_msg": "That word couldn't be added to the dictionary.",
                  "wrong_msg": "The wrong spelling was added to the dictionary."}
        }

        # Load words and corresponding audio
        speaker_a_words, speaker_b_words, self.map_sh_to_audio = self.load_audio_mappings()
        self.trials = build_trial_blocks(speaker_a_words, speaker_b_words)
        self.word_list = speaker_a_words + speaker_b_words

        self.total_trials = len(self.trials)

        # Game state attributes
        self.audio_played = False
        self.replay_used = False
        self.trial_counter = 0
        self.points = 0
        self.correct_answer_order = []
        self.character_points = {
        "A": self.scenarios["A"]["starting_points"],
        "B": self.scenarios["B"]["starting_points"]
        }
        self.max_points_per_trial = 50
        self.tile_buttons = []
        self.sound = QSoundEffect()

        self.setup_ui()
        
        # Hide all game UI initially
        self.phase2_title.hide()
        self.next_button.hide()
        self.play_word_button.hide()
        self.char_points_label.hide()
        self.total_points_label.hide()
        self.clock.hide()
        self.point_countdown.hide()
        self.points_label.hide()
        self.char_icon.hide()


    # Load audio and map words
    def load_audio_mappings(self):

        # Load Shahmukhi–IPA mapping from CSV
        df = pd.read_csv("tokens_shahmukhi_ipa.csv", encoding="utf-8")
        df.columns = [col.strip() for col in df.columns]
        shahmukhi_col = df.columns[0]
        ipa_col = "IPA"
        change_sh_to_ipa = dict(zip(df[shahmukhi_col].str.strip(), df[ipa_col].str.strip()))

        # Prepare to map IPA → audio paths
        ato_audio_directory = "2025_pan_AT0"
        ak_audio_directory = "2025_pan_AK1"
        match_ipa_to_file = defaultdict(list)

        for file_name in os.listdir(ato_audio_directory):
            if file_name.endswith(".wav"):
                ipa_word = file_name.split("_")[-1].replace(".wav", "").strip()
                full_path = os.path.join(ato_audio_directory, file_name)
                match_ipa_to_file[ipa_word].append((full_path, "ATO"))

        for file_name in os.listdir(ak_audio_directory):
            if file_name.endswith(".wav"):
                ipa_word = file_name.split("_")[-1].replace(".wav", "").strip()
                full_path = os.path.join(ak_audio_directory, file_name)
                match_ipa_to_file[ipa_word].append((full_path, "AK1"))

        # Separate Shahmukhi words by where their IPA appears (AK1 vs ATO)
        speaker_a_words = []  # AK1 → Laborer
        speaker_b_words = []  # ATO → Scholar
        map_sh_to_audio = {}

        for sh_word, ipa in change_sh_to_ipa.items():
            paths = match_ipa_to_file.get(ipa, [])
            sources = {src: path for path, src in paths}
            if "AK1" in sources:
                speaker_a_words.append(sh_word)
                map_sh_to_audio[sh_word] = sources
            elif "ATO" in sources:
                speaker_b_words.append(sh_word)
                map_sh_to_audio[sh_word] = sources

        if len(speaker_a_words) < 25 or len(speaker_b_words) < 25:
            raise ValueError(f"Not enough words: {len(speaker_a_words)} for AK1, {len(speaker_b_words)} for ATO.")

        return speaker_a_words, speaker_b_words, map_sh_to_audio



    def scale_w(self, x_ratio): return int(self.screen_width * x_ratio)
    def scale_h(self, y_ratio): return int(self.screen_height * y_ratio)

    # UI formatting
    def setup_ui(self):
        self.phase2_title = QLabel("Phase 2: Listening", self)
        self.phase2_title.setFont(QFont("Verdana", self.scale_h(0.05)))
        self.phase2_title.adjustSize()
        self.phase2_title.move((self.screen_width - self.phase2_title.width()) // 2, self.scale_h(0.4))

        self.instructions = QLabel("", self)
        self.instructions.setFont(QFont("Verdana", self.scale_h(0.016)))
        self.instructions.setWordWrap(True)
        self.instructions.setFixedWidth(self.scale_w(0.5))
        self.instructions.move(0, 0)  # Temporary position; will be repositioned later
        self.instructions.hide()

        self.next_button = QPushButton("Start", self)
        self.next_button.setFont(QFont("Verdana", self.scale_h(0.018)))
        self.next_button.resize(self.scale_w(0.15), self.scale_h(0.07))
        self.next_button.move((self.screen_width - self.next_button.width()) // 2, self.scale_h(0.70))
        self.next_button.setStyleSheet("background-color: lightgray; border-radius: 10px;")
        self.next_button.clicked.connect(self.start_first_instruction)

        self.play_word_button = QPushButton("Play Word", self)
        self.play_word_button.setFont(QFont("Verdana", self.scale_w(0.012)))
        self.play_word_button.resize(self.scale_w(0.15), self.scale_h(0.07))
        self.play_word_button.move((self.screen_width - self.play_word_button.width()) // 2, self.scale_h(0.70))
        self.play_word_button.setStyleSheet("background-color: lightblue; border-radius: 10px;")
        self.play_word_button.clicked.connect(self.handle_play_word)
        self.play_word_button.hide()

        self.char_points_label = QLabel(self)
        self.char_points_label.setFont(QFont("Verdana", self.scale_h(0.014)))
        self.char_points_label.move(self.scale_w(0.02), self.scale_h(0.06))
        self.char_points_label.resize(self.scale_w(0.2), 30)
        self.char_points_label.hide()

        icon_size = self.scale_w(0.125)
        self.char_icon = QLabel(self)
        self.char_icon.resize(icon_size, icon_size)
        self.char_icon.hide()

        self.total_points_label = QLabel(f"Total Points: {self.points}", self)
        self.total_points_label.setFont(QFont("Verdana", self.scale_h(0.016)))
        self.total_points_label.move(self.screen_width - self.scale_w(0.22), self.scale_h(0.06))
        self.total_points_label.resize(self.scale_w(0.2), 30)
        self.total_points_label.hide()

        self.clock = QLabel("", self)
        self.clock.setFont(QFont("Verdana", self.scale_h(0.014)))
        self.clock.setStyleSheet("background-color: lightgrey; border: 2px solid gray; padding: 8px; border-radius: 5px;")
        self.clock.resize(self.scale_w(0.08), self.scale_h(0.05))
        self.clock.move(self.screen_width - self.scale_w(0.22), self.scale_h(0.13))
        self.clock.hide()

        self.point_countdown = QLabel("", self)
        self.point_countdown.setFont(QFont("Verdana", self.scale_h(0.014)))
        self.point_countdown.setStyleSheet("background-color: lightgrey; border: 2px solid gray; padding: 8px; border-radius: 5px;")
        self.point_countdown.resize(self.scale_w(0.08), self.scale_h(0.05))
        self.point_countdown.move(self.screen_width - self.scale_w(0.22), self.scale_h(0.20))
        self.point_countdown.hide()

        self.points_label = QLabel("", self)
        self.points_label.setFont(QFont("Verdana", self.scale_h(0.025)))
        self.points_label.resize(700, 40)
        self.points_label.move((self.screen_width - 500) // 2, self.scale_h(0.18))

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_deciseconds = 0
        
        self.user_id = None

        # ID Entry UI
        self.id_container = QWidget(self)
        id_layout = QVBoxLayout(self.id_container)
        id_layout.setAlignment(Qt.AlignCenter)

        self.id_label = QLabel("Please enter your Name or ID to begin:", self)
        self.id_label.setFont(QFont("Verdana", self.scale_h(0.025)))
        self.id_label.setAlignment(Qt.AlignCenter)

        self.id_input = QLineEdit(self)
        self.id_input.setFont(QFont("Verdana", self.scale_h(0.02)))
        self.id_input.setFixedWidth(self.scale_w(0.4))
        self.id_input.setPlaceholderText("e.g., jsmith123")
        self.id_input.setAlignment(Qt.AlignCenter)

        self.continue_button = QPushButton("Continue", self)
        self.continue_button.setFont(QFont("Verdana", self.scale_h(0.02)))
        self.continue_button.setFixedSize(self.scale_w(0.12), self.scale_h(0.06))
        self.continue_button.setStyleSheet("background-color: lightgreen;")
        self.continue_button.clicked.connect(self.collect_user_id)

        id_layout.addSpacing(self.scale_h(0.2))
        id_layout.addWidget(self.id_label, alignment=Qt.AlignCenter)
        id_layout.addSpacing(self.scale_h(0.05))
        id_layout.addWidget(self.id_input, alignment=Qt.AlignCenter)
        id_layout.addSpacing(self.scale_h(0.05))
        id_layout.addWidget(self.continue_button, alignment=Qt.AlignCenter)


        self.id_container.setLayout(id_layout)
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.id_container)
        self.setLayout(main_layout)
        
        self.target_word_label = QLabel("", self)
        self.target_word_label.setFont(QFont("Jameel Noori Nastaleeq", self.scale_w(0.03)))
        self.target_word_label.setAlignment(Qt.AlignCenter)
        self.target_word_label.setGeometry(0, self.scale_h(0.28), self.screen_width, self.scale_h(0.1))
        self.target_word_label.hide()
    
    def collect_user_id(self):
        entered_id = self.id_input.text().strip()
        if entered_id:
            self.user_id = entered_id
            self.id_container.hide()
            self.phase2_title.show()
            self.next_button.show()
        else:
            self.id_label.setText("⚠ Please enter your ID to proceed")


        
    # instructions logic
    def start_first_instruction(self):
        self.phase2_title.hide()
        self.show_block_instruction()

    # shows instructions every 5, preps character image and text
    def show_block_instruction(self):
        if self.trial_counter >= self.total_trials:
            self.next_trial()
            return
        
        block_size = 5
        if self.trial_counter % block_size == 0 and self.trial_counter < self.total_trials:
            self.clear_existing_tiles()
            self.timer.stop()
            self.points_label.clear()
            self.target_word_label.hide()
            self.current_speaker, _ = self.trials[self.trial_counter]
            text = ("You will hear a series of spoken words. After each word, click the matching word tile "
                    f"to help {self.scenarios[self.current_speaker]['name']} complete their goal.")
            self.instructions.setText(text)
            # position instructions based on character
            y_pos = 0.62 if self.current_speaker == "B" else 0.58
            self.instructions.move(
                (self.screen_width - self.instructions.width()) // 2,
                self.scale_h(y_pos)
                )
            self.instructions.adjustSize()
            self.instructions.show()

            self.clock.hide()
            self.point_countdown.hide()
            self.char_points_label.hide()
            self.total_points_label.hide()

            if self.current_speaker == "B":
                scholar_size = self.scale_w(0.28)
                self.char_icon.resize(scholar_size, scholar_size)
                self.char_icon.move(self.scale_w(0.365), self.scale_h(0.15))
            else:
                normal_size = self.scale_w(0.225)
                self.char_icon.resize(normal_size, normal_size)
                self.char_icon.move(self.scale_w(0.3875), self.scale_h(0.15))

            pixmap = QPixmap("laborer.jpg") if self.current_speaker == "A" else QPixmap("scholar.jpg")
            pixmap = pixmap.scaled(self.char_icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.char_icon.setPixmap(pixmap)
            self.char_icon.show()

            self.next_button.setText("Next")
            self.next_button.show()
            self.next_button.clicked.disconnect()
            self.next_button.clicked.connect(self.start_block)
        else:
            self.start_block()

    #starts actual trial
    def start_block(self):
        self.instructions.hide()
        self.next_button.hide()

        # Show large character image 
        if self.current_speaker == "B":
            scholar_size = self.scale_w(0.28)
            self.char_icon.resize(scholar_size, scholar_size)
            self.char_icon.move(self.scale_w(0.365), self.scale_h(0.15))
        else:
            normal_size = self.scale_w(0.225)
            self.char_icon.resize(normal_size, normal_size)
            self.char_icon.move(self.scale_w(0.3875), self.scale_h(0.15))

        pixmap = QPixmap("laborer.jpg") if self.current_speaker == "A" else QPixmap("scholar.jpg")
        pixmap = pixmap.scaled(self.char_icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.char_icon.setPixmap(pixmap)
        self.char_icon.show()

        # Hide everything else
        self.char_points_label.hide()
        self.total_points_label.hide()
        self.clock.hide()
        self.point_countdown.hide()
        self.points_label.hide()
        self.clear_existing_tiles()
        self.target_word_label.hide()

        self.audio_played = False
        self.replay_used = False
        self.play_word_button.setEnabled(True)
        self.play_word_button.show()


    # audio playback logic
    def handle_play_word(self):
        _, self.target_word = self.trials[self.trial_counter]
        #print(f"\n Target word: {self.target_word}")

        audio_entry = self.map_sh_to_audio.get(self.target_word, {})
        #print(f" Audio entry found: {audio_entry}")

        source = "AK1" if self.current_speaker == "A" else "ATO"
        #print(f" Speaker source: {source}")

        audio_path = audio_entry.get(source, None)
        #print(f" Audio path: {audio_path}")

        #if not audio_path:
            #print(" ERROR: No audio path found for this word.")
            #return

        # Check if file actually exists
        #if not os.path.exists(audio_path):
            #print(f" ERROR: Audio file does NOT exist: {audio_path}")
            #return
        #else:
            #print(" Audio file exists.")

        self.sound.setSource(QUrl.fromLocalFile(audio_path))
        #print(f" Sound status after setSource: {self.sound.status()}")  

        self.sound.play()

        if not self.audio_played:
            self.audio_played = True

            def after_audio():
                if not self.sound.isPlaying():
                    self.sound.playingChanged.disconnect(after_audio)
                    self.play_word_button.hide()
                    self.next_trial()

            self.sound.playingChanged.connect(after_audio)

        else:
            if not self.replay_used:
                self.replay_used = True
            else:
                self.play_word_button.setEnabled(False)

    # trial logic
    def next_trial(self):
        if self.trial_counter >= self.total_trials:
            self.save_csv_output()  
            self.points_label.setText("")
            self.clear_existing_tiles()
            self.timer.stop()
            self.clock.hide()
            self.point_countdown.hide()
            self.char_icon.hide()
            self.char_points_label.hide()
            self.total_points_label.hide()

            self.final_message = QLabel("All finished!", self)
            self.final_message.setFont(QFont("Verdana", self.scale_h(0.025)))
            self.final_message.adjustSize()
            self.final_message.move((self.screen_width - self.final_message.width()) // 2, 80)
            self.final_message.show()

            y_base = 160
            for label_text in [
                    f"Your Points: {self.points}",
                    f"Laborer: {self.character_points['A']}",
                    f"Scholar: {self.character_points['B']}"
                    ]:
                label = QLabel(label_text, self)
                label.setFont(QFont("Verdana", self.scale_w(0.015)))
                label.setStyleSheet("background-color: lightgreen; padding: 6px; border-radius: 5px")
                label.adjustSize()
                label.move((self.screen_width - label.width()) // 2, y_base)
                label.show()
                y_base += 60
            return

        self.current_speaker, self.target_word = self.trials[self.trial_counter]
        self.correct_answer_order.append(self.target_word)
        scenario = self.scenarios[self.current_speaker]

        # Resize/reposition character image to SMALL version now
        if self.current_speaker == "B":
            small_size = self.scale_w(0.18)
            self.char_icon.resize(small_size, small_size)
            self.char_icon.move(self.scale_w(0.02), self.scale_h(0.08))
        else:
            small_size = self.scale_w(0.14)
            self.char_icon.resize(small_size, small_size)
            self.char_icon.move(self.scale_w(0.02), self.scale_h(0.12))

        pixmap = QPixmap("laborer.jpg") if self.current_speaker == "A" else QPixmap("scholar.jpg")
        pixmap = pixmap.scaled(self.char_icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.char_icon.setPixmap(pixmap)
        self.char_icon.show()

        # Show character and total points labels now (not earlier)
        self.char_points_label.setText(f"{scenario['name']} Points: {self.character_points[self.current_speaker]}")
        self.total_points_label.setText(f"Total Points: {self.points}")
        self.total_points_label.show()
        self.points_label.show()
        self.char_points_label.show()

        self.trial_counter += 1
        self.points_label.setText("")
        self.elapsed_deciseconds = 0
        self.clock.setText("0.0 sec")
        self.point_countdown.setText(f"{self.max_points_per_trial} pts")

        self.create_tiles()
        self.clock.show()
        self.point_countdown.show()
        self.timer.start()

    # CSV output
    def save_csv_output(self):
        filename = f"phase2_correct_order_{self.user_id}.csv"
        with open(filename, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for word in self.correct_answer_order:
                writer.writerow([word])

    # Generate tile grid
    def create_tiles(self):
        self.clear_existing_tiles()
        distractors = random.sample([w for w in self.word_list if w != self.target_word], 15)
        self.tile_words = distractors + [self.target_word]
        random.shuffle(self.tile_words)

        cols = 4
        tile_width = self.scale_w(0.20)
        tile_height = self.scale_h(0.10)
        spacing = 10
        x_margin = self.scale_w(0.09)
        y_margin = self.scale_h(0.4)

        for i, word in enumerate(self.tile_words):
            tile = QPushButton(word, self)
            tile.resize(tile_width, tile_height)
            tile.setFont(QFont("Jameel Noori Nastaleeq", self.scale_w(0.018)))
            tile.setStyleSheet("background-color: lightgray; border-radius: 12px;")
            row = i // cols
            col = i % cols
            tile.move(x_margin + col * (tile_width + spacing), y_margin + row * (tile_height + 20))
            tile.clicked.connect(lambda checked, w=word, btn=tile: self.check_tile_click(w, btn))
            tile.show()
            self.tile_buttons.append(tile)

    # Timer countdown
    def update_timer(self):
        self.elapsed_deciseconds += 1
        seconds = self.elapsed_deciseconds / 10
        self.clock.setText(f"{seconds:.1f} sec")
        pts_left = max(self.max_points_per_trial - self.elapsed_deciseconds, 0)
        self.point_countdown.setText(f"{pts_left} pts")

        if self.elapsed_deciseconds >= 50:
            self.timer.stop()
            self.disable_tiles()
            msg = self.scenarios[self.current_speaker]["timeout_msg"]
            self.points_label.setText(f" {msg} (0 pts)")
            QTimer.singleShot(1500, self.show_block_instruction)

    def check_tile_click(self, selected_word, tile_button):
        self.timer.stop()
        self.disable_tiles()
        pts_left = max(self.max_points_per_trial - self.elapsed_deciseconds, 0)

        if selected_word == self.target_word:
            self.points += pts_left
            self.character_points[self.current_speaker] += pts_left
            tile_button.setStyleSheet("background-color: green; color: white; border-radius: 12px;")
            self.points_label.setText(f"✅ Correct: +{pts_left} pts")
            QTimer.singleShot(1500, self.show_block_instruction)
        else:
            self.points -= 50
            self.character_points[self.current_speaker] -= 50
            tile_button.setStyleSheet("background-color: red; color: white; border-radius: 12px;")
            msg = self.scenarios[self.current_speaker]["wrong_msg"]
            self.points_label.setText(f"❌ {msg} (-50 pts)")
            self.total_points_label.setText(f"Total Points: {self.points}")
            self.char_points_label.setText(f"{self.scenarios[self.current_speaker]['name']} Points: {self.character_points[self.current_speaker]}")

            def highlight_correct_tile():
                for btn in self.tile_buttons:
                    if btn.text() == self.target_word:
                        btn.setStyleSheet("background-color: green; color: white; border-radius: 12px;")
                        break
                QTimer.singleShot(1000, self.show_block_instruction)

            QTimer.singleShot(1000, highlight_correct_tile)

    def disable_tiles(self):
        for tile in self.tile_buttons:
            tile.setEnabled(False)

    def clear_existing_tiles(self):
        for tile in self.tile_buttons:
            tile.setParent(None)
            tile.deleteLater()
        self.tile_buttons.clear()

    # Exit shortcut
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TileGame()
    window.showFullScreen()

    sys.exit(app.exec_())
