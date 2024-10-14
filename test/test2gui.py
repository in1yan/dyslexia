import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import Qt
import os
# Global variables
total_words = 0
correct_answers = 0
incorrect_words = []
current_word = None
word_index = 0
set_index = 0
word_sets = [
    {
        "level": "Easy",
        "words": [
            {"word": "cat", "sentence": "The _____ sat on the mat."},
            {"word": "dog", "sentence": "The _____ barked loudly."},
            {"word": "book", "sentence": "I read a _____ every night."},
            {"word": "jump", "sentence": "She can _____ very high."},
            {"word": "blue", "sentence": "The sky is _____."},
        ]
    },
    {
        "level": "Moderate",
        "words": [
            {"word": "whispered", "sentence": "The wind _____ through the trees."},
            {"word": "disappeared", "sentence": "The rabbit _____ into the woods."},
            {"word": "approached", "sentence": "The storm _____ quickly."},
            {"word": "footprints", "sentence": "We saw _____ in the soil."},
            {"word": "eerie", "sentence": "There was an _____ sound in the forest."}
        ]
    },
    {
        "level": "Difficult",
        "words": [
            {"word": "pharmacy", "sentence": "She went to the _____ to buy medicine."},
            {"word": "rhythm", "sentence": "The song had a fast _____."},
            {"word": "knight", "sentence": "The _____ rode his horse bravely."},
            {"word": "psychology", "sentence": "She studied _____ in college."},
            {"word": "receipt", "sentence": "He forgot to ask for a _____ at the store."}
        ]
    }
]

def init_ui():
    """Initialize the PyQt window and UI elements."""
    global sentence_label, option_buttons, start_button

    # Create the main window
    window = QWidget()
    window.setWindowTitle("Dyslexia Spelling Test")
    window.setGeometry(100, 100, 500, 300)
    window.setStyleSheet("background-color: #f0f8ff;")  # Set background color

    backimg = QLabel(window)
    backimg.setPixmap(QPixmap('./assets/images/im.jpeg'))
    backimg.setGeometry(0,0,1200,1000)
    backimg.show()

    # Main layout
    layout = QVBoxLayout()

    # Sentence label with increased font size
    sentence_label = QLabel("Welcome to the spelling test. Press 'Start' to begin.")
    sentence_label.setFont(QFont("Arial", 16))  # Increased font size for the sentence
    layout.addWidget(sentence_label, alignment=Qt.AlignCenter)

    # Option buttons
    buttons_layout = QHBoxLayout()
    option_buttons = []

    for i in range(4):
        btn = QPushButton(f"Option {i + 1}", window)
        btn.setFont(QFont("Arial", 14))  # Increase button font size
        btn.setStyleSheet("background-color: #add8e6; color: #000080; padding: 10px;")  # Button style with color
        btn.clicked.connect(lambda checked, b=btn: check_answer(b.text()))
        option_buttons.append(btn)
        buttons_layout.addWidget(btn)

    layout.addLayout(buttons_layout)

    # Start button with larger text and color
    start_button = QPushButton("Start Test", window)
    start_button.setFont(QFont("Arial", 16))  # Increased font size for the start button
    start_button.setStyleSheet("background-color: #20b2aa; color: white; padding: 10px;")  # Start button color
    start_button.clicked.connect(start_test)
    layout.addWidget(start_button, alignment=Qt.AlignCenter)

    window.setLayout(layout)
    window.show()
    return window

def start_test():
    start_button.hide()
    """Start the spelling test by resetting variables and loading the first word."""
    global total_words, correct_answers, incorrect_words, word_index, set_index
    total_words = 0
    correct_answers = 0
    incorrect_words = []
    word_index = 0
    set_index = 0
    load_next_word()

def load_next_word():
    """Load the next word and update the UI elements with the new sentence and options."""
    global word_sets, set_index, word_index, current_word, option_buttons, sentence_label

    # If no more words, show results
    if set_index >= len(word_sets):
        show_results()
        return

    # Get the current set and word
    current_set = word_sets[set_index]
    current_word = current_set["words"][word_index]

    # Update sentence label
    sentence_label.setText(current_word["sentence"].replace(current_word["word"], "_____"))

    # Generate incorrect options
    incorrect_options = generate_incorrect_options(current_word["word"])

    # Combine correct and incorrect options and shuffle
    options = incorrect_options + [current_word["word"]]
    random.shuffle(options)

    # Update the buttons with options
    for i, option in enumerate(options):
        option_buttons[i].setText(option)

def check_answer(selected_word):
    """Check the selected word and determine if the answer is correct."""
    global correct_answers, incorrect_words, word_index, total_words, set_index

    # Check if the selected word is correct
    if selected_word == current_word["word"]:
        correct_answers += 1
    else:
        incorrect_words.append(current_word["word"])

    # Move to the next word
    word_index += 1
    total_words += 1

    # If finished with the current set, move to the next
    if word_index >= len(word_sets[set_index]["words"]):
        word_index = 0
        set_index += 1

    load_next_word()

def show_results():
    """Show the final results and dyslexia level based on performance."""
    global correct_answers, total_words

    accuracy = (correct_answers / total_words) * 100
    dyslexia_level = classify_dyslexia_level(accuracy)

    result_msg = f"Total words: {total_words}\nCorrect answers: {correct_answers}\n" \
                 f"Accuracy: {accuracy:.2f}%\n\nDyslexia Level: {dyslexia_level}"

    if incorrect_words:
        result_msg += "\n\nWords you struggled with:\n" + "\n".join(incorrect_words)

    QMessageBox.information(None, "Test Results", result_msg)
    l = result_msg
    with open('result.txt', "w") as f:
        f.write(l)
    os.startfile('result.txt')
    QApplication.quit()

def generate_incorrect_options(correct_word):
    """Generate three incorrect options for the given correct word."""
    incorrect_words = [
        correct_word[:-1] + 'z',  # Change last letter
        'pre' + correct_word,     # Add prefix
        correct_word + 'ing',     # Add suffix
    ]
    return incorrect_words[:3]

def classify_dyslexia_level(accuracy):
    """Classify the dyslexia level based on accuracy."""
    if accuracy >= 90:
        return "Normal"
    elif accuracy >= 75:
        return "Mild Dyslexia"
    elif accuracy >= 50:
        return "Moderate Dyslexia"
    else:
        return "Severe Dyslexia"
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = init_ui()
    sys.exit(app.exec_())
