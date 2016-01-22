from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Triangle, Line)
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.core.audio import SoundLoader, Sound
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, ReferenceListProperty,\
ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window, WindowBase
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.animation import Animation
import math
import random
import time

import cgitb
cgitb.enable()



class StartScreen(Screen):
    def on_text(self, username_text):
        print('The widget', self, 'have:', username_text)
        self.username_text = username_text
        #return username_text

    def PlaySound(self):
        sound = SoundLoader.load(r'.\Sounds\Melody.wav')
        if sound:
            print("Sound is %.3f seconds long" % sound.length)
            sound.play()


    textinput = TextInput()
    textinput.bind(text=on_text)


    hello_world = StringProperty()


    def update_string(self, req, results):
        self.hello_world = results


    def username_button_pressed(self):
        username = StringProperty()
        username = self.username_text
        req = UrlRequest("http://bsccg08.ga.fal.io/Input_names/?FirstName=" + username, self.update_string)


asteroid_speed = 3                  #Lengh in seconds it takes the asteroids to move across the screen


class Asteroid_Movement(Widget):
    asteroids = ListProperty(())
    PlayerScore = NumericProperty(0)
    def Asteroid_spawn(self):
        Animation.cancel_all(self)
        targetX = NumericProperty(0)
        targetY = NumericProperty(0)
        self.go_left(instance=self, value=1)
        self.go_up(instance=self,value=1)
        #self.go_up(instance=self, value=1)
    def go_left(self, instance, value):
        animation = Animation(x= -100, y = random.randrange(0, self.parent.height), duration=asteroid_speed, transition='linear')
        animation.bind(on_progress = self.on_progess)
        animation.bind(on_complete = self.go_right)
        animation.start(self)
    def go_right(self, instance, value):
        animation = Animation(x= self.parent.width, y= random.randrange(0, self.parent.height), duration=asteroid_speed)
        animation.bind(on_progress = self.on_progess)
        animation.bind(on_complete = self.go_left)
        animation.start(self)
    def go_up(self,instance, value):
        animation = Animation(x= self.parent.width, y= random.randrange(0, self.parent.width), duration=asteroid_speed)
        animation.bind(on_progress = self.on_progess)
        animation.bind(on_complete = self.go_down)
        animation.start(self)
    def go_down(self,instance, value):
        animation = Animation(x= self.parent.width, y= random.randrange(0, self.parent.width), duration=3)
        animation.bind(on_progress = self.on_progess)
        animation.bind(on_complete = self.go_down)
        animation.start(self)


    def on_start(self,instance,value):
        pass
    def on_progess(self,instance, value,progression):
        pass
        if progression > 0.9:
            print("Progression")

        #if self.collide_point(30,30):
        #    self.PlayerScore += 1



########################################################################
class Asteroid_properties(Widget):
    pass

class Game(Screen, Widget):
    pass


#class controling the movement of the ship
class Ship(Widget):
    xtouch = NumericProperty(0.0)
    ytouch = NumericProperty(0.0)
    degrees = NumericProperty(0.0)
    PlayerScore = NumericProperty(0)

    def on_touch_down(self, touch):

        xtouch = touch.x
        ytouch = touch.y
        print(xtouch,ytouch)

        Animation.cancel_all(self)
        anim = Animation(x=xtouch, y=ytouch, duration=0.5, t='linear')
        anim.bind(on_progress = self.on_progess)
        anim.start(self)

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
        #print (self.degrees)

    def on_progess(self,instance, value,progression):
        if self.collide_widget(self):
            self.PlayerScore += 1
            print(self.PlayerScore)


#Gets the highscores from the database
class HighScores(Screen):
    Highscores = StringProperty()
    def update_string(self, req, results):
        self.Highscores = results


    def highscores_button_pressed(self):
        req = UrlRequest("http://bsccg08.ga.fal.io/Highscores/?Highscore=printnames", self.update_string)

#Class used for managing the different screens
class MyScreenManager(ScreenManager):
    pass

HSpresentation = Builder.load_file("Game.kv")
Asteroidspresentation = Builder.load_file("Asteroids.kv")

class Asteroids(App):
    def build(self):
        game = Asteroidspresentation
        #asteroid = HSpresentation
        return game


if __name__ == '__main__':
    Asteroids().run()
