import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import Qt
import os, random

# Passage for the patient to read
passage = """In the deep ocean, a small fish named Blue swam through the colorful coral reef. 
Blue was a curious fish, always exploring hidden places and discovering new creatures. One day, 
Blue found a shiny object buried in the sand. It was a golden coin, something Blue had never seen before. 
Excited, Blue showed the coin to his friends, but no one knew where it came from. As the sun set, Blue 
decided to keep the coin safe, hoping to solve the mystery of its origin another day."""

# Questions and their options
questions = [
    ("What was the name of the fish?", ["Blue", "Goldy", "Splash"]),
    ("What did Blue find buried in the sand?", ["A golden coin", "A pearl", "A shell"]),
    ("What time of day did Blue decide to keep the coin safe?", ["Sunset", "Noon", "Morning"]),
    ("Where did Blue swim?", ["Through the coral reef", "In the river", "In a pond"]),
    ("Why was Blue excited?", ["He found a golden coin", "He found a hidden cave", "He saw a giant whale"]),
    ("What color was the coin Blue found?", ["Golden", "Silver", "Bronze"]),
    ("Who did Blue show the coin to?", ["His friends", "His parents", "A stranger"]),
    ("What did Blue hope to solve?", ["The mystery of the coin’s origin", "The way to a hidden treasure", "How to find more coins"]),
    ("What did the coral reef look like?", ["Colorful", "Dark", "Dull"]),
    ("What was Blue's personality?", ["Curious", "Shy", "Lazy"])
]

# Correct answers for the questions
correct_answers = [
    "Blue", "A golden coin", "Sunset", "Through the coral reef", "He found a golden coin",
    "Golden", "His friends", "The mystery of the coin’s origin", "Colorful", "Curious"
]

# Global variables for UI elements
question_index = 0
score = 0
window = None
passage_label = None
question_label = None
button_group = None
radio_buttons = []
submit_button = None

def init_ui():
    """Initialize the PyQt5 UI for the Comprehension and Memory Test."""
    global window, passage_label, submit_button

    window = QWidget()
    window.setWindowTitle('Comprehension and Memory Test')
    window.setGeometry(100, 100, 600, 400)
    lu = QLabel(window)
    lu.setPixmap(QPixmap('./assets/images/bg3.jpg'))
    lu.setGeometry(0,0,1200,1000)
    lu.show()

    # Layout setup
    layout = QVBoxLayout()

    # Display the passage for reading
    passage_label = QLabel(passage)
    passage_label.setFont(QFont('Arial', 18))
    passage_label.setStyleSheet("background-color: #add8e6; color: #000080; padding: 10px;")
    passage_label.setWordWrap(True)
    layout.addWidget(passage_label)

    # Button to proceed to the question phase
    submit_button = QPushButton('Proceed to Questions')
    submit_button.setFont(QFont('Arial', 16))
    submit_button.setStyleSheet("background-color: #20b2aa; color: white; padding: 10px;")
    submit_button.clicked.connect(start_question_phase)
    layout.addWidget(submit_button, alignment=Qt.AlignCenter)

    window.setLayout(layout)
    window.show()

def start_question_phase():
    """Start the question phase after the patient reads the passage."""
    global passage_label, submit_button, question_label, button_group, radio_buttons

    # Remove passage label and the "Proceed" button
    passage_label.hide()
    submit_button.hide()

    # Add a label for questions
    question_label = QLabel()
    question_label.setFont(QFont('Arial', 14))
    window.layout().addWidget(question_label)

    # Radio buttons for the multiple-choice options
    button_group = QButtonGroup()
    for _ in range(3):
        rb = QRadioButton()
        rb.setFont(QFont('Arial', 14))
        window.layout().addWidget(rb)
        button_group.addButton(rb)
        radio_buttons.append(rb)

    # Button to submit answers
    submit_button = QPushButton('Submit Answer')
    submit_button.setFont(QFont('Arial', 20))
    submit_button.setStyleSheet("background-color: #32cd32; color: white;")
    submit_button.clicked.connect(check_answer)
    window.layout().addWidget(submit_button, alignment=Qt.AlignCenter)

    # Show the first question
    display_question()

def display_question():
    """Display the current question and its options."""
    global question_index, question_label, radio_buttons
    # Get the current question and options
    question, options = questions[question_index]
    random.shuffle(options)

    # Update the question label
    question_label.setText(question)
    question_label.setStyleSheet("color: #FFFF33;")
    question_label.setFont(QFont('Arial',26))

    # Update the radio buttons with the options
    for i, option in enumerate(options):
        radio_buttons[i].setText(option)
        radio_buttons[i].setFont(QFont('Arial',18))
        radio_buttons[i].setStyleSheet("color: #39FF14;")
        radio_buttons[i].setChecked(False)

def check_answer():
    """Check the answer for the current question and move to the next."""
    global question_index, score

    # Get the selected answer
    selected_button = button_group.checkedButton()
    if selected_button is None:
        QMessageBox.warning(window, 'Warning', 'Please select an answer!')
        return

    selected_answer = selected_button.text()

    # Check if the selected answer is correct
    if selected_answer == correct_answers[question_index]:
        score += 1

    # Move to the next question or end the test
    question_index += 1
    if question_index < len(questions):
        display_question()
    else:
        end_test()

def end_test():
    """End the test and show the result."""
    global score

    # Calculate score percentage
    total_questions = len(questions)
    percentage_score = (score / total_questions) * 100

    # Display the result
    result_msg = (f"Test Completed!\n\n"
                  f"Your Score: {score}/{total_questions}\n"
                  f"Percentage: {percentage_score:.2f}%")
    QMessageBox.information(window, 'Test Result', result_msg)
    if percentage_score>=80 and percentage_score<=100:
        ls = "Normal person"
    elif percentage_score>=60 and percentage_score<=79:
        ls = "Mild Dyslexia"
    elif percentage_score>=40 and percentage_score<=59:
        ls = "Moderate Dyslexia"
    elif percentage_score<=40:
        ls = "Severe Dyslexia"
    with open("result3.txt","a") as f2:
        f2.write(result_msg)
        f2.write("\n")
        f2.write(ls)
    os.startfile("result3.txt")

    # Close the application after showing the result
    sys.exit()

if __name__ == "__main__":
    # Initialize the PyQt application
    app = QApplication(sys.argv)

    # Initialize and display the UI
    init_ui()

    # Execute the application
    sys.exit(app.exec_())
