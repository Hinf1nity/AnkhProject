import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import cv2


class ImageDrawer:
    def __init__(self, width, height, hex_size=30):
        self.width = width
        self.height = height
        self.image = np.ones((self.height, self.width, 3),
                             dtype=np.uint8) * 255  # Imagen en blanco
        self.image_copy = []
        self.hex_size = hex_size
        self.hex = []

    def draw_image(self, image):
        image = cv2.imread(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.width, self.height))
        self.image = image
        self.image_copy = image.copy()

    def draw_hexagonal_grid(self):
        # Dibujar un tablero de hexágonos en la imagen
        count = 1
        print(self.image.shape)
        fig, ax = plt.subplots(figsize=(self.width, self.height), dpi=100)
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')

        rectangle = patches.Rectangle(
            (0, 0), self.width, self.height, color='black')
        ax.add_patch(rectangle)

        for i in range(self.hex_size, self.width, int(2 * self.hex_size)):
            flag = 0
            if count > 3:
                i = i-(count//2-1) * self.hex_size
            if count % 2 == 0:
                print("a")
                for j in range(5, self.height, int(np.sqrt(3) * self.hex_size)):
                    flag += 1
                    if flag == 1 or flag == 11:
                        continue
                    else:
                        hexagon = patches.RegularPolygon(
                            (i, j), numVertices=6, radius=self.hex_size, orientation=np.pi/6, edgecolor='black')
                        self.hex.append((i, j))
                        ax.add_patch(hexagon)
            else:
                if count == 1:
                    i = i+1 * self.hex_size
                for j in range(self.hex_size, self.height, int(np.sqrt(3) * self.hex_size)):
                    flag += 1
                    if (count == 1 or count == 11) and (flag == 1 or flag == 10):
                        continue
                    else:
                        hexagon = patches.RegularPolygon(
                            (i-0.5 * self.hex_size, j), numVertices=6, radius=self.hex_size, orientation=np.pi/6, edgecolor='black')
                        self.hex.append((i, j))
                        ax.add_patch(hexagon)
            count += 1
        plt.axis('off')
        fig.set_size_inches(self.width/100, self.height/100)

        plt.savefig('hexagonal_grid.png', bbox_inches='tight',
                    pad_inches=0, transparent=True)
        plt.close()
        plt.close()

        # Leer la imagen del tablero de hexágonos
        self.image = cv2.imread('hexagonal_grid.png')
        self.image = cv2.resize(self.image, (self.width, self.height))
        print(self.image.shape)

    def draw_square(self, position, size=50, color=(0, 0, 0)):
        # Dibujar un cuadrado en la imagen
        square = np.ones((size, size, 3), dtype=np.uint8) * \
            255  # Imagen en blanco sin canal alfa
        print(position)

        square[:, :] = color  # Color del cuadrado
        median = size//2
        # Colocar el cuadrado en la imagen
        self.image[position[1]-median:position[1]+median,
                   position[0]-median:position[0]+median, :] = square

    def draw_hexagon_object(self, position, size=50):
        # Dibujar un hexágono en la imagen sin fondo blanco
        # Imagen en blanco sin canal alfa
        hexagon_object = np.ones((size, size, 3), dtype=np.uint8) * 255
        print(position)

        fig, ax = plt.subplots(figsize=(size/100, size/100))
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')

        hexagon = patches.RegularPolygon(
            (size/2, size/2), numVertices=6, radius=size/2, orientation=np.pi/6, edgecolor='black')
        ax.add_patch(hexagon)

        plt.axis('off')
        plt.savefig('hexagon_object.png', bbox_inches='tight',
                    pad_inches=0, transparent=True)
        plt.close()

        # Leer la imagen del hexágono sin fondo blanco
        hexagon_object = cv2.imread('hexagon_object.png', cv2.IMREAD_UNCHANGED)

        # Colocar el hexágono en la imagen
        cx, cy = hexagon_object.shape[0]//2, hexagon_object.shape[1]//2
        self.image[position[1]-cx:position[1]+cx, position[0] -
                   cy:position[0]+cy, 2] = hexagon_object[:, :, 3]

    def remove_object(self, position, size=(0, 0)):
        # Restaurar el hexágono original en la posición
        hexagon_original = self.image_copy.copy()
        sx, sy = size[0]//2, size[1]//2
        self.image[position[1]-sx:position[1]+sx, position[0]-sy:position[0]+sy,
                   :] = hexagon_original[position[1]-sx:position[1]+sx, position[0]-sy:position[0]+sy, :]

    def show_image(self):
        plt.imshow(self.image)
        plt.title("Imagen con Objeto")
        plt.axis('off')
        plt.show()
