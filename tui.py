import npyscreen
import curses

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Google Translator - TUI")

class TestBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield

class MainForm(npyscreen.FormBaseNew):
    def create(self):
        # set event handler
        event_handlers = {
            # ALT + ENTER -> send request
            curses.ascii.alt(curses.ascii.NL): self.send_text
        }
        self.add_handlers(event_handlers)

        # get terminal's size
        y, x = self.useable_space()

        self.input = self.add(TestBox, name="Input (from)", footer="Footer", 
            max_width=x//2-3, max_height=y-5, relx=3, rely=3, value="{} {}".format(x, y))
        
        self.output = self.add(TestBox, name="Output (to)", footer="Footer",
            max_width=x//2-3, max_height=y-5, relx=x//2+1, rely=3, editable=False)
    
    def resize(self):
        '''
            resize the form when the terminal is resizing
            This function will be called by npyscreen automatically.
        '''
        # get terminal's size
        y, x = self.useable_space()

        # change input's size
        self.input.max_width = x//2-3
        self.input.max_height = y//2

        # change output's size & location
        self.output.max_width = x//2-3
        self.output.max_height = y//2
        self.output.relx = x//2+1  # location(x)

        # Output's contained widget, TextField must be move to a new position
        self.output.entry_widget.relx = x//2+2
    
    def send_text(self, event):
        # When press ALT + ENTER, send request & update output's text
        self.output.entry_widget.value = self.input.value
        self.output.entry_widget.display()

def main():
    TA = MyTestApp()
    TA.run()

if __name__ == '__main__':
    main()
