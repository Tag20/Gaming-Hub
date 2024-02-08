import subprocess
from ursina import *

def level_button_click():
    level_number = int(button.text.split()[-1])  # Extract the level number from the button text
    
    if level_number == 1:
        file_path = "Games 2.0\HowtoplayJump.py"
    elif level_number == 2:
        file_path = "Games 2.0\Jump Game Level 1.py"  # Specify the file path for Level 2
    elif level_number == 3:
        file_path = "Games 2.0\Jump Game Level 2.py"  # Specify the file path for Level 3
    elif level_number == 4:
        file_path = "Games 2.0\Jump Game Level 3.py"  # Specify the file path for Level 4
    elif level_number == 5:
        file_path = "Games 2.0\Jump Game Level 4.py"  # Specify the file path for Level 5
    elif level_number == 6:
        file_path = "Games 2.0\Jump Game Level 5.py"  # Specify the file path for Level 6
    elif level_number == 7:
        file_path = "Games 2.0\Jump Game Level 6.py"  # Specify the file path for Level 7
    elif level_number == 8:
        file_path = "Games 2.0\Jump Game Level 7.py"  # Specify the file path for Level 8
    elif level_number == 9:
        file_path = "Games 2.0\Jump Game Level 8.py"  # Specify the file path for Level 9
    elif level_number == 10:
        file_path = "Games 2.0\Jump Game Level 9.py"  # Specify the file path for Level 10
    else:
        file_path = ""
    
    subprocess.run(["python", file_path])  # Execute the Python file using subprocess

app = Ursina()

# Create the Jump Game label at the top
jump_label = Text(text="Jump Game", position=(0, 0.4), scale=1)

# Create the buttons
for i in range(10):
    row = i // 5  # Calculate the row index
    col = i % 5   # Calculate the column index

    button = Button(
        text=f"Level {i+1}",
        scale=(0.3, 0.15),  # Enlarge the button size
        position=(-0.6 + col * 0.3, 0.2 - row * 0.2),  # Adjust position accordingly
        on_click=level_button_click
    )

app.run()
