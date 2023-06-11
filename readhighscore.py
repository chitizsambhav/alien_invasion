class ReadHighScore():
    def __init__(self):
        with open('highscore.txt') as fileobject:
            self.high_score = int(fileobject.read())
