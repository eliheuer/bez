# Library and module imports
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
        for i in range(0, 9):
            self.generate_handel()

    def read_glif(self):
        print("[+] Reading E_.glig")
        try:
            with open('E_.glif') as fd:
                self.glif = xmltodict.parse(fd.read())
        except FileNotFoundError:
            print("[!] Error: File not found")
        else:
            print("[!] Done\n")

        # Name 
        glyph_name = self.glif['glyph']['@name']
        print("glyph name:\t", glyph_name)

        # Format 
        glyph_format = self.glif['glyph']['@format']
        print("glyph format:\t", glyph_format)

        # Width 
        glyph_width = self.glif['glyph']['advance']['@width']
        print("glyph width:\t", glyph_width)
        
    def generate_handel(self):
        valid = False
        while not valid:
            x = randint(8, WIDTH + 100)
            y = randint(8, HEIGHT - 8)
            new = Point(x, y)
            valid = True
            for i in self.handel_locations:
                if x == i.x and y == i.y:
                    valid = False
            if valid:
                self.handel_locations.append(new)

    # Update Logic.
    def update(self):
        if not self.done:
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
        if not self.done:
            pyxel.cls(COL_BACKGROUND)
            self.draw_em_square()
            self.test_blt()
            self.draw_active_handel()
            self.draw_info()
            self.draw_handels()
        else:
            self.draw_death()

    def draw_em_square(self):
        glyph_width = 150
        glyph_height = 200
        bottom_edge = (HEIGHT - glyph_height) / 2
        left_edge = (WIDTH - glyph_width) / 2
        line_col = 1
        
        # Left edge
        pyxel.line(left_edge, bottom_edge,
                   left_edge, bottom_edge + glyph_height, line_col)
        
        # Right edge
        pyxel.line(left_edge + glyph_width, bottom_edge,
                   left_edge + glyph_width, bottom_edge + glyph_height, line_col)
        
        # Top edge
        pyxel.line(left_edge, bottom_edge,
                   left_edge + glyph_width, bottom_edge, line_col)
    
        # Bottom edge
        pyxel.line(left_edge, bottom_edge + glyph_height,
                   left_edge + glyph_width, bottom_edge + glyph_height, line_col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 10,
                   left_edge + glyph_width, bottom_edge + 10, line_col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 20,
                   left_edge + glyph_width, bottom_edge + 20, line_col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 90,
                   left_edge + glyph_width, bottom_edge + 90, line_col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 150,
                   left_edge + glyph_width, bottom_edge + 150, line_col)

    def test_blt(self):
        for i in range(4):
            pyxel.blt(8, (16*i)+134, 0, 0, 0, 16, 16)

    def draw_active_handel(self):
        x = self.location.x
        y = self.location.y
        pyxel.circ(x, y, 4, 11)

    def draw_handels(self):
        last_location = None
        for j in self.handel_locations:
            x1 = j.x
            y1 = j.y
            if last_location == None:
                x2 = j.x
                y2 = j.y
            else:
                x2 = last_location.x
                y2 = last_location.y

            pyxel.circ(x1, y1, 4, 8)
            pyxel.line(x1, y1, x2, y2, 8)

            location = "(" + str(j.x) + "," + str(j.y) + ")"
            pyxel.text(x1 + 6, y1 - 2, location, 11)
            last_location = j

    def draw_info(self):
        info = "{:09}".format(self.info)
        pyxel.rect(0, 0, WIDTH, 4, COL_BACKGROUND)
        pyxel.text(1, 1, info, COL_INFO)


# Call Application
if __name__ == "__main__":
    Bez()
