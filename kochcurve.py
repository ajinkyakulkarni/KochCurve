#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk

WIDTH=600
HEIGHT=600
window = tk.Tk()
window.title("Koch Curve")
canvas = tk.Canvas(window, width=600, height=600, bg='white')
canvas.pack()

from math import cos, sin, radians, sqrt

class Point:
    # a list with two items
    def __init__(self, xcoord=0, ycoord=0):
        self.point = [xcoord, ycoord]
    
    def __getitem__(self, index):
        return self.point[index]
    
    def __setitem__(self, index, value):
        self.point[index]= value
    
    def __str__(self):
        return "Point: " + str(self.point)
        
class Vector:
    # Position vector.
    def __init__(self, point):
        # point is the tip, [0,0] the tail
        self.point = point
    
    def __getitem__(self, index):
        return self.point[index]
    
    def __str__(self):
        return "Vector: <" + str(self.point[0]) +', ' + str(self.point[1]) + '>'

class Line:
    def __init__(self, start, end, level=0):
        ''' create a line from Point or position vector start to Point or p-v end and depth level level'''
        self.start = start
        self.end = end
        self.level = level
        
    def draw(self, color='blue'):
        ''' draw the line on the canvas'''
        canvas.create_line(self.start[0], self.start[1], self.end[0], self.end[1],
            fill=color, tags='line')
        
    def __str__(self):
        ''' return a string describing the line state'''
        return "Line: " + str(self.start) + '-' + str(self.end) + ' Level ' + str(self.level)

def get_sublines(line):
    ''' Return a list of 4 sublines of line line
    
    Create 4 new lines using subdivision points of line
    '''
    points = get_subdivisions(line.start, line.end)
    lines = []
    lines.append(Line(points[0], points[1], line.level + 1))
    lines.append(Line(points[1], points[2], line.level + 1))
    lines.append(Line(points[2], points[3], line.level + 1))
    lines.append(Line(points[3], points[4], line.level + 1))
    return lines
    
        
def get_position_vector(A, B):
    # A & B are position vectors or just points defining a vector
    return Vector(Point(B[0]-A[0], B[1]-A[1]))

def rotate(axis, point, grades):
    # TODO eliminar calculos y accesos repetidos
    new_point = Point()
    new_point[0]=axis[0] + (point[0]-axis[0])*cos(radians(grades)) - (point[1]-axis[1])*sin(radians(grades))
    new_point[1]=axis[1] + (point[0]-axis[0])*sin(radians(grades)) + (point[1]-axis[1])*cos(radians(grades))
    return new_point

def drawLine(start, end, color='blue'):
    # A & B are position vectors or points
    canvas.create_line(start[0], start[1], end[0], end[1], fill=color, tags='line')
    
def get_subdivisions(tail, tip):
    # tail & tip are position vectors or just points defining a vector that represemt a line
    ''' return a list with position vectors to subdivisions '''
    v = get_position_vector(tail, tip)
    B = Vector(Point(v[0]/3.0 + tail[0], v[1]/3.0 + tail[1]))
    D = Vector(Point(v[0]*2/3 + tail[0], v[1]*2/3 + tail[1]))
    C = Vector(rotate(B, D, -60))
    pointlist = []
    pointlist.append(tail)
    pointlist.append(B)
    pointlist.append(C)
    pointlist.append(D)
    pointlist.append(tip)    
    return pointlist

def must_draw(line):
    # check if line is at final level and therefore should be drawn.
    # class Line has an attribute level which defines its own level
    
    level = int(spinbox.get()) # level better global updated every time buttons clicked
    # the problem of changing the spinbox while drawing
    
    return line.level == level

def kochCurve(line):
    ''' Generate and draw a Koch curve.
    
    Call this function three times for each line of an equilateral triangle
    and get a snowflake. This is the main backtracking algorythm.
    '''
    if must_draw(line):
        line.draw()
        #canvas.update()
    else:
        for subline in get_sublines(line):
            kochCurve(subline)

def drawKoch(event):
    # if event from button Curve draw a curve
    canvas.delete('line') # clear the canvas
    if event.widget == buttonCurve:
        start = Point(0,HEIGHT*2/3)
        end = Point(WIDTH,HEIGHT*2/3)
        kochCurve(Line(start, end)) # vuelta-atrás
    # if event from button snowflake draw a snowflake

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
    p1 = Point(100,350)
    print p1
    p2 = Point(500,150)
    l = Line(p1, p2)
    print l
    #for subline in get_sublines(l): print subline
    vectors = get_subdivisions(Vector(p1), Vector(p2))
    for v in vectors: print v
    drawLine(vectors[0], vectors[1])
    drawLine(vectors[1], vectors[2])
    drawLine(vectors[2], vectors[3])
    drawLine(vectors[3], vectors[4])
    return 0

if __name__ == '__main__':
    test()

window.mainloop()
