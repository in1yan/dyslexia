from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout
import random
import sys

class pairSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.chars = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]  # Digits + Uppercase letters
        self.setWindowTitle("Pair Selection")
        self.setStyleSheet("background-color: white;")
        self.guess_made = False  # To track if the player made a guess before timeout
        self.result_displayed = False  # To track if result is currently displayed
        self.pair_count = 0  # To track correct matching pairs

        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Character label
        self.char = QLabel(self)
        self.char.setAlignment(Qt.AlignCenter)
        self.char.setStyleSheet("font-size: 30px;")  # Font size for the character pair
        self.layout.addWidget(self.char)

        # Control instruction label
        self.control_instruct = QLabel("\"Press Enter or Space to continue\"", self)
        self.control_instruct.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.control_instruct.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.control_instruct)

        # Instruction label
        self.instruction = QLabel("\"Select the matching pairs\"", self)
        self.instruction.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.instruction.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.instruction)

        # Grid layout for buttons (options to choose from)
        self.button_grid = QGridLayout()
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_grid)
        self.layout.addWidget(self.button_widget)

        # Create buttons for options
        self.buttons = []

        # Start the game by showing a random pair of characters
        self.show_random_pair()

    def create_buttons(self):
        """Create buttons with random choices including the correct character pair."""
        self.random_choices = [''.join(random.sample(self.chars, 2)) for i in range(11)]  # Random choices
        self.random_choices += [self.rand_char] * 5  # Include the correct one 5 times
        random.shuffle(self.random_choices)  # Shuffle the choices

        positions = [(i, j) for i in range(4) for j in range(4)]  # 4x4 grid layout

        for i, char in enumerate(self.random_choices):
            button = QPushButton(char)
            button.setStyleSheet("font-size: 30px; padding: 20px;")
            button.clicked.connect(self.handle_button_click)
            self.buttons.append(button)
            row, col = positions[i]
            self.button_grid.addWidget(button, row, col)

    def show_random_pair(self):
        """Display a random character pair."""
        self.rand_char = ''.join(random.sample(self.chars, 2))  # Random pair of characters
        self.char.setText(f"Find the pair: {self.rand_char}")
        self.char.show()
        self.control_instruct.hide()
        self.instruction.setText("\"Select the matching pairs\"")
        self.instruction.show()
        self.guess_made = False  # Reset guess flag
        self.result_displayed = False  # Result is not displayed yet
        self.pair_count = 0  # Reset correct pair count

        # Create buttons for options
        self.buttons.clear()
        for i in reversed(range(self.button_grid.count())):
            self.button_grid.itemAt(i).widget().setParent(None)  # Remove existing buttons
        self.create_buttons()

        self.button_widget.show()

    def handle_button_click(self):
        """Handle the button click event and check if the guess is correct."""
        clicked_button = self.sender()
        guess = clicked_button.text()

        if guess == self.rand_char:
            self.pair_count += 1  # Increment correct pair count
            clicked_button.setStyleSheet("background-color: green; font-size: 30px; padding: 20px;")  # Highlight correct match
            clicked_button.setEnabled(False)  # Disable correct button
            if self.pair_count == 5:  # All 5 pairs found
                self.instruction.setText("All pairs found! Well done!")
                self.clear_screen_and_show_result()
        else:
            self.instruction.setText("That's not a matching pair, try again.")

    def clear_screen_and_show_result(self):
        """Clear the screen and show the result (all correct pairs found)."""
        self.char.hide()  # Hide the character label
        self.button_widget.hide()  # Hide buttons
        self.instruction.show()
        self.control_instruct.show()
        self.result_displayed = True  # Set result flag to True, waiting for user interaction

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Space:
            # Restart the game if Enter or Space key is pressed and result is displayed
            if self.result_displayed:
                self.show_random_pair()

    def show(self):
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pairSelection()
    window.showMaximized()
    app.exec()
