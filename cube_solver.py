import kociemba as kb
class solver():
    def __init__(self,state):
        self.state = state
        self.moves = []
        self.solved = False
        self.colormap = {
            'W' : 'F',
            'Y' : 'B',
            'R' : 'L', 
            'O' : 'R',
            'G' : 'U',
            'B' : 'D',
        }
        self.facelets = {
            'U': ['U'] * 9,
            'D': ['D'] * 9,
            'L': ['L'] * 9,
            'R': ['R'] * 9,
            'F': ['F'] * 9,
            'B': ['B'] * 9
        }
    def getting_strings(self):
        
        for pos , colors in self.state.items():
            x,y,z = pos
            c1,c2,c3 = colors
            if y == 1:
                self.set_facelet('U', pos, c2)
            if y == -1:
                self.set_facelet('D', pos, c2)
            if x == -1:
                self.set_facelet('L', pos, c1)
            if x == 1:
                self.set_facelet('R', pos, c1)
            if z == 1:
                self.set_facelet('F', pos, c3)
            if z == -1:
                self.set_facelet('B', pos, c3)
            # Joining lists together and converting to string
        final_string = ''.join(
                        self.facelets['U'] +
                        self.facelets['R'] +
                        self.facelets['F'] +
                        self.facelets['D'] +
                        self.facelets['L'] +
                        self.facelets['B']
                        )

        return kb.solve(final_string)
            
    def set_facelet(self, face, pos, color):
        x, y, z = pos
        # Map depending on face
        if face == 'U':
            row = z + 1
            col = x + 1
        elif face == 'D':
            row = -z + 1  # Inverted Z
            col = x + 1
        elif face == 'L':
            row = -y + 1  # Inverted Y
            col = z + 1  
        elif face == 'R':
            row = -y + 1
            col =  -z + 1
        elif face == 'F':
            row = -y + 1
            col = x + 1
        elif face == 'B':
            row = -y + 1
            col = -x + 1  # Inverted X
        else:
            raise ValueError(f"Unknown face: {face}")

        index = row * 3 + col
        self.facelets[face][index] = self.colormap[color]


        