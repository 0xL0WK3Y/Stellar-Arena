import arcade, math, random
from PlayerObject import PlayerCharacter
from FireEnemy import FireEnemyObject


WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 650
WINDOW_TITLE = "Stellar: Arena"

WALL_SCALE = 1

BULLET_SPEED = 7

LEFT_VIEW_MARGIN = 250
RIGHT_VIEW_MARGIN = 250
UPPER_VIEW_MARGIN = 256
BOTTOM_VIEW_MARGIN = 50

UPDATES_PER_FRAME = 7

class BotFight(arcade.Window):

    def __init__(self):

        super().__init__(WINDOW_WIDTH,WINDOW_HEIGHT,WINDOW_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.wall_list = None
        self.floor_list = None
        self.player_spawn_list = None
        self.enemy_spawn_list = None
        self.death_tile_list = None
        self.collision_list = None
        self.enemy_sprite_list = None
        self.bullet_sprite_list = None
        self.enemy_bullet_sprite_list = None
        self.player_score = 0

        self.enemy_spawner_x_list = []
        self.enemy_spawner_y_list = []

        self.view_bottom = 0
        self.view_left = 0

        self.movement_possible = True

        self.frame_count = 0

    def setup(self):

        self.player_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()
        self.player_spawn_list = arcade.SpriteList()
        self.enemy_spawn_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.bullet_sprite_list = arcade.SpriteList(use_spatial_hash =True)
        self.enemy_bullet_sprite_list = arcade.SpriteList(use_spatial_hash=True)

        self.max_enemies = 2
        self.enemy_num = 0
        self.player_score = 0

        level_file = "Maidens_Kiss.tmx"
        wall_layer_name = "Walls"
        floor_layer_name = "Floor"
        player_spawner_name = "PlayerSpawner"
        enemy_spawner_name = "EnemySpawner"
        death_tile_layer_name = "DeathTiles"

        game_arena = arcade.tilemap.read_tmx(level_file)
        self.wall_list = arcade.tilemap.process_layer(game_arena,wall_layer_name,WALL_SCALE)
        self.floor_list = arcade.tilemap.process_layer(game_arena,floor_layer_name,WALL_SCALE)
        self.player_spawn_list = arcade.tilemap.process_layer(game_arena,player_spawner_name,WALL_SCALE)
        self.enemy_spawn_list = arcade.tilemap.process_layer(game_arena,enemy_spawner_name,WALL_SCALE)

        for sprite in self.wall_list:
            self.collision_list.append(sprite)
        
        self.player = PlayerCharacter(100,4,"Lazer",15)
        for spawner in self.player_spawn_list:
            self.player.center_x = spawner.center_x
            self.player.center_y = spawner.center_y
        self.player_list.append(self.player)

        for spawner in self.enemy_spawn_list:
            self.enemy_spawner_x_list.append(spawner.center_x)
            self.enemy_spawner_y_list.append(spawner.center_y)

            

        if game_arena.background_color:
            arcade.set_background_color(game_arena.background_color)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.collision_list,0)

    def on_draw(self):
            
        arcade.start_render()
        self.wall_list.draw()
        self.floor_list.draw()
        self.enemy_spawn_list.draw()
        self.player_spawn_list.draw()
        self.bullet_sprite_list.draw()
        self.enemy_bullet_sprite_list.draw()

        score_text = f"Credits: {self.player_score}"
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
        

        try:
            self.player_list.draw()
            self.enemy_sprite_list.draw()
           
        except Exception as e:
            print(str(e))
    
    def on_key_press(self,key,modifiers):
       
        if (key == arcade.key.UP or key == arcade.key.W) and self.movement_possible:
            self.player.change_y = self.player.mv_speed
        elif (key == arcade.key.DOWN or key == arcade.key.S) and self.movement_possible:
            self.player.change_y = -self.player.mv_speed
        elif (key == arcade.key.RIGHT or key == arcade.key.D) and self.movement_possible:
            self.player.change_x = self.player.mv_speed
        elif (key == arcade.key.LEFT or key == arcade.key.A) and self.movement_possible:
            self.player.change_x = -self.player.mv_speed
    
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        
    def on_mouse_press(self,x,y,button,modifiers):

         if self.player.adaptation_uses <= 0:
            self.player.adaptation = "Lazer"
            self.player.adaptation_uses = 15

         if (self.player.adaptation == "Lazer"):
            bullet = arcade.Sprite("Sprites/lz_bullet.png")
            self.bullet_sprite_list.append(bullet)
         elif (self.player.adaptation == "Fire") and (self.player.adaptation_uses > 0):
            bullet = arcade.Sprite("Sprites/bullet.png",1)
            self.bullet_sprite_list.append(bullet)
         elif((self.player.adaptation == "Slime") and (self.player.adaptation_uses > 0)):
            bullet = arcade.Sprite("Sprites/slime_bullet.png",1)
            self.bullet_sprite_list.append(bullet)
         elif((self.player.adaptation == "Leech") and (self.player.adaptation_uses > 0)):
            bullet = arcade.Sprite("Sprites/leech_bullet.png",1)
            self.bullet_sprite_list.append(bullet)

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

         if self.player.adaptation != "Lazer":
            self.player.adaptation_uses -= 1


      
    def on_update(self,delta_time):

        self.frame_count += 1

        self.bullet_sprite_list.update()
        self.enemy_bullet_sprite_list.update()
        self.player_list.update()
        self.player.update_animation()
        self.enemy_sprite_list.update()
        self.enemy_sprite_list.update_animation()
        self.physics_engine.update()

        if self.enemy_num < 0:
            enemy_num = 0

        for bullet in self.bullet_sprite_list:
            self.bullet_wall_collision = arcade.check_for_collision_with_list(bullet,self.wall_list)
            self.bullet_enemy_collision = arcade.check_for_collision_with_list(bullet, self.enemy_sprite_list)

            for bullet_collision in self.bullet_wall_collision:
                bullet.remove_from_sprite_lists()
            for bullet_collision in self.bullet_enemy_collision:
                bullet_collision.take_damage(self.player.bullet_damage)
                if self.player.adaptation == "Lazer":
                    self.player.adaptation = bullet_collision.type
                elif self.player.adaptation == "Fire":
                    if self.frame_count % 60 == 0:
                        bullet_collision.take_damage(10)
                elif self.player.adaptation == "Leech":
                    self.player.health += 5
                elif self.player.adaptation == "Slime":
                    bullet_collision.mv_speed -= 5
                
                if bullet_collision.health <= 0:
                    self.enemy_num -= 1
                    self.player_score += 25
                bullet.remove_from_sprite_lists()
                

        for enemy_bullet in self.enemy_bullet_sprite_list:
            self.enemy_bullet_wall_collision = arcade.check_for_collision_with_list(enemy_bullet,self.wall_list)
            self.enemy_bullet_player_collision = arcade.check_for_collision_with_list(enemy_bullet,self.player_list)

            for bullet_collision in self.enemy_bullet_wall_collision:
                enemy_bullet.remove_from_sprite_lists()
            for bullet_collision in self.enemy_bullet_player_collision:
                self.player.take_damage(50)
                
                if self.player.health <= 0:
                    self.setup()
                enemy_bullet.remove_from_sprite_lists()

            
                

        view_changed = False
        left_border = self.view_left + LEFT_VIEW_MARGIN

        #Spawn enemies
        if self.enemy_num < self.max_enemies:
            
            enemy_type = random.randint(1,3)
            
            if(enemy_type == 1):
                self.enemy = FireEnemyObject(100,100,4,5,"Fire")
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1
            
            elif(enemy_type == 2):
                
                self.enemy = FireEnemyObject(100,100,4,5,"Leech")
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1
            
            elif(enemy_type == 3):

                self.enemy = FireEnemyObject(100,100,4,5,"Slime")
                self.enemy.center_x = self.enemy_spawner_x_list[self.enemy_num]
                self.enemy.center_y = self.enemy_spawner_y_list[self.enemy_num]
                self.enemy_sprite_list.append(self.enemy)
                self.enemy_num += 1

        for enemy in self.enemy_sprite_list:
            enemy.chase_player(self.player)
            enemy.check_wall_collision(self.wall_list)
            enemy.aim(self.player)

            if self.enemy_num > self.max_enemies:
                enemy.remove_from_sprite_lists()
            
            if enemy.health <= 0:
                enemy.remove_from_sprite_lists()
            
            if self.frame_count % 60 == 0:

                enemy_bullet = arcade.Sprite("Sprites/lz_bullet.png")
                enemy_bullet.center_x = enemy.start_x
                enemy_bullet.center_y = enemy.start_y

                enemy_bullet.angle = math.degrees(enemy.angle)

                enemy_bullet.change_x = math.cos(enemy.angle) * enemy.bullet_speed
                enemy_bullet.change_y = math.sin(enemy.angle) * enemy.bullet_speed

                self.enemy_bullet_sprite_list.append(enemy_bullet)
            
            self.enemy_bullet_sprite_list.update()

        
        #If the player character moves beyond a certain margin, move the camera with it.
        #This basically centers the camera to the player when he moves too far in any direction.
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

    main_window = BotFight()
    main_window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
        
