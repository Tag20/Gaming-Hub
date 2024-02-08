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
            if b.text:
                return  # Ignore if the button is already clicked

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

            if not check_for_game_over():
                ai_move()  # Call the AI move function if the game is not over

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
        return True  # Return True to indicate game over

    return False  # Return False if the game is not over

def check_for_game_over():
    for y in range(3):
        for x in range(3):
            if not board[x][y].text:
                return False  # There are still empty spaces, game is not over

    print("It's a tie!")
    destroy(cursor)
    mouse.visible = True
    Panel(z=1, scale=10, model='quad')
    t = Text("It's a tie!", scale=3, origin=(0, 0), background=True)
    t.create_background(padding=(.5, .25), radius=Text.size / 2)
    t.background.color = color.gray
    return True  # Return True to indicate game over

def evaluate_board(board):
    score = 0

    # Evaluate rows
    for y in range(3):
        if board[0][y].text == board[1][y].text == board[2][y].text:
            if board[0][y].text == 'O':
                score -= 10
            elif board[0][y].text == 'X':
                score += 10

    # Evaluate columns
    for x in range(3):
        if board[x][0].text == board[x][1].text == board[x][2].text:
            if board[x][0].text == 'O':
                score -= 10
            elif board[x][0].text == 'X':
                score += 10

    # Evaluate diagonals
    if board[0][0].text == board[1][1].text == board[2][2].text:
        if board[0][0].text == 'O':
            score -= 10
        elif board[0][0].text == 'X':
            score += 10

    if board[0][2].text == board[1][1].text == board[2][0].text:
        if board[0][2].text == 'O':
            score -= 10
        elif board[0][2].text == 'X':
            score += 10

    return score

def ai_move():
    best_score = -float('inf')
    best_move = None

    for y in range(3):
        for x in range(3):
            if not board[x][y].text:
                # Simulate player's move
                board[x][y].text = player.name
                if check_for_victory():
                    board[x][y].text = ''
                    board[x][y].color = color.white
                    board[x][y].collision = True
                    return

                # Simulate AI's move
                board[x][y].text = 'X' if player.name == 'O' else 'O'
                score = evaluate_board(board)
                board[x][y].text = ''

                if score > best_score:
                    best_score = score
                    best_move = (x, y)

    if best_move:
        x, y = best_move
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

        if not check_for_game_over():
            ai_move()  # Call the AI move function recursively

app.run()
