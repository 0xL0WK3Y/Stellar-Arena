import arcade

def load_texture_pair(filename):
    """ Handles textures """
    
    return[
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class PlayerCharacter(arcade.Sprite):
    
    
    
    def __init__(self,health,mv_speed,adaptation,adaptation_uses):

        super().__init__()
        
        # Player attributes.
        self.rotation = 0
        self.updates_per_frame = 7
        self.health = health
        self.mv_speed = mv_speed
        self.adaptation = adaptation
        self.adaptation_uses = adaptation_uses
        self.bullet_damage = 25
        self.face_right = 0
        self.face_left = 1
        self.character_face_direction = self.face_left
        self.character_scale = 1
        self.current_texture = 0
        self.updates_per_frame = 7
        
        # Handles the player textures.
        self.player_sprite = arcade.Sprite("Sprites/player.png")

        self.idle_sprite = load_texture_pair("Sprites/player.png")

        self.walk_textures = []
        for i in range(1,2,1):
            texture = load_texture_pair("Sprites/player_move_"+str(i)+".png")
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

    def take_damage(self,damage_taken):
        """ Handles damage taken and health point reduction. """

        self.damage_taken = damage_taken
        self.health -= self.damage_taken
