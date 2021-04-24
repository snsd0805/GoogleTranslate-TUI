import requests
import re
from urllib.parse import quote

class GoogleTranslator():
    def __init__(self, fr, to):
        # set up
        self.languageCode = {}
        self.fr = fr
        self.to = to
        self.inputLanguage = ""
        self.outputLanguage = ""

        self.loadLanguageCode()

        self.URL = "https://translate.google.com.tw/_/TranslateWebserverUi/data/batchexecute?\
            rpcids=MkEWBc&\
            f.sid=4622116653376551039&\
            bl=boq_translate-webserver_20210414.13_p0&\
            hl=zh-TW&\
            soc-app=1&\
            soc-platform=1&\
            soc-device=1&\
            _reqid=1737851&\
            rt=c"

        self.HEADER = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }

        # can't sure whether it works for everyone, token in this URL might been blocked.
        self.DATA = "f.req=%5B%5B%5B%22MkEWBc%22%2C%22%5B%5B%5C%22{}%5C%22%2C%5C%22{}%5C%22%2C%5C%22{}%5C%22%2Ctrue%5D%2C%5Bnull%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at=AD08yZn6jdbpV8qLjfergSwRT4IO%3A1618543754261&"

    def loadLanguageCode(self):
        with open('LanguageCode.csv') as fp:
            data = fp.readlines()
            data = [line.replace('\n', '') for line in data]
        
        for line in data:
            country, code = line.split(',')
            self.languageCode[country] = code
            if code==self.fr: self.inputLanguage = country
            if code==self.to: self.outputLanguage = country

    def translate(self, text):
        '''
            return a string which translate from self.fr to self.to
        '''
        # send request
        text = quote(text)
        response = requests.post(
            self.URL,
            data=self.DATA.format(text, self.fr, self.to), 
            headers=self.HEADER
        )
        lines = response.text.split('\n')
        targetLine = ""
        for i in range(2, len(lines)):
            targetLine += lines[i]

        # replace useless char
        # change JSON format to Python format because we will use this string to generate Python code
        replaceDict = {
            '\\n': '',
            'null': 'None',
            'true': 'True',
            'false': 'False'
        }
        for item in replaceDict:
            targetLine = targetLine.replace(item, replaceDict[item])

        # get information block
        data = eval(targetLine)
        data = eval(data[0][2])
        
        ans = []
        for i in data[1][0][0][5]:
            ans.append(i[0])
        return ans
