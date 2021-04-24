import npyscreen
import curses
from TUI.Box import EditBox, SelectBox
from config import config

class LanguageForm(npyscreen.ActionForm):
    def create(self):
        # get language list
        languages = list(self.parentApp.translator.languageCode.keys())
        codes = list(self.parentApp.translator.languageCode.values())

        # get terminal's size
        y, x = self.useable_space()

        inputDefault = languages.index(self.parentApp.translator.inputLanguage)
        outputDefault = languages.index(self.parentApp.translator.outputLanguage)

        self.input = self.add(SelectBox, name="Input Language",
            value=inputDefault,
            values=languages,
            max_height=y-5, max_width = x//2-5,
            relx=3, rely=3,
        )

        self.output = self.add(SelectBox, name="Output Language",
            value=outputDefault,
            values=languages,
            max_height=y-5, max_width = x//2-5,
            relx=x//2+3, rely=3,
        )
    
    def resize(self):
        # get terminal's size
        y, x = self.useable_space()

        self.input.max_height = y-5
        self.input_max_width = x//2-5

        self.output.max_height = y-5
        self.output.max_width = x//2-5
        self.output.relx = x//2+3
        self.output.entry_widget.relx = x//2+4
        
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def on_ok(self):
        languages = list(self.parentApp.translator.languageCode.keys())
        codes = list(self.parentApp.translator.languageCode.values())
        self.parentApp.translator.fr = codes[self.input.value[0]]
        self.parentApp.translator.to = codes[self.output.value[0]]
        self.parentApp.translator.inputLanguage = languages[self.input.value[0]]
        self.parentApp.translator.outputLanguage = languages[self.output.value[0]]
        self.parentApp.setNextForm("MAIN")