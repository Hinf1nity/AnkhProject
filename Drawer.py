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
        self.hex_size = hex_size
        self.hex = []
        self.draw_hexagonal_grid()

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

    def draw_square(self, hex_num, size=50, color=(0, 0, 0)):
        # Dibujar un cuadrado en la imagen
        square = np.ones((size, size, 3), dtype=np.uint8) * \
            255  # Imagen en blanco sin canal alfa
        position = self.hex[hex_num]
        print(self.hex)
        print(position)

        square[:, :] = color  # Color del cuadrado

        # Colocar el cuadrado en la imagen
        self.image[position[1]:position[1]+size,
                   position[0]-size:position[0], :] = square

    def draw_hexagon_object(self, hex_num, size=50):
        # Dibujar un hexágono en la imagen sin fondo blanco
        # Imagen en blanco sin canal alfa
        hexagon_object = np.ones((size, size, 3), dtype=np.uint8) * 255
        position = self.hex[hex_num]
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
        self.image[position[1]:position[1]+hexagon_object.shape[0], position[0] -
                   hexagon_object.shape[1]:position[0], 2] = hexagon_object[:, :, 3]

    def remove_object(self, hex_num, size=(0, 0)):
        # Restaurar el hexágono original en la posición
        hexagon_original = cv2.imread('hexagonal_grid.png')
        hexagon_original = cv2.resize(
            hexagon_original, (self.width, self.height))
        position = self.hex[hex_num]
        self.image[position[1]:position[1]+size[0], position[0]-size[1]:position[0],
                   :] = hexagon_original[position[1]:position[1]+size[0], position[0]-size[1]:position[0], :]

    def show_image(self):
        plt.imshow(self.image)
        plt.title("Imagen con Objeto")
        plt.axis('off')
        plt.show()
