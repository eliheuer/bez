#Import modules/libraries
import pyxel
from collections import namedtuple
from random import randint

#Named tuple for cartesian points
Point = namedtuple("Point", ["x", "y"])

#Constants
COL_BACKGROUND = 0
COL_DEATH_SCREEN = 10
TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5
COL_SCORE = 11

WIDTH = 240
HEIGHT = 240

HEIGHT_SCORE = FONT_HEIGHT = pyxel.constants.FONT_HEIGHT

START = Point((WIDTH/2) - 2, HEIGHT - 11)

class Bez:

    #Initialization.
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption = "Bez!", fps = 60)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.location = START
        self.death = False
        self.score = 0

    #Update Logic.
    def update(self):
        if not self.death:
            self.update_location()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_location(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and not pyxel.btn(pyxel.KEY_LEFT):
            if self.location.x < WIDTH - 11:
                old = self.location
                new = Point(old.x + 1, old.y)
                self.location = new
        elif pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT):
            if self.location.x > 0:
                old = self.location
                new = Point(old.x - 1, old.y)
                self.location = new
        elif pyxel.btn(pyxel.KEY_SPACE):
            #self.shoot()
            pass

    #Draw Logic.
    def draw(self):
        if not self.death:
            pyxel.cls(COL_BACKGROUND)
            self.draw_spacship()
            self.draw_score()
        else:
            self.draw_death()

    def draw_spacship(self):
        x = self.location.x
        y = self.location.y 
        pyxel.circ(x, y, 4, 4)

    def draw_score(self):
        score = "{:04}".format(self.score)
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

    def draw_death(self):
        pyxel.cls(COL_DEATH_SCREEN)
        display_text = TEXT_DEATH[:]
        display_text.insert(1, "{:04}".format(self.score))
        for i, text in enumerate(display_text):
            y_offset = (FONT_HEIGHT + 2) * (i + 5)
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_DEATH + y_offset, text, COL_TEXT_DEATH)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.constants.FONT_WIDTH):
        text_width = len(text) * char_width
        return (page_width - text_width) // 2

#Call Application
Bez()
