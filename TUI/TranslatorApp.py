import npyscreen
from TUI.MainForm import MainForm

class TranslatorApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", MainForm, name="Google Translator - TUI")
