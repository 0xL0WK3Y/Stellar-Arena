import arcade, math, random

def load_texture_pair(filename):

    return[
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

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
        self.idle_sprite = load_texture_pair("C:\\Users\\Dell\\Desktop\\Pylam\\Arcade\\Sprites\\player.png")

        self.walk_textures = []
        for i in range(1,2,1):
            texture = load_texture_pair("C:\\Users\\Dell\\Desktop\\Pylam\\Arcade\\Sprites\\player_move_"+str(i)+".png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float=1/60):
        
        if self.change_x < 0 and self.character_face_direction == self.face_right:
            self.character_face_direction = self.face_left
        elif self.change_x > 0 and self.character_face_direction == self.face_left:
            self.character_face_direction = self.face_right
            
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_sprite[0]
            return
        if self.current_texture > 2 * self.updates_per_frame:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture // self.updates_per_frame][self.character_face_direction]


    def chase_player(self, player):

        self.player = player

        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:

            start_x = self.center_x
            start_y = self.center_y

            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * self.mv_speed
            self.change_y = math.sin(angle) * self.mv_speed
            


