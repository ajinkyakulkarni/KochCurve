#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  kochcurve.py
#  
#  2016 Maximiliano G. G.
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from sys import exit
from math import cos, sin, radians

try:
    import Tkinter as tk # Python < 3
except ImportError:
    try:
        import tkinter as tk
    except ImportError:
        sys.exit("No tkinter module installed")

WIDTH=600
HEIGHT=600

window = tk.Tk()
window.title("Koch Curve")
window.resizable(width=False, height=False)

canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg='white')
canvas.pack(side=tk.TOP)

class Point:
    def __init__(self, xcoord=0, ycoord=0):
        self.point = [xcoord, ycoord]
    
    def __getitem__(self, index):
        return self.point[index]
    
    def __setitem__(self, index, value):
        self.point[index]= value
    
    def __str__(self):
        ''' Return a string describing the point '''
        return "Point: " + str(self.point)
        
class Vector:
    ''' Position vector
    
    Although you can use a point as a position vector, they are conceptually different.
    '''
    def __init__(self, point):
        # point is the tip (and Point [0,0] the tail)
        self.point = point
    
    def __getitem__(self, index):
        return self.point[index]
    
    def __str__(self):
        ''' Return a string describing the vector '''
        return 'Vector: <' + str(self.point[0]) +', ' + str(self.point[1]) + '>'

class Line:
    def __init__(self, start, end, level=0):
        ''' Create a line from start to end
        
        start & end are Points or Position vectors while level specifies the
        depth level or step at which the line belongs.
        '''
        self.start = start
        self.end = end
        self.level = level # we can access this value directly or defining a getter/setter
        
    def draw(self, color='blue'):
        ''' Draw the line on the canvas '''
        canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1],
            fill=color, tags='line')
        
    def __str__(self):
        ''' Return a string describing the line '''
        return "Line: " + str(self.start) + '-' + str(self.end) + ' Level ' + str(self.level)

def get_sublines(line):
    ''' Return a list of 4 sublines of line line
    
    Create 4 new lines using subdivision points of line.
    '''
    points = get_subdivisions(line.start, line.end)
    return [Line(points[0], points[1], line.level + 1),
        Line(points[1], points[2], line.level + 1),
        Line(points[2], points[3], line.level + 1),
        Line(points[3], points[4], line.level + 1)]

def get_position_vector(A, B):
    # A & B are position vectors or just points defining a vector
    return Vector(Point(B[0]-A[0], B[1]-A[1]))

def rotate(axis, point, grades):
    new_point = Point()
    r_grades = radians(grades)
    new_point[0]=axis[0] + (point[0]-axis[0])*cos(r_grades) - (point[1]-axis[1])*sin(r_grades)
    new_point[1]=axis[1] + (point[0]-axis[0])*sin(r_grades) + (point[1]-axis[1])*cos(r_grades)
    return new_point
    
def get_subdivisions(tail, tip):
    ''' return a list with position vectors to subdivisions
    
    tail(A) & tip(E) are position vectors or just points defining a vector that represent a line
         /C\
    A__B/   \D__E
    '''
    v = get_position_vector(tail, tip)
    B = Vector(Point(v[0]/3.0 + tail[0], v[1]/3.0 + tail[1]))
    D = Vector(Point(v[0]*2/3.0 + tail[0], v[1]*2/3.0 + tail[1]))
    C = Vector(rotate(B, D, -60))
    return [tail,B,C,D,tip]
    
def must_draw(line):
    ''' Check if line is at final level and therefore should be drawn. '''
    level = int(spinbox.get())
    # level better global and updated only before the first call to main algorithm
    # because changing the spinbox while drawing causes a bug
    return line.level == level

def kochCurve(line):
    ''' Generate and draw a Koch curve.
    
    Call this function three times for each line of an equilateral triangle
    and get a snowflake. This is the main backtracking algorythm. Cool!
    '''
    if must_draw(line):
        line.draw()
        #canvas.update() # uncomment this line to see how it is created step by step
    else:
        for subline in get_sublines(line):
            kochCurve(subline)

def drawKoch(event):
    canvas.delete('line') # clean the canvas
    canvas.create_text(WIDTH/2, HEIGHT/2, anchor=tk.CENTER, text="Calculating...", tags="text", fill='black')
    canvas.update()
    if event.widget == buttonCurve:
        # clicked buttonCurve
        start = Point(0,HEIGHT*2/3)
        end = Point(WIDTH,HEIGHT*2/3)
        kochCurve(Line(start, end)) # backtracking
    elif event.widget == buttonSnowflake:
        # clicked buttonSnowflake
        # call three times kochCurve for each line of an equilateral triangle
        point1 = Point(100,175)
        point2 = Point(WIDTH-100,175)
        point3 = rotate(point1, point2, 60)
        kochCurve(Line(point1, point2))
        kochCurve(Line(point2, point3))
        kochCurve(Line(point3, point1))
    canvas.delete('text')
    
# Buttons and Spinbox
#
# button for create a koch curve
buttonCurve = tk.Button(window, text="Koch Curve")
buttonCurve.bind('<Button-1>', drawKoch)
buttonCurve.pack(side=tk.LEFT, fill=tk.X, expand=1)

# button for create a koch snowflake
buttonSnowflake = tk.Button(window, text="Koch Snowflake")
buttonSnowflake.bind('<Button-1>', drawKoch)
buttonSnowflake.pack(side=tk.LEFT, fill=tk.X, expand=1)

# label for spinbox level selection
labelLevel = tk.Label(window, anchor=tk.E, text="Level")
labelLevel.pack(side=tk.LEFT)

# spinbox for level selection
spinbox = tk.Spinbox(window, from_=0, to=10, increment=1, width=2)
spinbox.pack(side=tk.LEFT)    
    
def test():
    return 0

if __name__ == '__main__':
    test()

window.mainloop()
