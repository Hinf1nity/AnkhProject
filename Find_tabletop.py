import cv2
import numpy as np
import matplotlib.pyplot as plt


class HexagonDetector:
    def __init__(self):
        self.center = []
        self.i = 0

    def find_hexagons(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        original_image = image.copy()
        image = cv2.resize(image, (640, 640))
        original_image = cv2.resize(original_image, (640, 640))

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise and help contour detection
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 31)

        structuring_element = np.ones((1, 1), np.uint8)
        closing = cv2.morphologyEx(
            thresh, cv2.MORPH_CLOSE, structuring_element, iterations=1)
        opening = cv2.morphologyEx(
            closing, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=3)
        closing1 = cv2.morphologyEx(
            opening, cv2.MORPH_CLOSE, structuring_element, iterations=3)

        # Find contours in the edged image
        contours, _ = cv2.findContours(
            closing1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        for contour in contours:
            # Approximate the contour to a polygon
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # If the polygon has 6 vertices, it might be a hexagon
            if len(approx) == 6:
                # Draw the contour
                cv2.drawContours(image, [approx], 0, (0, 255, 0), 3)

                # Calculate the center of the hexagon
                M = cv2.moments(approx)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    self.center.append((cx, cy))
                    self.i += 1

        # Display the result using Matplotlib
        print(
            f"La cantidad de hexágonos detectados en la imagen son: {self.i}")
        plt.figure(figsize=(20, 5))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("Hexágonos detectados")

        return self.center
