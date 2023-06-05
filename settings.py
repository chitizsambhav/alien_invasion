class Settings():

    def __init__(self):
        self.bg_color = (230, 230, 230)
        self.screen_width = 1536
        self.screen_height = 864
        self.ship_speed_factor = 1.5
        # Bullet Settings
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_speed = 1
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.alien_speed_factor = .5
        self.alien_fleet_drop = 10
        self.alien_fleet_direction = 1
