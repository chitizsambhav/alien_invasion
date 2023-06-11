class Settings():

    def __init__(self):
        self.bg_color = (230, 230, 230)
        self.screen_width = 1536
        self.screen_height = 864
        # Bullet Settings
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_speed = 1
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.alien_fleet_drop = 10
        self.ship_limit = 2
        self.speedup_scale = 1.5
        self.score_scale = 1.5
        self.initialize_dynmaic_settings()

    def initialize_dynmaic_settings(self):
        self.alien_speed_factor = 1
        self.bullet_speed = 3
        self.ship_speed_factor = 2
        self.alien_fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_points = int(self.score_scale*self.alien_points)
