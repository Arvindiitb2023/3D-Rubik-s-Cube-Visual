class shuffler():
    def __init__(self):
        self.state = 27
    
    def rotate_layer(self,state, axis, index, direction):
        transformed = {}

        for pos, faces in state.items():
            x, y, z = pos
            if (axis == 'y' and y == index):
                if direction == 1:
                    new_x, new_z = z, -x
                    new_faces = [faces[2], faces[1], faces[0]]  # Z → X, Y stays, X → Z
                else:
                    new_x, new_z = -z, x
                    new_faces = [faces[2], faces[1], faces[0]]  # Z → X, Y stays, X → Z
                transformed[(new_x, y, new_z)] = new_faces
    
            elif axis == 'x' and x == index:
                if direction == 1:
                    new_y, new_z = -z, y
                    new_faces = [faces[0], faces[2], faces[1]]  # X stays, Y <-> Z
                else:
                    new_y, new_z = z, -y
                    new_faces = [faces[0], faces[2], faces[1]]
                transformed[(x, new_y, new_z)] = new_faces
            
            elif axis == 'z' and z == index:
                if direction == 1:
                    new_x, new_y = -y, x
                    new_faces = [faces[1], faces[0], faces[2]]  # Z stays, Y <-> Z
                else:
                    new_x, new_y = y, -x
                    new_faces = [faces[1], faces[0], faces[2]]
                transformed[(new_x, new_y, z)] = new_faces
            else:
                transformed[pos] = faces

        return transformed
