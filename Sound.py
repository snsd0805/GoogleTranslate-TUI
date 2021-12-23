from urllib.request import urlopen
from urllib.parse import quote
from pygame import mixer
import time

class Sound:
    def __init__(self):
        self.url = "https://translate.google.com.vn/translate_tts?ie=UTF-8&q={}&tl={}&client=tw-ob"
        self.cache_file = "/tmp/translate.mp3"
        mixer.init()
    
    def play(self, message, language):
        source = urlopen(self.url.format(quote(message), language))

        # write to file
        with open(self.cache_file, "wb") as fp:
            fp.write(source.read())

        # play sound
        mixer.music.load(self.cache_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
