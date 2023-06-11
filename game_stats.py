class Game_stats():

    def __init__(self, ai_settings,rhs):
        self.ship_left = None
        self.ai_settings = ai_settings
        self.game_active = False
        self.reset_stats()
        if rhs.high_score==0:
            self.high_score = 0
        else:
            self.high_score = rhs.high_score

    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
