import npyscreen
import curses
from Sound import Sound
from TUI.Box import EditBox

readme = '''
        █▀▀ █▀█ █▀█ █▀▀ █░░ █▀▀ ▄▄ ▀█▀ █▀█ ▄▀█ █▄░█ █▀ █░░ ▄▀█ ▀█▀ █▀▀   ▀█▀ █░█ █
        █▄█ █▄█ █▄█ █▄█ █▄▄ ██▄ ░░ ░█░ █▀▄ █▀█ █░▀█ ▄█ █▄▄ █▀█ ░█░ ██▄   ░█░ █▄█ █
        
        This is an unofficial Google Translate client.
        It use Google Translate's API(free), so it may not work when you send too many requests.

        It just a practice for npyscreen, this respository may not update any more.

        - General
        -    ^Q           :         Quit
        -    ALT + ENTER  :         Search
        -    CTRL + T     :         Swap language
        -    CTRL + D     :         Delete all input
        -    CTRL + S     :         Select Language
        -
        - Sound
        -    CTRL + K     :         Play left sound
        -    CTRL + L     :         Play right sound
'''

class MainForm(npyscreen.FormBaseNew):

    def while_waiting(self):
        if not self.lock:
            self.DISPLAY()
        else:
            self.lock = True

    def create(self):
        self.keypress_timeout = 5

        # lock is for INPUT's DISPLAY() updatting
        self.lock = False

        def inputUpdate():
            self.lock = False

        # set event handler
        event_handlers = {
            # send request
            curses.ascii.alt(curses.ascii.NL): self.send_text,
            
            #exit
            "^Q": self.exit_app,

            # delete all input
            "^D": self.remove_text,

            # select language
            "^S": self.change_language,

            # play sound on the left window
            "^K": self.play_left,
            
            # play sound on the right window
            "^L": self.play_right,

            # reverse language
            "^T": self.reverse_language
        }
        self.add_handlers(event_handlers)

        # get terminal's size
        y, x = self.useable_space()

        self.input = self.add(EditBox, name="Input (from)", footer=self.parentApp.translator.inputLanguage, 
            max_width=x//2-5, max_height=y//3,
            relx=3, rely=3,
            value="Hello world"
        )
        
        # avoid some language input error
        # ex. Chinese
        self.input.entry_widget.when_value_edited = inputUpdate

        self.output = self.add(EditBox, name="Output (to)", footer=self.parentApp.translator.outputLanguage,
            max_width=x//2-5, max_height=y//3,
            relx=x//2+2, rely=3,
            value="你好，世界",
            editable=False
        )

        self.readme = self.add(EditBox, name="README",
            max_width=x-5, max_height=y//3*2-6,
            relx=3, rely=y//3+4,
            value=readme,
            editable=False
        )
    
    def resize(self):
        '''
            resize the form when the terminal is resizing
            This function will be called by npyscreen automatically.
        '''
        # get terminal's size
        y, x = self.useable_space()

        # change input's size
        self.input.max_width = x//2-5
        self.input.max_height = y//3

        # change output's size & location
        self.output.max_width = x//2-5
        self.output.max_height = y//3

        self.output.relx = x//2+2  # location(x)

        # change README's size & location
        self.readme.max_width = x-5
        self.readme.max_height = y//3*2-6
        self.readme.rely = y//3+4

        # Output and README's contained widget, TextField must be move to a new position
        self.output.entry_widget.relx = x//2+3
        self.readme.entry_widget.rely = y//3+5

        self.input.footer = self.parentApp.translator.inputLanguage
        self.output.footer = self.parentApp.translator.outputLanguage
    
    def send_text(self, event):
        '''
            use self.translator to send the request to Google Translate
            then update the response to self.output
        '''
        # When press ALT + ENTER, send request & update output's text
        if self.input.value != "":
            try:
                targetText = self.parentApp.translator.translate(self.input.value.replace('\n', ' '))
            except:
                targetText = ["This is not a true translation, there exist an error."]

            finally:
                text = ""
                for i in targetText:
                    text = text + i + "\n"
                self.output.value = text

                # refresh entire form
                # Though npyscreen's documentation mention that we should avoid using DISPLAY() function
                # I can't display Chinese or Japanese,etc correctly when I didn't use this function.
                self.DISPLAY()

    def play_left(self, event):
        if self.input.value != "":
            message = self.input.value
            language = self.parentApp.translator.fr
            Sound().play(message, language)
        
    def play_right(self, event):
        if self.output.value != "":
            message = self.output.value
            language = self.parentApp.translator.to
            Sound().play(message, language)

    def reverse_language(self, event):

        translator = self.parentApp.translator
        
        translator.to, translator.fr = translator.fr, translator.to
        translator.inputLanguage, translator.outputLanguage = translator.outputLanguage, translator.inputLanguage

        self.input.value, self.output.value = self.output.value, self.input.value

        self.input.footer = translator.inputLanguage
        self.input.update()

        self.output.footer = translator.outputLanguage
        self.output.update()

    def remove_text(self, event):
        self.input.value = ""
        self.input.update()

    def exit_app(self, event):
        exit(0)
    
    def change_language(self, event):
        self.parentApp.switchForm("LANGUAGE")
