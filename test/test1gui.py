import sys
import time
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import Qt
import os

# Passage to be read
passage = """the rabbit ran quickly across the field but it was too fast for the fox to follow behind them the wind whispered through the trees making a soft and eerie sound the children watched as the rabbit disappeared into the woods leaving only small footprints in the soft soil the wind blew even harder and the sky turned gray as a storm approached"""

# Global variables for UI elements
passage_label = None
start_button = None
window = None

def init_ui():
    """Initialize the PyQt window and UI elements without using self."""
    global passage_label, start_button, window

    # Create the main window
    window = QWidget()
    window.setWindowTitle('Reading Test (Decoding and Fluency)')
    window.setGeometry(100, 100, 600, 400)

    backgrndimg = QLabel(window)
    backgrndimg.setPixmap(QPixmap('./assets/images/bg1.jpg'))
    backgrndimg.setGeometry(0,0,1500,1000)
    backgrndimg.show()

    # Create layout
    layout = QVBoxLayout()

    # Label to display the passage
    passage_label = QLabel(passage)
    passage_label.setFont(QFont('Arial', 20))
    passage_label.setStyleSheet("background-color: #000000;color: #ffffff;")  # S
    passage_label.setWordWrap(True)
    layout.addWidget(passage_label)

    # Button to start the test
    start_button = QPushButton('Start Test')
    start_button.setFont(QFont('Arial', 16))
    start_button.setStyleSheet("background-color: #20b2aa; color: white; padding: 10px;")
    start_button.clicked.connect(start_test)
    layout.addWidget(start_button, alignment=Qt.AlignCenter)

    # Set the layout for the window
    window.setLayout(layout)
    window.show()

def start_test():
    start_button.setText("Lisenting...")
    """Start the reading test and record reading time."""
    global start_time
    start_time = time.time()

    # Speech recognition to capture user's reading
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        QMessageBox.information(window, 'Info', 'Please start reading the passage aloud.')
        audio_data = recognizer.listen(source)

    # Record end time
    end_time = time.time()

    # Try to recognize the speech
    try:
        user_reading = recognizer.recognize_google(audio_data)
        l1 = user_reading.lower()
        ls = str(l1)
        QMessageBox.information(window, 'Captured Text', f"You read:\n\n{ls}")
        with open("results2.txt","w") as ff:
            ff.write(ls)
        # Measure reading time and calculate results
        reading_time = end_time - start_time
        wpm, errors, accuracy = calculate_results(user_reading, reading_time)
        display_results(wpm, errors, accuracy, reading_time)

    except sr.UnknownValueError:
        QMessageBox.warning(window, 'Error', 'Speech recognition could not understand the audio.')
    except sr.RequestError as e:
        QMessageBox.warning(window, 'Error', f"Could not request results from Google Speech Recognition service; {e}")

def calculate_results(user_reading, reading_time):
    """Calculate WPM, word errors, and accuracy."""
    # Calculate Words Per Minute (WPM)
    words_in_passage = passage.split()
    words_in_reading = user_reading.split()
    num_words = len(words_in_passage)
    num_read_words = len(words_in_reading)
    wpm = (num_read_words / reading_time) * 60

    # Count word errors
    errors = sum(1 for i, word in enumerate(words_in_passage) if i < num_read_words and word != words_in_reading[i])
    accuracy = ((num_words - errors) / num_words) * 100

    return wpm, errors, accuracy

def display_results(wpm, errors, accuracy, reading_time):
    """Display the test results in a message box."""
    result_msg = (f"Reading Time: {reading_time:.2f} seconds\n"
                  f"Words Per Minute (WPM): {wpm:.2f}\n"
                  f"Word Errors: {errors}\n"
                  f"Accuracy: {accuracy:.2f}%")
    QMessageBox.information(window, 'Test Results', result_msg)
    l =result_msg
    lu = ""
    if accuracy >= 80:
        lu ="Normal"
    elif accuracy >= 75:
        lu= "Mild Dyslexia"
    elif accuracy >= 50:
        lu= "Moderate Dyslexia"
    else:
        lu= "Severe Dyslexia"
    lm = "\n Dyslexia Level: "+lu
    with open("results2.txt","a") as ff:
        ff.write(result_msg)
        ff.write(lm)
        os.startfile('results2.txt')
    QApplication.quit()

if __name__ == "__main__":
    # Create the PyQt application
    app = QApplication(sys.argv)

    # Initialize the UI
    init_ui()

    # Execute the PyQt application
    sys.exit(app.exec_())
