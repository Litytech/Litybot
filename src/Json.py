import json
import random

class Json:
    """
        Class with the logic for manipulate a json object
        @author José Cruz
        @version 1.0
    """

    def __init__(self):
        self.inspireme = None
        self.readJson()
    
    def readJson(self):
        """Read the json file"""
        with open('assets\inspireList.json', encoding='utf-8') as file:
            data = json.load(file)
            self.inspireme = data['inspire']

    def randomInspire(self):
        """Get a ramdon inspirational phrase"""
        request = random.choice(self.inspireme)
        return request

        