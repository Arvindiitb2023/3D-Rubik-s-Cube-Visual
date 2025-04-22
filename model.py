from PyQt6.QtOpenGLWidgets import QOpenGLWidget 
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import math
import sys

AXIS_M = [(1,0,0) ,(-1,0,0) ,(0,1,0),(0,-1,0) ,(0,0,1),(0,0,-1)]
AXIS_B = [
    # Edges on the Top (Y = +2)
    ( 1,  1,  0),  # X+ Y+
    (-1,  1,  0),  # X- Y+
    ( 0,  1,  1),  # Y+ Z+
    ( 0,  1, -1),  # Y+ Z-

    # Edges on the Bottom (Y = -2)
    ( 1, -1,  0),  # X+ Y-
    (-1, -1,  0),  # X- Y-
    ( 0, -1,  1),  # Y- Z+
    ( 0, -1, -1),  # Y- Z-

    # Edges on the Middle layer (Y = 0)
    ( 1,  0,  1),  # X+ Z+
    (-1, 0,  1),   # X- Z+
    ( 1,  0, -1),  # X+ Z-
    (-1, 0, -1)    # X- Z-
]
AXIS_C = [(1,1,1) , (-1,1,1) , (1,-1,1) , (-1,-1,1) , (1,1,-1) , (-1,1,-1) , (1,-1,-1) , (-1,-1,-1)]

COLOR_MAP = {
    'W' : [1,1,1],
    'R' : [1,0,0],
    'G' : [0,1,0],
    'B' : [0,0,1],
    'O' : [1,0.5,0],
    'Y' : [1,1,0],
    'D' : [0,0,0]
}

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.camera_distance = 10.0
        self.camera_azimuth = 45.0
        self.camera_elevation = 30.0
        self.spacing = 1.02
        self.angles = [[0,0,0],[0,0,0] ,[0,0,0]] # x,y,z 
        # lets try other method see lets assign number to every one what when rotated they change the position and accoring to that we will rotate it 
        self.state={
            (-1,1,1) : ['R' , 'G' , 'W'],
            (0,1,1)  : ['D' , 'G' ,'W'],
            (1,1,1)  : ['O','G' ,'W'],
            
            (-1,1,0) : ['R' ,'G' , 'D'],
            (0,1,0)  : ['D' , 'G' ,'D'],
            (1,1,0)  : ['O' , 'G','D'],

            (-1,1,-1) : ['R' , 'G' , 'Y'],
            (0,1,-1) : ['D' , 'G' ,'Y'],
            (1,1,-1)  : ['O','G' ,'Y'],

            (-1,0,1) : ['R' , 'D' , 'W'],
            (0,0,1)  : ['D' , 'D' ,'W'],
            (1,0,1)  : ['O','D' ,'W'],
            
            (-1,0,0) : ['R' ,'D' , 'D'],
            (0,0,0)  : ['D' , 'D' ,'D'],
            (1,0,0)  : ['O' , 'D','D'],

            (-1,0,-1) : ['R' , 'D' , 'Y'],
            (0,0,-1) : ['D' , 'D' ,'Y'],
            (1,0,-1)  : ['O','D' ,'Y'],

            (-1,-1,-1) : ['R' , 'B' , 'Y'],
            (0,-1,-1)  : ['D' , 'B' ,'Y'],
            (1,-1,-1)  : ['O','B' ,'Y'],
            
            (-1,-1,0) : ['R' ,'B' , 'D'],
            (0,-1,0)  : ['D' , 'B' ,'D'],
            (1,-1,0)  : ['O' , 'B','D'],

            (-1,-1,1) : ['R' , 'B' , 'W'],
            (0,-1,1)  : ['D' , 'B' ,'W'],
            (1,-1,1)  : ['O','B' ,'W'],

        }

        
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h != 0 else 1
        gluPerspective(45.0, aspect, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        azimuth_rad = math.radians(self.camera_azimuth)
        elevation_rad = math.radians(self.camera_elevation)
        x = self.camera_distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
        y = self.camera_distance * math.sin(elevation_rad)
        z = self.camera_distance * math.cos(elevation_rad) * math.cos(azimuth_rad)
        gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        
        for axis,color in self.state.items():
            if axis in AXIS_C:
                glPushMatrix()
                if axis[0] == 1:
                    self.rotate_right(self.angles[0][0])
                if axis[1] == 1:
                    self.rotate_top(self.angles[1][0])
                if axis[2] == 1:
                    self.rotate_front(self.angles[2][0])
                
                if axis[0] == 0:
                    self.rotate_right(self.angles[0][1])
                if axis[1] == 0:
                    self.rotate_top(self.angles[1][1])
                if axis[2] == 0:
                    self.rotate_front(self.angles[2][1])
                
                if axis[0] == -1:
                    self.rotate_right(self.angles[0][2])
                if axis[1] == -1:
                    self.rotate_top(self.angles[1][2])
                if axis[2] == -1:
                    self.rotate_front(self.angles[2][2])
            
                self.corners(axis,color)
                glPopMatrix()

            elif axis in AXIS_B:
                glPushMatrix()

                if axis[0] == 1:
                    self.rotate_right(self.angles[0][0])
                if axis[1] == 1:
                    self.rotate_top(self.angles[1][0])
                if axis[2] == 1:
                    self.rotate_front(self.angles[2][0])

                if axis[0] == 0:
                    self.rotate_right(self.angles[0][1])
                if axis[1] == 0:
                    self.rotate_top(self.angles[1][1])
                if axis[2] == 0:
                    self.rotate_front(self.angles[2][1])
                
                if axis[0] == -1:
                    self.rotate_right(self.angles[0][2])
                if axis[1] == -1:
                    self.rotate_top(self.angles[1][2])
                if axis[2] == -1:
                    self.rotate_front(self.angles[2][2])

                self.middle(axis,color)
                glPopMatrix()

            elif axis in AXIS_M:
                glPushMatrix()
                
                if axis[0] == 1:
                    self.rotate_right(self.angles[0][0])
                if axis[1] == 1:
                    self.rotate_top(self.angles[1][0])
                if axis[2] == 1:
                    self.rotate_front(self.angles[2][0])

                if axis[0] == 0:
                    self.rotate_right(self.angles[0][1])
                if axis[1] == 0:
                    self.rotate_top(self.angles[1][1])
                if axis[2] == 0:
                    self.rotate_front(self.angles[2][1])

                if axis[0] == -1:
                    self.rotate_right(self.angles[0][2])
                if axis[1] == -1:
                    self.rotate_top(self.angles[1][2])
                if axis[2] == -1:
                    self.rotate_front(self.angles[2][2])

 
                self.center(axis,color)
                glPopMatrix()



    def corners(self, axis,color):

        loc = [axis[0] , axis[1] , axis[2]] 
        loc = [coord * self.spacing for coord in loc]
        glTranslatef(*loc)
        glBegin(GL_QUADS)
        self.FB(axis,color) # Front (+Z) (-Z)
        self.LR(axis,color) # Left (-X ,X)
        self.UD(axis,color)  # Top (+Y)(-Y)
        glEnd()

    def middle(self,axis,color):
        loc = [axis[0] , axis[1] , axis[2]] 
        loc = [coord * self.spacing for coord in loc]
        glTranslatef(*loc)
        glBegin(GL_QUADS)
        if axis[0] == 0:
           self.FB(axis,color)
           self.UD(axis,color)
        elif axis[1] == 0:
           self.FB(axis,color)
           self.LR(axis,color)
        else:
           self.LR(axis,color)
           self.UD(axis,color)
        glEnd()

    def center(self, axis,color):
        loc = [axis[0] , axis[1] , axis[2]] 
        loc = [coord * self.spacing for coord in loc]
        glTranslatef(*loc)
        glBegin(GL_QUADS)
        if axis[2] != 0 : # Front (+Z) (-Z)
            self.FB(axis,color)
        elif axis[0] != 0: # Left (-X ,X)
            self.LR(axis,color)
        else:               # Top (+Y)(-Y)
            self.UD(axis,color)
        glEnd()
    
    def rotate_top(self,angle):
        glTranslatef(0.0, 1.05, 0.0)  # move to top layer
        glRotatef(angle, 0.0, 1.0, 0.0)  # rotate around Y-axis
        glTranslatef(0.0, -1.05, 0.0)  # move back

    def rotate_right(self,angle):
        glTranslatef(1.05, 0, 0.0)  # move to top layer
        glRotatef(angle, 1.0, 0.0, 0.0)  # rotate around Y-axis
        glTranslatef(-1.05, 0, 0.0)  # move back
    
    def rotate_front(self,angle):
        glTranslatef(0, 0, 1.05)  # move to top layer
        glRotatef(angle, 0, 0.0, 1.0)  # rotate around Y-axis
        glTranslatef(0, 0, -1.05)  # move back

    
    def FB(self,axis,color):
        color = COLOR_MAP[color[2]]
        glColor3f(*color)
        glVertex3f( 0.5,  0.5,  axis[2]*0.5)
        glVertex3f( 0.5, -0.5,  axis[2]*0.5)
        glVertex3f(-0.5, -0.5,  axis[2]*0.5)
        glVertex3f(-0.5,  0.5,  axis[2]*0.5)

    def LR(self,axis,color):
        color = COLOR_MAP[color[0]]
        glColor3f(*color)
        glColor(*color)
        glVertex3f(0.5*axis[0],  0.5,  0.5)
        glVertex3f(0.5*axis[0], -0.5,  0.5)
        glVertex3f(0.5*axis[0], -0.5, -0.5)
        glVertex3f(0.5*axis[0],  0.5, -0.5)

    def UD(self,axis,color):
        color = COLOR_MAP[color[1]]
        glColor3f(*color)
        glColor(*color)
        glVertex3f( 0.5,  0.5*axis[1],  0.5)
        glVertex3f(-0.5,  0.5*axis[1],  0.5)
        glVertex3f(-0.5,  0.5*axis[1], -0.5)
        glVertex3f( 0.5,  0.5*axis[1], -0.5)


        




       