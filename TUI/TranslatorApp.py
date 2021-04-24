import npyscreen
from TUI.MainForm import MainForm
from TUI.LanguageForm import LanguageForm
from GoogleTranslator import GoogleTranslator
from config import config

class TranslatorApp(npyscreen.NPSAppManaged):

    translator = GoogleTranslator(config['inputLanguage'], config['outputLanguage'])

    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", MainForm, name="Google Translator - TUI")
        self.addForm("LANGUAGE", LanguageForm, name="LANGUAGE CHOOSE")