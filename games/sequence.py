from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout
import random
import sys
import os

class Sequence(QWidget):
    def __init__(self):
        super().__init__()
        self.chars = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]
        self.setWindowTitle("Dyslexia")
        self.setStyleSheet("background-color: white;")
        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Central character label
        self.char = QLabel(self)
        self.char.setAlignment(Qt.AlignCenter)
        self.char.setStyleSheet("font-size: 150px;")
        self.layout.addWidget(self.char)

        # Instruction label
        self.instruction = QLabel("\"Press Enter or Space to start\"", self)
        self.instruction.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.instruction.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.instruction)

        # GIF label for animation
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.gif_label)

        # Grid layout for buttons (4x4 grid of characters)
        self.button_grid = QGridLayout()
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_grid)
        self.layout.addWidget(self.button_widget)
        self.button_widget.hide()  # Initially hide the buttons

        # Path to GIF file
        self.gif_paths = [os.path.join('./assets/gifs', f) for f in os.listdir('./assets/gifs') if f.endswith('.gif')]
        self.gif_path = random.choice(self.gif_paths)

        # Random character to be guessed
        self.rand_num = str(random.choice(self.chars))

        # Create 4x4 buttons with possible choices
        self.buttons = []
        self.create_buttons()

        self.show_number()

    def create_buttons(self):
        """Create a 4x4 grid of buttons with possible choices."""
        random_choices = random.sample(self.chars, 3)
        random_choices.append(self.rand_num)
        positions = [(i, j) for i in range(2) for j in range(2)]
        random.shuffle(random_choices)  # Shuffle positions to randomize button placement

        for i, char in enumerate(random_choices):  # Create buttons with random choices
            button = QPushButton(char)
            button.setStyleSheet("font-size: 30px; padding: 20px;")
            button.clicked.connect(self.handle_button_click)
            self.buttons.append(button)
            row, col = positions[i]  # Get randomized grid position
            self.button_grid.addWidget(button, row, col)

    def show_number(self):
        """Display a random character."""
        self.rand_num = str(random.choice(self.chars))  # Set a new random character
        self.char.setText(self.rand_num)
        self.char.show()
        self.gif_label.hide()
        self.instruction.hide()
        self.button_widget.hide()

        # Wait 3 seconds before showing the GIF
        QTimer.singleShot(8000, self.show_gif)

    def show_gif(self):
        """Display the GIF animation."""
        self.char.hide()
        self.gif_label.show()

        self.gif_path = random.choice(self.gif_paths)
        # Set the movie (GIF) and start it
        movie = QMovie(self.gif_path)
        self.gif_label.setMovie(movie)
        movie.start()

        # Wait 3 seconds before showing the buttons for user input
        QTimer.singleShot(10000, self.ask_for_input)

    def ask_for_input(self):
        """Ask the user to input their guess using buttons."""
        self.gif_label.movie().stop()  # Stop the GIF after it's displayed
        self.gif_label.hide()  # Hide the GIF
        self.button_widget.show()  # Show the grid of buttons for input
        self.create_buttons()

    def handle_button_click(self):
        """Handle button click event and check the user's guess."""
        clicked_button = self.sender()  # Get the button that was clicked
        guess = clicked_button.text()

        if guess == self.rand_num:
            self.instruction.setText("Correct!")
        else:
            self.instruction.setText(f"Wrong! It was {self.rand_num}. Try again!")

        self.instruction.show()

        # Hide buttons and restart the cycle after showing feedback
        self.button_widget.hide()

        QTimer.singleShot(3000, self.show_number)
    def show(self):
        self.showMaximized()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Sequence()
    window.setWindowTitle("Dyslexia")
    window.showMaximized()
    app.exec()
