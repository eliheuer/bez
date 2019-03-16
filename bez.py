############################
#                          #
# Bez: A Simple UFO Editor #
#                          #
############################


import argparse
import pyxel
import xmltodict

COL_BACKGROUND = 0  # Background color
COL_INFO = 11       # Text color
WIDTH = 255         # Workspace width
HEIGHT = 255        # Workspace height


class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.line_type = line_type

class Bez:

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, caption="Bez", fps=60)
        pyxel.image(0).load(0, 0, "assets/pencil_16x16.png")
        pyxel.mouse(True)
        self.read_glif()
        self.reset()
        pyxel.run(self.update, self.draw)
 
    def reset(self):
        self.location = Point(WIDTH / 2, HEIGHT / 2)
        self.handel_locations = []
        self.zoom = 25
        self.zoom_flag = False
        self.generate_handels()

    def create_arg_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", help = "input filename")
        args = parser.parse_args()
        return args

    def use_arg_parser():
        args = create_arg_parser()
        glif_path = args.i

    def read_glif(self):
        """Reads glyph data from UFO files, creates global variables"""
        print("[+] Reading A_.glif")

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

    def generate_handels(self):
        for i in range(len(self.glyph_x_points)):
            x = int(self.glyph_x_points[i])
            y = int(self.glyph_y_points[i])
            p = Point(x, y)
            self.handel_locations.append(p)

    # Update Logic.
    def update(self):
        """
        Set hotkeys to quit (Q) and reset (R)
        """
        self.update_location()
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_location(self):
        """
        Updates location of points
        """
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

        if pyxel.btn(pyxel.KEY_UP) and not pyxel.btn(pyxel.KEY_DOWN):
            if self.location.y < HEIGHT - 11:
                old = self.location
                new = Point(old.x, old.y + 1)
                self.location = new
        elif pyxel.btn(pyxel.KEY_DOWN) and not pyxel.btn(pyxel.KEY_UP):
            if self.location.x > 0:
                old = self.location
                new = Point(old.x, old.y - 1)
                self.location = new

        elif pyxel.btn(pyxel.KEY_SPACE):
            # self.next_point()
            pass


    # Draw Logic.
    def draw(self):
        pyxel.cls(COL_BACKGROUND)
        self.draw_em_square()
        self.draw_handels()
        self.draw_active_handel()

    def draw_active_handel(self):
        x = self.location.x
        y = self.location.y
        pyxel.circ(x, y, 2, 11)
        active_location = "("+str(int(x))+","+str(int(y))+")"
        pyxel.text(x + 1, y + 3, active_location, 11)

    def draw_em_square(self):
        glyph_width = 150
        glyph_height = 200
        col = 1
        bottom_edge = (HEIGHT - glyph_height) / 2
        left_edge = (WIDTH - glyph_width) / 2

        # Left edge
        pyxel.line(left_edge, bottom_edge,
                   left_edge, bottom_edge + glyph_height, col)
        
        # Right edge
        pyxel.line(left_edge + glyph_width, bottom_edge,
                   left_edge + glyph_width, bottom_edge + glyph_height, col)
        
        # Top edge
        pyxel.line(left_edge, bottom_edge,
                   left_edge + glyph_width, bottom_edge, col)
    
        # Bottom edge
        pyxel.line(left_edge, bottom_edge + glyph_height,
                   left_edge + glyph_width, bottom_edge + glyph_height, col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 10,
                   left_edge + glyph_width, bottom_edge + 10, col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 20,
                   left_edge + glyph_width, bottom_edge + 20, col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 90,
                   left_edge + glyph_width, bottom_edge + 90, col)

        # Bottom edge
        pyxel.line(left_edge, bottom_edge + 150,
                   left_edge + glyph_width, bottom_edge + 150, col)

    def draw_handels(self):
        last_location = None

        if self.zoom == 25 and self.zoom_flag == False:
            self.handel_locations_zoomed = []
            for i in self.handel_locations:
                x = (i.x / 4) + 50
                y = (i.y / 4) + 50
                #t = i.t
                p = Point(x, y)
                self.handel_locations_zoomed.append(p)
            #self.handel_locations = self.handel_locations_zoomed
            self.zoom_flag = True

        for j in self.handel_locations_zoomed:
            x1 = j.x
            y1 = j.y
            if last_location == None:
                x2 = j.x
                y2 = j.y
                fx = j.x
                fy = j.y
                lx = j.x
                ly = j.y
            else:
                x2 = last_location.x
                y2 = last_location.y
            pyxel.line(x1, y1, x2, y2, 8)
            pyxel.circ(x1, y1, 2, 8)
            location = "("+str(int(j.x))+","+str(int(j.y))+")"
            pyxel.text(x1 + 1, y1 + 3, location, 11)
            last_location = j
        list_len = len(self.handel_locations_zoomed)
        print(list_len)
        fx = self.handel_locations_zoomed[0].x
        fy = self.handel_locations_zoomed[0].y
        lx = j.x
        ly = j.y
        pyxel.line(fx, fy, lx, ly, 8)


# Call Application
if __name__ == "__main__":
    Bez()
