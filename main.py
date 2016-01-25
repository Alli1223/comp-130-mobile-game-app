from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.audio import SoundLoader, Sound
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
import math
import random

import cgitb
cgitb.enable()

PLAYERSCORE = 0                                      #The players default score
ASTEROID_AMMOUNT = 20                                #Ammount of asteroids that will be loaded in the game

class Player_Object(Widget):
    """This class manages the collision detection for the player"""
    PlayerScore = NumericProperty(PLAYERSCORE)
    def collide_asteroid(self, asteroid):
        if self.collide_widget(asteroid):
            self.PlayerScore = self.PlayerScore + 1         #if the ship collides with the asteroids add 1 to the score
            print(self.PlayerScore)


class StartScreen(Screen):
    """This class provides the functionality to the start screen buttons"""
    def on_text(self, username_text):
        print('The widget', self, 'have:', username_text)
        self.username_text = username_text
        return username_text

    #Plays Sound located in the Sounds folder
    def PlaySound(self):
        sound = SoundLoader.load(r'.\Sounds\Melody.wav')
        if sound:
            print("Sound is %.3f seconds long" % sound.length)
            sound.play()

    #updates the sring property to the value entered in the text input box
    textinput = TextInput()
    textinput.bind(text=on_text)
    user_input = StringProperty()

    def update_string(self, req, results):
        self.user_input = results

    #Send a URL request to the server with the username vairable as the FirstName input.
    def username_button_pressed(self):
        username = StringProperty()
        username = self.username_text
        req = UrlRequest("http://bsccg08.ga.fal.io/Input_names/?FirstName=" + username, self.update_string)

class Ship(Widget):
    """This class manages the movement and orientation of the player ship"""
    xtouch = NumericProperty(0)
    ytouch = NumericProperty(0)
    degrees = NumericProperty(0.0)
    PlayerScore = NumericProperty(0)
    player_ship = Player_Object()

    def on_touch_down(self, touch):
        xtouch = touch.x
        ytouch = touch.y

        #animation that moves the ship to a designatd x and y coordinate
        Animation.cancel_all(self)
        self.anim = Animation(x=xtouch, y=ytouch, duration=0.25, t='linear')
        self.anim.bind(on_start = self.on_start)
        self.anim.bind(on_progress = self.on_progess)
        self.anim.start(self)

        #x1,y1 is the ships current position
        #x2,y2 is the postition it is moving to
        x1 = self.x
        y1 = self.y
        x2 = touch.x
        y2 = touch.y
        deltaX = x2 - x1
        deltaY = y2 - y1
        angle = math.atan2(deltaY, deltaX)

        #convert it from 180 degrees to 360
        if self.degrees <= 0:
            self.degrees = 360 - (-self.degrees)
        #convert it from radians to degrees
        self.degrees = angle * (180 / math.pi)


    #A function that plays a sound when the animation starts moving
    def on_start(self,instance, value):
        StartScreen.PlaySound(self)

    #A function that runs when the ship starts moving
    def on_progess(self,instance, value, progression):
        pass

class Asteroid(Widget):
    """Creates an instance of Asteroid and gives it a random velocity and manages their X and Y location
    and makes sure they stay on the screen."""
    def __init__(self, **kwargs):
        super(Asteroid, self).__init__(**kwargs)
        self.Asteroid = ObjectProperty(None)
        Clock.schedule_interval(self.update, 1 / 60.0)
        self.velocity = (random.randrange(-5,5), random.randrange(-5,5))    #The X & Y velocity is a random ammount between -5 and 5

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    player_ship = Player_Object()

    """The update function makes sure that the asteroids stay on the screen
    Then checks to see if they have collided with the ship."""
    def update(self, dt):
        self.move()
        if (self.y < 0) or (self.y > self.parent.top):
            self.velocity_y *= -1
        if (self.x < 0) or (self.x > self.parent.right):
            self.velocity_x *= -1
        self.player_ship.collide_asteroid(self)


    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    #def collision(self, asteroid):
    #    if self.collide_widget(asteroid):
    #        print("WORKS!")

class Asteroid_Movement(Widget):
    """This class spawns the asteroids and manages their behaviour"""

    #creates a list of asteroids that move about the screen
    asteroids = ListProperty(())

    def start(self):
        """Creates instances of asteroids and gives them a random spawn position then adds them to the listproperty
        """
        for i in range(0,ASTEROID_AMMOUNT):
            asteroid = Asteroid()
            self.add_widget(asteroid)
            self.asteroids.append(asteroid)
            asteroid.center_x = random.randrange(self.parent.width)
            asteroid.center_y = random.randrange(self.parent.height)



class Game(Screen, Widget):
    """Game screen has no functions, but manages the game screen which Asteroid_Movement and Asteroid
    inherit from"""
    pass

class HighScores(Screen):
    """HighScores manages the functionality of the HighScores screen and runs different python files
    on the sever depending on the button pressed."""
    Highscores = StringProperty()
    scores = StringProperty()

    #Prints the Highscores label depending on the results printed in the server file
    def update_string(self, req, results):
        self.Highscores = results

    def highscores_button_pressed(self):
        req = UrlRequest("http://bsccg08.ga.fal.io/Highscores/?Highscore=printnames", self.update_string)

    #Inputs the Scores depending on the results variable scores.
    def update_scores(self, req, results):
        self.scores = results

    def scores_button_pressed(self):
        scores = str(300)
        req = UrlRequest("http://bsccg08.ga.fal.io/Input_score/?score=" + scores , self.update_scores)


#Class used for managing the different screens
class MyScreenManager(ScreenManager):
    pass

HSpresentation = Builder.load_file("Game.kv")                   #Loads the Game.kv file which manages the layout of the game screen
Asteroidspresentation = Builder.load_file("Asteroids.kv")       #Loads the Asteroids.kv file that manages the menu and highscores screen

class Asteroids(App):
    def build(self):
        return self.root


if __name__ == '__main__':
    Asteroids().run()
