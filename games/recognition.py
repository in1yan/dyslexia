from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QGraphicsBlurEffect
import random
import sys

class charRecognition(QWidget):
    def __init__(self):
        super().__init__()
        self.blur_val = 50  # Initial blur value
        self.chars = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]  # Digits + Uppercase letters
        self.setWindowTitle("Fuzzy Character Game")
        self.setStyleSheet("background-color: white;")
        self.guess_made = False  # To track if the player made a guess before timeout
        self.result_displayed = False  # To track if result is currently displayed

        # Layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Character label
        self.char = QLabel(self)
        self.char.setAlignment(Qt.AlignCenter)
        self.char.setStyleSheet("font-size: 150px;")  # Large font size for the character
        self.blur = QGraphicsBlurEffect()
        self.blur.setBlurRadius(self.blur_val)  # Initial blur radius
        self.char.setGraphicsEffect(self.blur)
        self.layout.addWidget(self.char)
        # control instruct

        self.control_instruct = QLabel("\"Press enter or space to continue\"", self)
        self.control_instruct.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.control_instruct.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.control_instruct)
        # Instruction label
        self.instruction = QLabel("\"Select the character you see\"", self)
        self.instruction.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.instruction.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.instruction)

        # Answer label for showing the correct answer after the guess
        self.ans = QLabel("")
        self.ans.setAlignment(Qt.AlignCenter)
        self.ans.setStyleSheet("font-size: 150px;")
        self.layout.addWidget(self.ans)

        # Grid layout for buttons (options to choose from)
        self.button_grid = QGridLayout()
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_grid)
        self.layout.addWidget(self.button_widget)

        # Create buttons for options
        self.buttons = []

        # Start the game by showing a fuzzy character
        self.show_fuzzy_character()

    def create_buttons(self):
        """Create buttons with random choices including the correct character."""
        random_choices = random.sample(self.chars, 3)  # Random choices
        random_choices.append(self.rand_char)  # Include the correct one
        random.shuffle(random_choices)  # Shuffle the choices

        positions = [(i, j) for i in range(2) for j in range(2)]  # 2x2 grid layout

        for i, char in enumerate(random_choices):
            button = QPushButton(char)
            button.setStyleSheet("font-size: 30px; padding: 20px;")
            button.clicked.connect(self.handle_button_click)
            self.buttons.append(button)
            row, col = positions[i]
            self.button_grid.addWidget(button, row, col)

    def show_fuzzy_character(self):
        """Display a random character with reduced visibility (blur)."""
        self.rand_char = str(random.choice(self.chars))  # Random character
        self.char.setText(self.rand_char)
        self.char.show()
        self.ans.hide()  # Hide answer label initially
        self.control_instruct.hide()
        self.instruction.setText("\"Select the character you see\"")
        self.instruction.show()
        self.guess_made = False  # Reset guess flag
        self.result_displayed = False  # Result is not displayed yet

        # Create buttons for options
        self.buttons.clear()
        for i in reversed(range(self.button_grid.count())):
            self.button_grid.itemAt(i).widget().setParent(None)  # Remove existing buttons
        self.create_buttons()

        self.button_widget.show()

        # Gradually reduce blur every 0.5 second
        self.blur_val = 50  # Reset blur value
        self.change_blur_val()

    def change_blur_val(self):
        """Gradually reduce the blur effect."""
        if self.blur_val > 0:
            self.blur_val -= 5
            self.blur.setBlurRadius(self.blur_val)
            QTimer.singleShot(3000, self.change_blur_val)  # Continue reducing blur
        else:
            # After blur is removed, check if the player made a guess
            if not self.guess_made:
                self.instruction.setText("Time ran out! Try Again!")
                self.ans.setText(self.rand_char)  # Show the correct answer on timeout
                self.clear_screen_and_show_result()

    def handle_button_click(self):
        """Handle the button click event and check if the guess is correct."""
        self.guess_made = True  # Mark that the player made a guess
        clicked_button = self.sender()
        guess = clicked_button.text()

        if guess == self.rand_char:
            self.instruction.setText("Correct!")
            self.ans.setText("")
        else:
            self.instruction.setText(f"Wrong! The correct answer was:")
            self.ans.setText(self.rand_char)

        # Show the result and restart the game after 3 seconds
        self.clear_screen_and_show_result()

    def clear_screen_and_show_result(self):
        """Clear the screen and show the result (correct/wrong)."""
        self.char.hide()  # Hide the character label
        self.button_widget.hide()  # Hide buttons
        self.instruction.show()
        self.control_instruct.show()
        self.ans.show()
        self.result_displayed = True  # Set result flag to True, waiting for user interaction

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Restart the game if Enter key is pressed and result is displayed
            if self.result_displayed:
                self.show_fuzzy_character()

    def show(self):
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = charRecognition()
    window.showMaximized()
    app.exec()
