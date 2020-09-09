import arcade, math, random

def load_texture_pair(filename):
    """ Handles textures """

    return[
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class Enemy(arcade.Sprite):
    

    def __init__(self,health,mv_speed,type,fire_damage):
        
        super().__init__()
        
        # Player attributes.
        self.bullet_speed = 5
        self.rotation = 0
        self.updates_per_frame = 7
        self.health = health
        self.mv_speed = mv_speed
        self.type = type
        self.face_right = 0
        self.face_left = 1
        self.character_face_direction = self.face_left
        self.character_scale = 1
        self.current_texture = 0
        self.updates_per_frame = 7
        self.walls_hit = []
        self.fire_damage = fire_damage

        # Handles enemy sprites according to the enemy's type.
        if self.type == "Leech":
            self.sprite = arcade.Sprite("Sprites/leech_enemy.png")
            self.idle_sprite = load_texture_pair("Sprites/leech_enemy.png")
        elif self.type == "Slime":
            self.sprite = arcade.Sprite("Sprites/slime_enemy.png")
            self.idle_sprite = load_texture_pair("Sprites/slime_enemy.png")
        else:
            self.sprite = arcade.Sprite("Sprites/fire_enemy.png")
            self.idle_sprite = load_texture_pair("Sprites/fire_enemy.png")
        self.walk_textures = []
        for i in range(1,2,1):
            if self.type == "Leech":
                texture = load_texture_pair("Sprites/leech_enemy_mv" + str(i)+".png")
            elif self.type == "Slime":
                texture = load_texture_pair("Sprites/slime_enemy_mv"+str(i)+".png")
            else:
                texture = load_texture_pair("Sprites/fire_enemy_mv"+str(i)+".png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float=1/60):
        """ Handles possible animations""" 

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
        """ Allows the enemy to chase the player. """

        self.player = player
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.mv_speed < 0:
            self.mv_speed = 0

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
    
    def check_wall_collision(self,wall_list):
        """ Handles enemy collision. """

        self.wall_list = wall_list
        walls_hit = []
        walls_hit += arcade.check_for_collision_with_list(self, self.wall_list)

        for wall in walls_hit:
                if self.change_x > 0:
                    self.right = wall.left
                elif self.change_x < 0:
                    self.left = wall.right
        if len(walls_hit) > 0:
            self.change_x *= -1

        self.center_y += self.change_y
        walls_hit = arcade.check_for_collision_with_list(self, self.wall_list)
        for wall in walls_hit:
            if self.change_y > 0:
                self.top = wall.bottom
            elif self.change_y < 0:
                self.bottom = wall.top
        if len(walls_hit) > 0:
            self.change_y *= -1
    
    def aim(self,player):
        """ Makes the enemy aim at the player. """

        self.player = player

        self.start_x = self.center_x
        self.start_y = self.center_y

        self.dest_x = self.player.center_x
        self.dest_y = self.player.center_y

        x_diff = self.dest_x - self.start_x
        y_diff = self.dest_y - self.start_y

        self.angle = math.atan2(y_diff,x_diff)

        self.angle = math.degrees(self.angle) - 90

    def take_damage(self,bullet_damage):
        """ Handles damage taken and health point reduction. """

        self.bullet_damage = bullet_damage
        self.health -= self.bullet_damage
            


