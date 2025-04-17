import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer

# Set the root directory as a traversable path
DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if DIR_PATH not in sys.path:
    sys.path.insert(0, DIR_PATH)

from TerminAI.utils.config import Config
from TerminAI.models.generic_ import generate_generic_response

os.environ["QT_QPA_PLATFORM"] = "wayland"

class ModernTerminal(QWidget):
    '''
    The terminal class, has the following important functions

    1. init_ui --> Define the UI here, the colors, size and everything goes here
    2. append_prompt --> This is defining the prompt bar, which tells the username, current directory and host
    3. init_start --> Here we show the user the "generating response..." message, NEED to fix the delay's here!
    4. model_json --> Here we are calling the json creation and upgrading models. MAKE IT A BETTER NAME!
    5. execute --> Call the relevant models and execute in the sequence defined by the queue.
    6. display_response --> Here we display whatever we need too. UPDATE THIS AS WELL WITH concat.
    '''

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_processing = False
        self.current_prompt = ""                       # Store the current prompt text for reuse

    def init_ui(self):
        ''' Terminal setup. For changing the color scheme and more, refer here.
        '''

        self.setWindowTitle(Config.terminal.title)
        self.setGeometry(100, 100, Config.terminal.d_length, Config.terminal.d_breadth)

        # Setting up the main layout, setContentsMargins() defines the borders and the whitespacing.
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Terminal display area
        self.terminal_display = QTextEdit()
        self.terminal_display.setReadOnly(True)
        self.terminal_display.setStyleSheet("""
            QTextEdit {
                background-color: #999999;
                color: #000000;
                border: none;
                padding: 0px;
            }
        """)
        self.terminal_display.setFont(QFont(Config.terminal.font, Config.terminal.font_size))

        # Modifying the input field, this is the space where we enter our prompts.
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont(Config.terminal.font, Config.terminal.font_size))
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid black;    /* Black border */
                border-radius: 3px;         /* Rounded corners */
                padding: 0px;               /* Inner padding */
                background-color: #999999;  /* Background color of the input field same as the general background */
                color: black;               /* Text color */
            }
        """)
        self.input_field.returnPressed.connect(self.init_start)

        self.main_layout.addWidget(self.terminal_display, stretch=1)                # Stretch just means expand this thing till 0 padding.
        self.main_layout.setSpacing(0)                                              # Remove whitespace between the others and input field.
        self.main_layout.addWidget(self.input_field, stretch=0)

        self.setLayout(self.main_layout)
        
        # Setting up the prompt bar 
        self.append_prompt()

    def append_prompt(self):
        ''' 
        Keeping it simple with this one, just the username, hostname (that we didn't use), and the current directory.
        - In the future we can try adding color coding and git status?
        - Allow users to configure it using config
        '''

        user = os.getenv("USER", 'user')        # We get the user name from here. We should probably pass this to the models as well
        host = os.uname().nodename
        current_dir = os.getcwd()
        home = os.path.expanduser("~")
        if current_dir.startswith(home):
            current_dir = "~" + current_dir[len(home):]

        # Keeping everything black, except the "$" sign which is white. Looks aesthetic!
        prompt_text = (
            f'<span style="color: #000000;">{user}</span>'
            f'<span style="color: #000000;">@UB</span>:'
            f'<span style="color: #000000;">{current_dir}</span>'
            f' <span style="color: #FFFFFF;">$</span> '
        )

        self.terminal_display.append(prompt_text)
        self.terminal_display.moveCursor(QTextCursor.End)


    def process(self, prompt):
        # Testing the generic response
        return generate_generic_response(prompt, [])

    def init_start(self):
        '''
        This does the following things
            1. If the user enters 'clear' then we clear the screen and change the processing boolean
            2. This appends the prompt bar and calls the "generating response..." text while we process in the behind 
            3. Ensures that the cursor stays at the bottom of the screen
            4. Then calls the worker class for processing

        Finally it clears the input field for new prompts.
        '''

        if self.is_processing:
            return

        self.is_processing = True
        self.current_prompt = self.input_field.text()

        if self.current_prompt.strip():
            # We'll have to clear the terminal here... if the user enters clear 

            if self.current_prompt.strip().lower() == "clear":
                # No need to call the worker class here
                
                self.terminal_display.clear()                       # Clear the terminal
                self.append_prompt()                                # Adding the prompt bar again
                self.is_processing = False                          # Resetting the status
                self.input_field.clear()                            # Clearing the input field
                
                return

            # First we insert the prompt in the right place
            self.terminal_display.insertPlainText(self.current_prompt + "\n")
            
            # Calling the generating response part here, in a seperate thread.
            self.terminal_display.append(
                f'<span style="color: #FFB86C;">{Config.terminal.stall_message}</span>'
            )
            self.terminal_display.moveCursor(QTextCursor.End)       # Ensuring that the cursor stays at the bottom
            QApplication.processEvents()

            output = self.process(self.current_prompt)
            self.display_response(output)
        self.input_field.clear()


    def display_response(self, results):
        ''' This function is being used to display the final processed output from the results list '''

        cursor = self.terminal_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.select(QTextCursor.LineUnderCursor)
        
        cursor.removeSelectedText()
        cursor.deletePreviousChar()

        formatted_output = f"\n <span style='color: #007ACC;'>{Config.terminal.Name}</span> {results} \n"

        self.terminal_display.append(f"<pre>{formatted_output}</pre>")

        # Then we add the prompt bar again for the next input
        self.append_prompt()
        self.is_processing = False          # Keep track of stuff man


app = QApplication(sys.argv)
terminal = ModernTerminal()
terminal.show()
sys.exit(app.exec_())
