import arcade

class FireEnemyObject(arcade.Sprite):
    

    def __init__(self,max_health,health,mv_speed,damage,adaptation):
        
        super().__init__()
        
        self.rotation = 0
        self.updates_per_frame = 7
        self.max_health = max_health
        self.health = health
        self.mv_speed = mv_speed
        self.adaptation = adaptation
        self.face_right = 0
        self.face_left = 1
        self.character_face_direction = self.face_left
        self.character_scale = 1
        self.current_texture = 0
        self.updates_per_frame = 7

        self.fire_sprite = arcade.Sprite("C:\\Users\\Dell\\Desktop\\Pylam\\Project\\Sprites\\player.png")