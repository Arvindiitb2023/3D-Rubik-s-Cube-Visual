from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QWheelEvent
from PyQt6.QtCore import QThread, pyqtSignal,Qt,QTimer
import sys
import numpy as np
from model import OpenGLWidget
from cube_shuffler import State

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


class InvertedPendulam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.object = OpenGLWidget(self)
        
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.object)
        container.setLayout(main_layout) 
        self.setCentralWidget(container)

        self.shuffle = State()
        self.threads = []
        self.target_at = 85
        self.step_at = 5

    def update_motion(self,state):
        self.object.state = state
        self.object.update()

    def animate_rotation(self, axis ,i,j,idx,d):
      def update():
        if self.object.angles[i][j] != d*self.target_at:
            self.object.angles[i][j] += self.step_at*d
            self.object.update()
        else:
            self.timer.stop()
            self.object.angles[i][j] -= d*self.target_at  # Reset
            thread = SimulationThread(self.shuffle, self.object, axis,idx,d)
            thread.update_signal.connect(self.update_motion)
            thread.finished.connect(lambda: self.threads.remove(thread))
            self.threads.append(thread)
            thread.start()

      self.timer = QTimer()
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



    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.object.last_mouse_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
      if event.buttons() & Qt.MouseButton.LeftButton and self.object.last_mouse_pos:
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