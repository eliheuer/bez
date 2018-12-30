# Library and module imports
import argparse
import defcon
import pyxel
import xmltodict
from collections import namedtuple
from random import randint


# Named tuple for cartesian points
Point = namedtuple("Point", ["x", "y"])


COL_BACKGROUND = 0
COL_INFO = 11
WIDTH = 255
HEIGHT = 255


# Application 
class Bez:

    # Initialization
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption="Bez", fps=60)
        pyxel.image(0).load(0, 0, "assets/pencil_16x16.png")
        pyxel.mouse(True)

        self.read_glif()
        self.reset()

        pyxel.run(self.update, self.draw)
 
    def reset(self):
        self.location = Point(WIDTH / 2, HEIGHT / 2)
        self.done = False
        self.info = 0
        self.handel_locations = []
        self.zoom = 25
        self.generate_handels()
        #self.generate_random_handels()


    def create_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help = "input filename")
        parser.add_argument("-o", help = "output filename")
        args = parser.parse_args()
        return args


    def use_arg_parser():
        args = create_arg_parser()
        ttf_path = args.i
        ufo_path = args.o
        print('ttf_path: ', ttf_path)
        print('ufo_path:', ufo_path)


    def read_glif(self):
        """Reads glyph data from UFO files, creates global variables"""
        print("[+] Reading E_.glif")

        # Read UFO data from .glif file 
        try:
            with open('E_.glif') as ufo:
                self.glif = xmltodict.parse(ufo.read())
        except FileNotFoundError:
            print("[!] Error: File not found")
        else:
            print("[!] Done\n")

        # Read glyph name to variable: self.glif_name
        self.glyph_name = self.glif['glyph']['@name']
        print("glyph name:\t", self.glyph_name)

        # Read glyph format to variable: self.glif_format
        self.glyph_format = self.glif['glyph']['@format']
        print("glyph format:\t", self.glyph_format)

        # Read glyph width to variable: self.glif_width
        self.glyph_width = self.glif['glyph']['advance']['@width']
        print("glyph width:\t", self.glyph_width)

        # Read glyph unicode info to variable: self.glif_unicode
        self.glyph_unicode = self.glif['glyph']['unicode']['@hex']
        print("glyph unicode:\t", self.glyph_unicode)

        # Read glyph x-coordinate info to variable: self.glif_x_points
        self.glyph_x_points = []
        for x_point in self.glif['glyph']['outline']['contour']['point']:
            self.glyph_x_points.append(x_point['@x'])
            print("glyph x points:\t", x_point['@x'])

        # Read glyph y-coordinate info to variable: self.glif_y_points
        self.glyph_y_points = []
        for y_point in self.glif['glyph']['outline']['contour']['point']:
            self.glyph_y_points.append(y_point['@y'])
            print("glyph y points:\t", y_point['@y'])

        # Read glyph line types info to variable: self.glif_line_types
        self.glyph_line_types = []
        for line_type in self.glif['glyph']['outline']['contour']['point']:
            self.glyph_line_types.append(line_type['@x'])
            print("glyph line types:\t", line_type['@type'])

    def generate_random_handels(self):
        for i in range(9):
            x = randint(50, WIDTH - 50)
            y = randint(50, HEIGHT - 50)
            new = Point(x, y)
            self.handel_locations.append(new)

    def generate_handels(self):
        for i in range(len(self.glyph_line_types)):
            x = int(self.glyph_x_points[i])
            y = int(self.glyph_y_points[i])
            new = Point(x, y)
            self.handel_locations.append(new)
            

    # Update Logic.
    def update(self):
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
            # self.next_point()
            pass






    # Draw Logic.
    def draw(self):
        pyxel.cls(COL_BACKGROUND)
        self.draw_handels()
        self.draw_active_handel()


    def draw_active_handel(self):
        x = self.location.x
        y = self.location.y
        pyxel.circ(x, y, 2, 11)


    def draw_handels(self):
        last_location = None
        # [TODO] Put zoom code here.
        for j in self.handel_locations:
            x1 = j.x
            y1 = j.y
            if last_location == None:
                x2 = j.x
                y2 = j.y
            else:
                x2 = last_location.x
                y2 = last_location.y

            pyxel.line(x1, y1, x2, y2, 14)
            pyxel.circ(x1, y1, 4, 14)

            location = "(" + str(j.x) + "," + str(j.y) + ")"
            pyxel.text(x1 + 6, y1 - 2, location, 11)
            last_location = j


# Call Application
if __name__ == "__main__":
    Bez()
