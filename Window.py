from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QWheelEvent
from PyQt6.QtCore import QThread, pyqtSignal,Qt,QTimer
import sys
from model import OpenGLWidget
from cube_shuffler import shuffler
from cube_solver import solver 

class SimulationThread(QThread):
    update_signal = pyqtSignal(object)
    def __init__(self,shuffle,object,axis,idx,d):
        super().__init__()
        self.object = object
        self.shuffle = shuffle
        self.axis = axis
        self.idx = idx
        self.d = d
    def run(self):
            new_state = self.shuffle.rotate_layer(self.object.state , self.axis ,self.idx, self.d) # direction 1 = cw -1 ccw
            self.update_signal.emit(new_state)

class solver_thread(QThread):
    update_signal = pyqtSignal(object)
    def __init__(self,object):
        super().__init__()
        self.object = object
        self.solver = solver(self.object.state)
    def run(self):
        self.string = self.solver.getting_strings()
        self.update_signal.emit(self.string)


class InvertedPendulam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.object = OpenGLWidget(self)
        
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.object)
        container.setLayout(main_layout) 
        self.setCentralWidget(container)
        self.shuffle = shuffler()
        self.threads = []
        self.target_at = 85
        self.step_at = 5
        self.move_queue = []
        self.currently_animating = False

    def update_motion(self, new_state):
        self.object.state = new_state
        self.object.update()
    def update_motion3(self, moves):
        print(moves)
        self.move_queue = moves.split()
        self.currently_animating = False
        self.process_next_move()

    def process_next_move(self):
        if not self.move_queue:
            self.currently_animating = False
            return  # No more moves

        move = self.move_queue.pop(0)  # Get the next move
        self.currently_animating = True

        if move == 'U':
         self.animate_rotation('y',1,0,1,-1, callback=self.process_next_move)
        elif move == "U'":
         self.animate_rotation('y',1,0,1,1, callback=self.process_next_move)
        elif move == 'D':
         self.animate_rotation('y',1,2,-1,1, callback=self.process_next_move)
        elif move == "D'":
         self.animate_rotation('y',1,2,-1,-1, callback=self.process_next_move)
        elif move == 'L':
         self.animate_rotation('x',0,2,-1,1, callback=self.process_next_move)
        elif move == "L'":
         self.animate_rotation('x',0,2,-1,-1, callback=self.process_next_move)
        elif move == 'R':
         self.animate_rotation('x',0,0,1,-1, callback=self.process_next_move)
        elif move == "R'":
         self.animate_rotation('x',0,0,1,1, callback=self.process_next_move)
        elif move == 'F':
         self.animate_rotation('z',2,0,1,-1, callback=self.process_next_move)
        elif move == "F'":
         self.animate_rotation('z',2,0,1,1, callback=self.process_next_move)
        elif move == 'B':
         self.animate_rotation('z',2,2,-1,1, callback=self.process_next_move)
        elif move == "B'":
         self.animate_rotation('z',2,2,-1,-1, callback=self.process_next_move)
        elif move == 'U2':
         self.move_queue = ['U', 'U'] + self.move_queue
         self.process_next_move()
        elif move == 'D2':
         self.move_queue = ['D', 'D'] + self.move_queue
         self.process_next_move()
        elif move == 'L2':
         self.move_queue = ['L', 'L'] + self.move_queue
         self.process_next_move()
        elif move == 'R2':
         self.move_queue = ['R', 'R'] + self.move_queue
         self.process_next_move()
        elif move == 'F2':
         self.move_queue = ['F', 'F'] + self.move_queue
         self.process_next_move()
        elif move == 'B2':
         self.move_queue = ['B', 'B'] + self.move_queue
         self.process_next_move()


    def animate_rotation(self, axis ,i,j,idx,d,callback=None):
      self.timer = QTimer()
      def update():
        if self.object.angles[i][j] != d*self.target_at:
            self.object.angles[i][j] += self.step_at*d
            self.object.update()
        else:
            self.object.angles[i][j] = 0 # Reset
            self.timer.stop()
            thread = SimulationThread(self.shuffle, self.object, axis,idx,d)
            thread.update_signal.connect(self.update_motion)
            thread.finished.connect(lambda: self.threads.remove(thread))
            if callback:
               thread.finished.connect(callback)
            # thread.finished.connect(callback)
            self.threads.append(thread)
            thread.start()
    
      self.timer.timeout.connect(update)
      self.timer.start(15)  



  # moments code
  
    def keyPressEvent(self, event):
        key = event.key()
        if event.key() == Qt.Key.Key_W:
            self.animate_rotation('y',1,0,1,1)
        if key == Qt.Key.Key_R:
            self.animate_rotation('x',0,0,1,1)
        if key == Qt.Key.Key_E:
            self.animate_rotation('z',2,0,1,1)
        
        if event.key() == Qt.Key.Key_W and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.animate_rotation('y',1,1,0,1)
        if event.key() == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.animate_rotation('x',0,1,0,1)
        if key == Qt.Key.Key_E and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.animate_rotation('z',2,1,0,1)

        if event.key() == Qt.Key.Key_W and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.animate_rotation('y',1,2,-1,1)
        if event.key() == Qt.Key.Key_R and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.animate_rotation('x',0,2,-1,1)
        if key == Qt.Key.Key_E and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.animate_rotation('z',2,2,-1,1)

        if key == Qt.Key.Key_Space:
            self.solver = solver_thread(self.object)
            self.solver.update_signal.connect(self.update_motion3)
            self.solver.start()
        if event.key() == Qt.Key.Key_C:  # Press 'C' to toggle coloring mode
            self.object.coloring_mode = not self.object.coloring_mode
            print("Coloring mode:", self.object.coloring_mode)
            



    
        

    def mouseMoveEvent(self, event):
      if event.buttons() & Qt.MouseButton.RightButton :
        current_pos = event.position().toPoint()
        dx = current_pos.x() - self.object.last_mouse_pos.x()
        dy = current_pos.y() - self.object.last_mouse_pos.y()

        # Sensitivity tuning
        self.object.camera_azimuth += dx * 0.5
        self.object.camera_elevation += dy * 0.5

        # Clamp elevation to avoid flipping
        self.object.camera_elevation = max(-89.0, min(89.0, self.object.camera_elevation))

        self.object.last_mouse_pos = current_pos
        self.object.update()

    def wheelEvent(self, event: QWheelEvent):
        # Check for Ctrl key held down
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            # Positive delta = scroll up (zoom in), negative = scroll down (zoom out)
            if delta > 0:
                self.object.camera_distance = max(10.0, self.object.camera_distance - 5)
            else:
                self.object.camera_distance += 5

            self.object.update()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvertedPendulam()
    window.show()
    sys.exit(app.exec())  