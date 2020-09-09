import arcade, math, random, timeit
from PlayerObject import PlayerCharacter
from EnemyObject import Enemy

# Here are some constant variables

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Stellar: Arena"
arena = "Maidens_Kiss.tmx"
WALL_SCALE = 1

BULLET_SPEED = 7

LEFT_VIEW_MARGIN = 250
RIGHT_VIEW_MARGIN = 250
UPPER_VIEW_MARGIN = 256
BOTTOM_VIEW_MARGIN = 50

UPDATES_PER_FRAME = 7

class ArenaSelection(arcade.View):

    """ This is the menu screen for the arena selection called by the MenuView class. """

    def on_show(self):
        """ A bit like __init__, it loads the basic textures and sounds. """

        arcade.set_background_color(arcade.color.BLACK)
        self.background_img = arcade.load_texture("Sprites/Selection.png")
        self.select_sound = arcade.load_sound("Sound/select.wav")
        self.cancel_sound = arcade.load_sound("Sound/cancel.wav")
    def on_draw(self):
        """ It renders everything """

        arcade.start_render()
        arcade.draw_xywh_rectangle_textured(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,self.background_img)
    def on_key_press(self,key,modifiers):
        """ It allows the player to select an arena by pressing the keys 1,2,3 
        or to go back by pressing backspace. """

        if (key == arcade.key.NUM_1 or key == arcade.key.KEY_1):
            arcade.play_sound(self.select_sound)
            arena = "Maidens_Kiss.tmx"
            game_view = GameView()
            game_view.setup(arena)
            self.window.show_view(game_view)
        elif (key == arcade.key.NUM_2 or key == arcade.key.KEY_2):
            arcade.play_sound(self.select_sound)
            arena = "Metallic_Pyre.tmx"
            game_view = GameView()
            game_view.setup(arena)
            self.window.show_view(game_view)
        elif (key == arcade.key.NUM_3 or key == arcade.key.KEY_3):
            arcade.play_sound(self.select_sound)
            arena = "Terminal_Stasis.tmx"
            game_view = GameView()
            game_view.setup(arena)
            self.window.show_view(game_view)
        elif (key == arcade.key.BACKSPACE):
            arcade.play_sound(self.cancel_sound)
            menu_view = MenuView()
            self.window.show_view(menu_view)
            
class InstructionsView(arcade.View):
    """ A screen which shows the player some basic information about the game. 
    Called by the MenuView class. """

    def on_show(self):
        """ A bit like __init__, it loads the basic textures and sounds. """

        arcade.set_background_color(arcade.color.BLACK)
        self.background_img = arcade.load_texture("Sprites/Instructions.png")
        self.cancel_sound = arcade.load_sound("Sound/cancel.wav")
    def on_draw(self):
        """ It renders everything. """

        arcade.start_render()
        arcade.draw_xywh_rectangle_textured(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,self.background_img)
    def on_key_press(self, key, modifiers):
        """ The player can go back to the main menu by pressing backspace. """

        if (key == arcade.key.BACKSPACE):
            arcade.play_sound(self.cancel_sound)
            menu_view = MenuView()
            self.window.show_view(menu_view)

class MenuView(arcade.View):
    """ The main menu window which appears when the game is ran. """

    def on_show(self):
        """ A bit like __init__, it loads the basic textures and sounds. """

        arcade.set_background_color(arcade.color.BLACK)
        self.background_img = arcade.load_texture("Sprites/MainMenu.png")
        self.select_sound = arcade.load_sound("Sound/select.wav")
        self.cancel_sound = arcade.load_sound("Sound/cancel.wav")

    def on_draw(self):
        """ It renders everything. """

        arcade.start_render()
        arcade.draw_xywh_rectangle_textured(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,self.background_img)
    
    def on_key_press(self, key, modifiers):
        """ The player can choose to start the game by going to the arena selection screen 
        or can look at the instructions screen. """

        if (key == arcade.key.P or key == arcade.key.SPACE):
            arcade.play_sound(self.select_sound)
            arena_selection_view = ArenaSelection()
            self.window.show_view(arena_selection_view)
        elif (key == arcade.key.I):
            arcade.play_sound(self.select_sound)
            instruction_view = InstructionsView()
            self.window.show_view(instruction_view)
            

class GameView(arcade.View):
    """ The main game window which appears when the game starts. It is called by the ArenaSelection class. """

    def __init__(self):
        """Here we instantiate some basic variables."""

        super().__init__() 
        arcade.set_background_color(arcade.color.BLACK)

        #The sprite lists.
        self.player_list = None
        self.wall_list = None
        self.floor_list = None
        self.player_spawn_list = None
        self.enemy_spawn_list = None
        self.mv_box_tile_list = None
        self.hp_box_tile_list = None
        self.ad_box_tile_list = None
        self.collision_list = None
        self.enemy_sprite_list = None
        self.bullet_sprite_list = None
        self.enemy_bullet_sprite_list = None
        
        # The locations of the enemy spawners.
        self.enemy_spawner_x_list = []
        self.enemy_spawner_y_list = []

        # Some camera variables.
        self.view_bottom = 0
        self.view_left = 0

        # Status variables
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        # Here we load the sound files.
        self.lz_fire_sound = arcade.load_sound("Sound/lz_fire.wav")
        self.lz_hit_sound = arcade.load_sound("Sound/lz_hit.wav")
        self.fr_fire_sound = arcade.load_sound("Sound/fr_fire.wav")
        self.fr_hit_sound = arcade.load_sound("Sound/fr_hit.wav")
        self.sl_fire_sound = arcade.load_sound("Sound/sl_fire.wav")
        self.sl_hit_sound = arcade.load_sound("Sound/sl_hit.wav")
        self.lc_fire_sound = arcade.load_sound("Sound/lc_fire.wav")
        self.lc_hit_sound = arcade.load_sound("Sound/lc_hit.wav")
        self.explosion_sound = arcade.load_sound("Sound/explosion.wav")
        self.defeat_sound = arcade.load_sound("Sound/defeat.wav")
        self.screech_sound = arcade.load_sound("Sound/screech.wav")
        self.meep_sound = arcade.load_sound("Sound/meep.wav")

    def setup(self,arena):
        """ This function is called when the game starts or restarts after a game over. Here we pass values to variables
        relevant to the game that may be resetted later. This is the basic function which loads everything the game
        will need. """


        # We instantiate the sprite lists. Spatial hashing is activated to increase the frame-rate.
        self.player_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.player_spawn_list = arcade.SpriteList()
        self.enemy_spawn_list = arcade.SpriteList()
        self.mv_box_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.hp_box_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.ad_box_tile_list = arcade.SpriteList(use_spatial_hash=True)
        self.collision_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_sprite_list = arcade.SpriteList(use_spatial_hash =True)
        self.enemy_bullet_sprite_list = arcade.SpriteList(use_spatial_hash=True)

        # Some important variables that will be used under and for certain conditions.
        self.max_enemies = 2
        self.enemy_num = 0
        self.credits = 0
        self.bonus_effect = 0
        self.deal_fire_damage = False
        self.arena = arena

        # The layer names for when any level gets imported.
        wall_layer_name = "Walls"
        floor_layer_name = "Floor"
        player_spawner_name = "PlayerSpawner"
        enemy_spawner_name = "EnemySpawner"
        mv_box_tile_layer_name = "MVBox"
        hp_box_tile_layer_name = "HPBox"
        ad_box_tile_layer_name = "ADBox"

        # Here we import the level and process every layer according to their name.
        game_arena = arcade.tilemap.read_tmx(self.arena)
        self.wall_list = arcade.tilemap.process_layer(game_arena,wall_layer_name,WALL_SCALE)
        self.floor_list = arcade.tilemap.process_layer(game_arena,floor_layer_name,WALL_SCALE)
        self.player_spawn_list = arcade.tilemap.process_layer(game_arena,player_spawner_name,WALL_SCALE)
        self.enemy_spawn_list = arcade.tilemap.process_layer(game_arena,enemy_spawner_name,WALL_SCALE)
        self.mv_box_tile_list = arcade.tilemap.process_layer(game_arena,mv_box_tile_layer_name,WALL_SCALE)
        self.hp_box_tile_list = arcade.tilemap.process_layer(game_arena,hp_box_tile_layer_name,WALL_SCALE)
        self.ad_box_tile_list = arcade.tilemap.process_layer(game_arena,ad_box_tile_layer_name,WALL_SCALE)

        # The list of every sprite that can collide with the player.
        for sprite in self.wall_list:
            self.collision_list.append(sprite)

        # Here we create the player.
        self.player = PlayerCharacter(100,4,"Lazer",15)
        for spawner in self.player_spawn_list:
            self.player.center_x = spawner.center_x
            self.player.center_y = spawner.center_y
        self.player_list.append(self.player)

        # We find the location of every enemy spawner.
        for spawner in self.enemy_spawn_list:
            self.enemy_spawner_x_list.append(spawner.center_x)
            self.enemy_spawner_y_list.append(spawner.center_y)

        # We give the arena the background color of the map.
        if game_arena.background_color:
            arcade.set_background_color(game_arena.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.collision_list,0) # Instantiating the physics engine.

    def on_draw(self):
        """ This function renders everything on screen. """

        arcade.start_render()
        draw_start_time = timeit.default_timer

        # We render the sprite lists.
        self.wall_list.draw()
        self.floor_list.draw()
        self.enemy_spawn_list.draw()
        self.player_spawn_list.draw()
        self.bullet_sprite_list.draw()
        self.enemy_bullet_sprite_list.draw()
        self.mv_box_tile_list.draw()
        self.hp_box_tile_list.draw()
        self.ad_box_tile_list.draw()

        # Drawing some UI.
        score_text = f"Credits: {self.credits}"
        health_text = f"HP: {self.player.health}"
        bullet_text = "Bullets: Infinite"
        lazer_icon = arcade.load_texture("Sprites/lazer_icon.png")
        fire_icon = arcade.load_texture("Sprites/fire_icon.png")
        slime_icon = arcade.load_texture("Sprites/slime_icon.png")
        leech_icon = arcade.load_texture("Sprites/leech_icon.png")

        if self.player.adaptation != "Lazer":
            bullet_text = f"Bullets: {self.player.adaptation_uses}"

        arcade.draw_text(score_text,10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)
        arcade.draw_text(health_text,10 + self.view_left, 30 + self.view_bottom, arcade.csscolor.WHITE, 18)
        arcade.draw_text(bullet_text,10 + self.view_left, 60 + self.view_bottom, arcade.csscolor.WHITE, 18)

        if self.player.adaptation == "Lazer":
            arcade.draw_xywh_rectangle_textured(10 + self.view_left, 110 + self.view_bottom, 24, 24, lazer_icon)
            arcade.draw_text("LaZer: Adapt to your enemies.", 10 + self.view_left, 90 + self.view_bottom, arcade.csscolor.WHITE,12)
        elif self.player.adaptation == "Fire":
            arcade.draw_xywh_rectangle_textured(10 + self.view_left, 110 + self.view_bottom, 24, 24, fire_icon)
            arcade.draw_text("Fire: Damage over time.", 10 + self.view_left, 90 + self.view_bottom, arcade.csscolor.WHITE,12)
        elif self.player.adaptation == "Slime":
            arcade.draw_xywh_rectangle_textured(10 + self.view_left, 110 + self.view_bottom, 24, 24, slime_icon)
            arcade.draw_text("Slime: Slow them down.", 10 + self.view_left, 90 + self.view_bottom, arcade.csscolor.WHITE,12)
        elif self.player.adaptation == "Leech":
            arcade.draw_xywh_rectangle_textured(10 + self.view_left, 110 + self.view_bottom, 24, 24, leech_icon)
            arcade.draw_text("Leech: Absorb their life.", 10 + self.view_left, 90 + self.view_bottom, arcade.csscolor.WHITE,12)

        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()

    
        if self.fps is not None:
            fps_text = f"FPS: {self.fps:.0f}"
            arcade.draw_text(fps_text, 10 + self.view_left, 620 + self.view_bottom, arcade.csscolor.WHITE, 16)
        
        # Rendering the player.
        try:
            self.player_list.draw()
            self.enemy_sprite_list.draw()
           
        except Exception as e:
            print(str(e))
    
    def on_key_press(self,key,modifiers):
        """ Handles player movement. Makes the player move when a movement key is pressed."""
       
        if (key == arcade.key.UP or key == arcade.key.W):
            self.player.change_y = self.player.mv_speed
        elif (key == arcade.key.DOWN or key == arcade.key.S):
            self.player.change_y = -self.player.mv_speed
        elif (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player.change_x = self.player.mv_speed
        elif (key == arcade.key.LEFT or key == arcade.key.A):
            self.player.change_x = -self.player.mv_speed
    
    def on_key_release(self, key, modifiers):
        """ Handles player movement. Stops the player when a movement key is released. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        
    def on_mouse_press(self,x,y,button,modifiers):
        """ Allows the player to shoot bullets. """

        # When the player uses all of their enhanced bullets, return to their weapons to default.
        if self.player.adaptation_uses <= 0:
            self.player.adaptation = "Lazer"
            self.player.adaptation_uses = 15

        # Changes the sprite of the player's bullets according to the player's adaptation.
        if (self.player.adaptation == "Lazer"):
            bullet = arcade.Sprite("Sprites/lz_bullet.png")
            arcade.play_sound(self.lz_fire_sound)
            self.bullet_sprite_list.append(bullet)
        elif (self.player.adaptation == "Fire") and (self.player.adaptation_uses > 0):
            bullet = arcade.Sprite("Sprites/fire_bullet.png",1)
            arcade.play_sound(self.fr_fire_sound)
            self.bullet_sprite_list.append(bullet)
        elif((self.player.adaptation == "Slime") and (self.player.adaptation_uses > 0)):
            bullet = arcade.Sprite("Sprites/slime_bullet.png",1)
            arcade.play_sound(self.sl_fire_sound)
            self.bullet_sprite_list.append(bullet)
        elif((self.player.adaptation == "Leech") and (self.player.adaptation_uses > 0)):
            bullet = arcade.Sprite("Sprites/leech_bullet.png",1)
            arcade.play_sound(self.lc_fire_sound)
            self.bullet_sprite_list.append(bullet)

        # Handle the shooting mechanic
        start_x = self.player.center_x
        start_y = self.player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y 

        dest_x = x + self.view_left
        dest_y = y + self.view_bottom
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
       
        angle = math.atan2(y_diff, x_diff)
        
        bullet.angle = math.degrees(angle)
        
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Reduce the player's adaptation uses every time they shoot and enhanced bullet.
        if self.player.adaptation != "Lazer":
            self.player.adaptation_uses -= 1


      
    def on_update(self,delta_time):
        """ Does something every time a frame changes. """

        self.frame_count += 1

        # Update the sprite lists and the physics.
        self.bullet_sprite_list.update()
        self.enemy_bullet_sprite_list.update()
        self.player_list.update()
        self.player.update_animation()
        self.enemy_sprite_list.update()
        self.enemy_sprite_list.update_animation()
        self.physics_engine.update()

        # Make sure the enemy number does not go below zero.
        if self.enemy_num < 0:
            enemy_num = 0

        # Handles the power up "shop" mechanic.
        for mv_up in self.mv_box_tile_list:
            self.mv_box_collision = arcade.check_for_collision_with_list(mv_up, self.player_list)

            for player_collision in self.mv_box_collision:
                if self.credits >= 500:
                    self.credits -= 500
                    self.player.mv_speed += 3
                    mv_up.remove_from_sprite_lists()
        
        for hp_up in self.hp_box_tile_list:
            self.hp_box_collision = arcade.check_for_collision_with_list(hp_up, self.player_list)

            for player_collision in self.mv_box_collision:
                if self.credits >= 1000:
                    self.credits -= 1000
                    self.player.health += 550
                    hp_up.remove_from_sprite_lists()
        
        for ad_up in self.ad_box_tile_list:
            self. ad_box_collision = arcade.check_for_collision_with_list(ad_up, self.player_list)

            for player_collision in self.ad_box_collision:
                if self.credits >= 750:
                    self.credits -= 750
                    self.bonus_effect += 5
                    ad_up.remove_from_sprite_lists()

        # Handles everything that happens when the player shoots and hits an enemy. That includes dealing damage and taking effects.
        for bullet in self.bullet_sprite_list:
            self.bullet_wall_collision = arcade.check_for_collision_with_list(bullet,self.wall_list)
            self.bullet_enemy_collision = arcade.check_for_collision_with_list(bullet, self.enemy_sprite_list)

            # Remove the bullet when it collides with something.
            for bullet_collision in self.bullet_wall_collision:
                bullet.remove_from_sprite_lists()

            # Handle the bullet effects
            for bullet_collision in self.bullet_enemy_collision:
                if self.player.adaptation == "Lazer":
                    self.player.adaptation = bullet_collision.type
                    self.deal_fire_damage = False
                    arcade.play_sound(self.lz_hit_sound)
                elif self.player.adaptation == "Fire":
                    if bullet_collision.type != "Fire":
                        bullet_collision.fire_damage = True
                    arcade.play_sound(self.fr_hit_sound)
                elif self.player.adaptation == "Leech":
                    if bullet_collision.type != "Leech":
                        self.player.health += 5 + self.bonus_effect
                    self.deal_fire_damage = False
                    arcade.play_sound(self.lc_hit_sound)
                elif self.player.adaptation == "Slime":
                    if bullet_collision.type != "Slime":
                        bullet_collision.mv_speed -= 5 + self.bonus_effect
                    self.deal_fire_damage = False
                    arcade.play_sound(self.sl_hit_sound)
                
                # Deal damage and destroy enemies.
                bullet_collision.take_damage(self.player.bullet_damage)
                if bullet_collision.health <= 0:
                    if bullet_collision.type == "Fire":
                            arcade.play_sound(self.explosion_sound)
                    elif bullet_collision.type == "Slime":
                        arcade.play_sound(self.meep_sound)
                    else:
                        arcade.play_sound(self.screech_sound)
                    bullet_collision.remove_from_sprite_lists()
                    self.enemy_num -= 1
                    self.credits += 25
                bullet.remove_from_sprite_lists()
            
                
        # Handle everything that happens when an enemy shoots and hits a player.
        for enemy_bullet in self.enemy_bullet_sprite_list:
            self.enemy_bullet_wall_collision = arcade.check_for_collision_with_list(enemy_bullet,self.wall_list)
            self.enemy_bullet_player_collision = arcade.check_for_collision_with_list(enemy_bullet,self.player_list)

            # Remove the bullet when it collides with something.
            for bullet_collision in self.enemy_bullet_wall_collision:
                enemy_bullet.remove_from_sprite_lists()

            # Deal damage to and destroy the player.
            for bullet_collision in self.enemy_bullet_player_collision:
                self.player.take_damage(50)
                
                if self.player.health <= 0:
                    arcade.play_sound(self.defeat_sound)
                    self.setup(self.arena)
                enemy_bullet.remove_from_sprite_lists()

            
                
        # Handle the camera view.
        view_changed = False
        left_border = self.view_left + LEFT_VIEW_MARGIN

        # Spawn the enemies.
        if self.enemy_num < self.max_enemies:
            
            # Spawn an enemy of random type and stats.
            enemy_type = random.randint(1,3)
            
            if(enemy_type == 1):
                self.enemy = Enemy(110,4,"Fire",False)
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1
            
            elif(enemy_type == 2):
                
                self.enemy = Enemy(120,4,"Leech",False)
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1
            
            elif(enemy_type == 3):

                self.enemy = Enemy(100,5,"Slime",False)
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1
        
        # Handle enemy behavior.
        for enemy in self.enemy_sprite_list:
            enemy.chase_player(self.player)
            enemy.check_wall_collision(self.wall_list)
            enemy.aim(self.player)

            # Attempt to fix the spawning bug (Doesn't seem to work)
            if self.enemy_num > self.max_enemies:
                enemy.remove_from_sprite_lists()
                self.enemy_num -= 1
            
            # Handle the enemy burning mechanic that comes with the fire bullets.
            if enemy.fire_damage:
                if self.frame_count % 60 == 0:
                    enemy.take_damage(10 + self.bonus_effect)
                    arcade.play_sound(self.fr_hit_sound)
            
            if self.frame_count % 60 == 0:

                if enemy.type == "Leech":
                    enemy_bullet = arcade.Sprite("Sprites/leech_bullet.png")
                    arcade.play_sound(self.lc_fire_sound)
                elif enemy.type == "Slime":
                    enemy_bullet = arcade.Sprite("Sprites/slime_bullet.png")
                    arcade.play_sound(self.sl_fire_sound)
                else:
                    enemy_bullet = arcade.Sprite("Sprites/fire_bullet.png")
                    arcade.play_sound(self.fr_fire_sound)
                enemy_bullet.center_x = enemy.start_x
                enemy_bullet.center_y = enemy.start_y

                enemy_bullet.angle = math.degrees(enemy.angle)

                enemy_bullet.change_x = math.cos(enemy.angle) * enemy.bullet_speed
                enemy_bullet.change_y = math.sin(enemy.angle) * enemy.bullet_speed

                self.enemy_bullet_sprite_list.append(enemy_bullet)

                # Handle death by fire bullets.
                if enemy.fire_damage:
                    if enemy.health <= 0:
                        self.enemy_num -= 1
                        self.credits += 25
                        if enemy.type == "Fire":
                            arcade.play_sound(self.explosion_sound)
                        elif enemy.type == "Slime":
                            arcade.play_sound(self.meep_sound)
                        else:
                            arcade.play_sound(self.screech_sound)
                        enemy.remove_from_sprite_lists()
            
            self.enemy_bullet_sprite_list.update()
        
        # Handles the camera movement.
        # If the player character moves beyond a certain margin, move the camera with it.
        # This basically centers the camera to the player when he moves too far in any direction.
        if self.player.left < left_border:
            self.view_left -= left_border - self.player.left
            view_changed = True
            
        right_border = self.view_left + WINDOW_WIDTH - RIGHT_VIEW_MARGIN
        if self.player.right > right_border:
            self.view_left += self.player.right - right_border
            view_changed = True
        
        top_border = self.view_bottom + UPPER_VIEW_MARGIN
        if self.player.top > UPPER_VIEW_MARGIN:
            self.view_bottom += self.player.top - top_border
            view_changed = True


        bottom_border = self.view_bottom + BOTTOM_VIEW_MARGIN
        if self.player.bottom < bottom_border:
            self.view_bottom -= bottom_border - self.player.bottom
            view_changed = True

        if view_changed:

            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)
            
            arcade.set_viewport(self.view_left,self.view_left+WINDOW_WIDTH,self.view_bottom,self.view_bottom+WINDOW_HEIGHT)

def main():
    """ The main method of the file. Everything starts here. """

    window = arcade.Window(WINDOW_WIDTH,WINDOW_HEIGHT,"Stellar: Arena") # Create the window.
    game_window = MenuView()
    window.show_view(game_window) # Call the main menu screen.
    arcade.run() # Start the game.

# For imports.
if __name__ == "__main__":
    main()
        
