from ursina import *

app = Ursina()

camera.orthographic = True
camera.fov = 4
camera.position = (1, 1)

player = Entity(name='O', color=color.azure)
cursor = Tooltip(color=player.color, origin=(0, 0), scale=4, enabled=True)
cursor.background.color = color.clear

bg = Entity(parent=scene, model='quad', texture='shore', scale=(16, 8), z=10, color=color.light_gray)
mouse.visible = True

board = [[None for x in range(3)] for y in range(3)]
for y in range(3):
    for x in range(3):
        b = Button(parent=scene, position=(x, y))
        board[x][y] = b

        def on_click(b=b):
            b.text = player.name
            b.color = player.color
            b.collision = False
            check_for_victory()

            if player.name == 'O':
                player.name = 'X'
                player.color = color.orange
            else:
                player.name = 'O'
                player.color = color.azure

            cursor.text = ''
            cursor.color = player.color

            ai_move()  # Call the AI move function after the player's move

        b.on_click = on_click

def check_for_victory():
    name = player.name
    won = (
        (board[0][0].text == name and board[1][0].text == name and board[2][0].text == name) or
        (board[0][1].text == name and board[1][1].text == name and board[2][1].text == name) or
        (board[0][2].text == name and board[1][2].text == name and board[2][2].text == name) or
        (board[0][0].text == name and board[0][1].text == name and board[0][2].text == name) or
        (board[1][0].text == name and board[1][1].text == name and board[1][2].text == name) or
        (board[2][0].text == name and board[2][1].text == name and board[2][2].text == name) or
        (board[0][0].text == name and board[1][1].text == name and board[2][2].text == name) or
        (board[0][2].text == name and board[1][1].text == name and board[2][0].text == name)
    )

    if won:
        # print('Winner is:', name)
        destroy(cursor)
        mouse.visible = True
        Panel(z=1, scale=10, model='quad')
        t = Text(f'Player\n{name}\nwon!', scale=3, origin=(0, 0), background=True)
        t.create_background(padding=(.5, .25), radius=Text.size / 2)
        t.background.color = player.color.tint(-.2)

def ai_move():
    # AI logic goes here
    # You need to implement the AI move strategy

    # Example: Random move
    import random
    available_moves = []
    for y in range(3):
        for x in range(3):
            if not board[x][y].text:
                available_moves.append((x, y))

    if available_moves:
        x, y = random.choice(available_moves)
        board[x][y].text = player.name
        board[x][y].color = player.color
        board[x][y].collision = False
        check_for_victory()

        if player.name == 'O':
            player.name = 'X'
            player.color = color.orange
        else:
            player.name = 'O'
            player.color = color.azure

        cursor.text = ''
        cursor.color = player.color

app.run()