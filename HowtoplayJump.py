import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "My Game"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.8
TILE_SCALING = 0.5
COIN_SCALING = 0.7

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
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.exit_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")

        arcade.set_background_color(arcade.csscolor.POWDER_BLUE)

        self.game_over = False
        self.game_started = False
        self.win_message = False

        # New variable to store the key instructions
        self.key_instructions = ""
        self.keys = set()

    def setup(self):
        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()

        image_source = ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk1.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 3
        self.player_sprite.center_y = 96
        self.player_list.append(self.player_sprite)

        exit_image = arcade.Sprite(":resources:images/items/flagGreen1.png")
        exit_image.center_x = 1280
        exit_image.center_y = 126
        self.exit_list.append(exit_image)

        for x in range(0, 1280, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        for x in range(0, 1250, 270):
            coin = arcade.Sprite(":resources:images/items/gemBlue.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 80
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
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

            # Display key instructions
            arcade.draw_text(self.key_instructions, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50,
                             arcade.color.BLACK, font_size=16, anchor_x="center")

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
            self.keys.add(key)  # Add the pressed key to the set

            if key == arcade.key.UP or key == arcade.key.W:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                # Update key instructions based on pressed key
                self.key_instructions = "Press LEFT or A to move left\nPress RIGHT or D to move right"
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
                # Update key instructions based on pressed key
                self.key_instructions = "Press RIGHT or D to move right"
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
                # Update key instructions based on pressed key
                self.key_instructions = "Move towards the green flags"

            # Check if all keys have been pressed at least once
            if arcade.key.W in self.keys and arcade.key.UP in self.keys \
                    and (arcade.key.LEFT in self.keys or arcade.key.A in self.keys) \
                    and (arcade.key.RIGHT in self.keys or arcade.key.D in self.keys):
                self.key_instructions = "You are ready! Move towards the green flags!!!"

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

            if self.player_sprite.center_x >= 1280:
                self.win_message = True

            if self.player_sprite.bottom < -100:
                self.game_over = True

    def reset_game(self):
        self.setup()
        self.game_over = False
        self.game_started = False
        self.win_message = False

    def on_resize(self, width, height):
        if width < 1280:
            width = 1280
        if height < 720:
            height = 720
        super().on_resize(width, height)
        arcade.set_viewport(0, width, 0, height)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
