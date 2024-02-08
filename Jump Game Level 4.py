import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "My Game"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.8
TILE_SCALING = 0.5
COIN_SCALING = 0.7
ENEMY_SCALING = 0.8

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.exit_list = None
        self.enemy_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        arcade.set_background_color(arcade.csscolor.POWDER_BLUE)

        # Game state variables
        self.game_over = False
        self.game_started = False
        self.win_message = False

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk1.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 3
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 2560, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Create the open space for falling down
        for x in range(320, 640, 64):
            open_space = arcade.Sprite(":resources:images/tiles/sandCenter.png", TILE_SCALING)
            open_space.center_x = x
            open_space.center_y = -96
            self.wall_list.append(open_space)

        # Create the land with a gem over the center part
        for x in range(640, 960, 64):
            land = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            land.center_x = x
            land.center_y = 32
            self.wall_list.append(land)

        gem = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
        gem.center_x = 800
        gem.center_y = 96
        self.coin_list.append(gem)

        # Create the small grass level before the mountain
        for x in range(960, 1024, 64):
            grass = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            grass.center_x = x
            grass.center_y = 96
            self.wall_list.append(grass)

        # Create the mountain to climb
        for x in range(1024, 1280, 64):
            for y in range(1, 5):
                mountain = arcade.Sprite(":resources:images/tiles/stoneCenter.png", TILE_SCALING)
                mountain.center_x = x
                mountain.center_y = 32 + (y * 64)
                self.wall_list.append(mountain)

        # Create the gem at the top of the mountain
        gem = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
        gem.center_x = 1120
        gem.center_y = 352
        self.coin_list.append(gem)

        # Create the additional level on top of the mountain
        for x in range(960, 1280, 64):
            level2 = arcade.Sprite(":resources:images/tiles/stoneCenter.png", TILE_SCALING)
            level2.center_x = x
            level2.center_y = 448
            self.wall_list.append(level2)

        # Create the second mountain level
        for x in range(960, 1280, 64):
            for y in range(1, 5):
                mountain = arcade.Sprite(":resources:images/tiles/stoneCenter.png", TILE_SCALING)
                mountain.center_x = x
                mountain.center_y = 512 + (y * 64)
                self.wall_list.append(mountain)

        # Create the second gem at the top of the second mountain
        gem = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
        gem.center_x = 1120
        gem.center_y = 768
        self.coin_list.append(gem)

        # Create the flat land with an enemy
        for x in range(1280, 1600, 64):
            land = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            land.center_x = x
            land.center_y = 32
            self.wall_list.append(land)

        enemy = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_idle.png", ENEMY_SCALING)
        enemy.center_x = 1440
        enemy.center_y = 96
        self.enemy_list.append(enemy)

        # Create the gem after the enemy
        gem = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
        gem.center_x = 1760
        gem.center_y = 96
        self.coin_list.append(gem)

        # Create the final flag
        flag = arcade.Sprite(":resources:images/items/flagGreen1.png")
        flag.center_x = 2048
        flag.center_y = 96
        self.exit_list.append(flag)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        if not self.game_started:
            arcade.draw_text("Press any key to start", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
        elif self.game_over:
            arcade.draw_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                             arcade.color.BLACK, font_size=30, anchor_x="center")
            arcade.draw_text("Press Enter to restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("Press Esc to exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
        elif self.win_message:
            arcade.draw_text("You Win!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                             arcade.color.BLACK, font_size=30, anchor_x="center")
            arcade.draw_text("Press Enter to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text("Press Esc to exit", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
                             arcade.color.BLACK, font_size=20, anchor_x="center")
        else:
            self.wall_list.draw()
            self.coin_list.draw()
            self.player_list.draw()
            self.exit_list.draw()
            self.enemy_list.draw()

            score_text = f"Score: {self.score}"
            arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                             arcade.csscolor.BLUE, 18)

    def on_key_press(self, key, modifiers):
        if self.game_over:
            if key == arcade.key.ENTER:
                self.reset_game()
            elif key == arcade.key.ESCAPE:
                arcade.close_window()
        elif not self.game_started:
            self.setup()
            self.game_started = True
        elif self.win_message:
            if key == arcade.key.ENTER:
                self.reset_game()
        else:
            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        if not self.game_over and not self.win_message:
            self.physics_engine.update()

            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                arcade.play_sound(self.collect_coin_sound)
                self.score += 1

            enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

            for enemy in enemy_hit_list:
                if self.player_sprite.center_y > enemy.center_y:
                    enemy.remove_from_sprite_lists()
                    self.score += 1
                else:
                    self.game_over = True

            if self.player_sprite.center_x >= 2048:
                self.win_message = True

            if self.player_sprite.bottom < -100:
                self.game_over = True

            changed = False

            # Scroll left
            left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
            if self.player_sprite.left < left_boundary:
                self.view_left -= left_boundary - self.player_sprite.left
                changed = True

            # Scroll right
            right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed = True

            # Scroll up
            top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
            if self.player_sprite.top > top_boundary:
                self.view_bottom += self.player_sprite.top - top_boundary
                changed = True

            # Scroll down
            bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
            if self.player_sprite.bottom < bottom_boundary:
                self.view_bottom -= bottom_boundary - self.player_sprite.bottom
                changed = True

            if changed:
                # Only scroll to integers. Otherwise, we end up with pixels that
                # don't line up on the screen
                self.view_bottom = int(self.view_bottom)
                self.view_left = int(self.view_left)

                # Do the scrolling
                arcade.set_viewport(self.view_left,
                                    SCREEN_WIDTH + self.view_left,
                                    self.view_bottom,
                                    SCREEN_HEIGHT + self.view_bottom)

    def reset_game(self):
        self.game_over = False
        self.game_started = False
        self.win_message = False
        self.setup()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
