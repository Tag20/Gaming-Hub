from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import subprocess
import sys
from kivy.config import ConfigParser


class ZoomButton(Button):
    def on_enter(self, *args):
        anim = Animation(scale=1.5, duration=0.2)
        anim.start(self)

    def on_leave(self, *args):
        anim = Animation(scale=1.0, duration=0.2)
        anim.start(self)

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            # Check if it's a right-click event
            if 'button' in touch.profile and touch.button == 'right':
                # Return True to indicate the event is handled
                return True
        # Call the superclass method for other touch events
        return super().on_touch_down(touch)


class UserProfile(AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dropdown = DropDown(auto_dismiss=False)
        self.dropdown.bind(on_dismiss=self.on_dropdown_dismiss)

    def on_dropdown_dismiss(self, instance):
        print("Dropdown dismissed")

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.open_profile_form()
            return True
        return super().on_touch_down(touch)

    def open_profile_form(self):
        # Create the popup form
        popup = Popup(title='User Profile',
                      size_hint=(None, None), size=(400, 400), auto_dismiss=False)

        # Create the form layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Create text input fields
        user_name_input = TextInput(hint_text='User Name')
        email_input = TextInput(hint_text='Email Address')
        dob_input = TextInput(hint_text='Date of Birth')
        dob_input.input_filter = 'int'

        # Create a button to submit the form
        submit_button = Button(text='Save', size_hint=(1, None), height=40)
        submit_button.bind(on_release=lambda btn: self.update_user_profile(popup, user_name_input.text, email_input.text, dob_input.text))

        # Add the input fields and submit button to the layout
        layout.add_widget(user_name_input)
        layout.add_widget(email_input)
        layout.add_widget(dob_input)
        layout.add_widget(submit_button)

        # Add the layout to the popup and open it
        popup.content = layout
        popup.open()

    def update_user_profile(self, popup, user_name, email, dob):
        if user_name and email and dob:
            if validate_email(email):
                self.source = 'UserProfile.png'  # Update with the appropriate image

                user_details_label = Label(text=f"User Name: {user_name}\nEmail: {email}\nDate of Birth: {dob}")

                self.dropdown.add_widget(user_details_label)

                self.dropdown.open(self)

                popup.dismiss()
            else:
                print("Invalid email address")
        else:
            print("Please fill in all fields")


class ButtonApp(App):
    def build(self):
        # Setting background color
        Window.clearcolor = (0, 0, 0, 0)  # Setting window background color

        # Adding video as background
        video = Video(source='Background.mp4', state='play', allow_stretch=True)
        video.opacity = 0.5

        # Creating buttons
        button1 = ZoomButton(text="Pong", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.8},
                             background_color=(0, 0, 0, 0))
        button2 = ZoomButton(text="Tic-Tac-Toe-1v1", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7},
                             background_color=(0, 0, 0, 0))
        button3 = ZoomButton(text="2048", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.6},
                             background_color=(0, 0, 0, 0))
        button4 = ZoomButton(text="Packman", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5},
                             background_color=(0, 0, 0, 0))
        button5 = ZoomButton(text="Tic-Tac-Toe-AI", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.4},
                             background_color=(0, 0, 0, 0))
        button6 = ZoomButton(text="Arcade", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3},
                             background_color=(0, 0, 0, 0))
        exit_button = ZoomButton(text="Exit", size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                background_color=(0, 0, 0, 0))

        button1.bind(on_release=self.open_game1)
        button2.bind(on_release=self.open_game2)
        button3.bind(on_release=self.open_game3)
        button4.bind(on_release=self.open_game4)
        button5.bind(on_release=self.open_game5)
        button6.bind(on_release=self.open_game6)
        exit_button.bind(on_release=self.exit_app)

        layout = RelativeLayout()
        layout.add_widget(video)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)
        layout.add_widget(button6)
        layout.add_widget(exit_button)

        user_profile = UserProfile(source='UserProfile.png',
                                   size_hint=(0.1, 0.1),
                                   pos_hint={'top': 1, 'right': 1})

        layout.add_widget(user_profile)

        logo = Image(source='LogoSmall.png', size_hint=(0.1, 0.1), pos_hint={'top': 1, 'x': 0})

        layout.add_widget(logo)

        return layout

    def on_stop(self):
        if self.root.children:
            root_children = self.root.children
            if root_children[-1].children:
                dropdown_content = root_children[-1].children[0]
                if isinstance(dropdown_content, Label):
                    user_name = dropdown_content.text.split("\n")[0].split(":")[1].strip()
                    email = dropdown_content.text.split("\n")[1].split(":")[1].strip()
                    dob = dropdown_content.text.split("\n")[2].split(":")[1].strip()
                    print(f"Saving user profile: {user_name}, {email}, {dob}")
                    # Save the user profile to a file or database


    def open_game1(self, instance):
        subprocess.Popen([sys.executable, "pong.py"])

    def open_game2(self, instance):
        subprocess.Popen([sys.executable, "tictactoe.py"])

    def open_game3(self, instance):
        subprocess.Popen([sys.executable, "2048.py"])

    def open_game4(self, instance):
        subprocess.Popen([sys.executable, "packman.py"])

    def open_game5(self, instance):
        subprocess.Popen([sys.executable, "tictactoeAI.py"])

    def open_game6(self, instance):
        subprocess.Popen([sys.executable, "arcade.py"])

    def exit_app(self, instance):
        self.stop()


def validate_email(email):
    # Add your email validation logic here
    return True  # Placeholder validation logic


if __name__ == '__main__':
    ButtonApp().run()