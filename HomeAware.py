import cv2
import numpy as np

def display_image(img, window_name, max_width=1200, max_height=800):
    height, width = img.shape[:2]

    aspect_ratio = width / height

    if width > max_width or height > max_height:
        # Resize the image while maintaining the aspect ratio
        if width > height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        img = cv2.resize(img, (new_width, new_height))

    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class HomeAware:
    def __init__(self):
        self.__reference_images = dict()
        self.__reference_images['bedroom'] = cv2.imread("./Images/Chambre/Reference.JPG")
        self.__reference_images['kitchen'] = cv2.imread("./Images/Cuisine/Reference.JPG")
        self.__reference_images['living_room'] = cv2.imread("./Images/Salon/Reference.JPG")

        self.__masks = dict()
        self.__masks['bedroom'] = cv2.imread("./Images/Chambre/bedroom_mask.jpg", cv2.IMREAD_GRAYSCALE)
        self.__masks['kitchen'] = cv2.imread("./Images/Cuisine/kitchen_mask.jpg", cv2.IMREAD_GRAYSCALE)
        self.__masks['living_room'] = cv2.imread("./Images/Salon/living_room_mask.jpg", cv2.IMREAD_GRAYSCALE)

    def apply_clahe(self, image):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        clahe_image = clahe.apply(image)
        return clahe_image

    def adjust_brightness_to_reference(self, image, reference_image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

        mean_image = np.mean(gray_image)
        mean_reference = np.mean(gray_reference)

        adjustment_factor = mean_reference / mean_image
        adjusted_image = cv2.convertScaleAbs(image, alpha=adjustment_factor, beta=0)

        return adjusted_image

    def histogram_matching(self, image, template):
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        source_hist, bins = np.histogram(image.flatten(), 256, [0, 256])
        template_hist, bins = np.histogram(template.flatten(), 256, [0, 256])

        # Calcule la fonction de répartition cumulée (CDF) pour chaque image
        cdf_source = source_hist.cumsum()
        cdf_template = template_hist.cumsum()

        # Normalisation de la CDF
        cdf_source_normalized = cdf_source / cdf_source.max()
        cdf_template_normalized = cdf_template / cdf_template.max()

        # Mapping de chaque pixel dans l'image source
        lookup_table = np.zeros(256)
        g_j = 0
        for i in range(256):
            while cdf_template_normalized[g_j] < cdf_source_normalized[i] and g_j < 255:
                g_j += 1
            lookup_table[i] = g_j

        matched_image = cv2.LUT(image, lookup_table.astype(np.uint8))
        return matched_image

    def preprocess(self, image, room):
        adjusted_image = self.adjust_brightness_to_reference(image, self.__reference_images[room])

        gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
        display_image(gray_image, "Image after brightness adjustment")

        clahe_image = self.apply_clahe(gray_image)
        display_image(clahe_image, "Image after preprocess")

        hist_matched_image = self.histogram_matching(clahe_image,  self.__reference_images[room])
        display_image(hist_matched_image, "Image after preprocess")

        return hist_matched_image

    def compute_difference(self, image, room):
        reference_image = self.preprocess(self.__reference_images[room], room)
        current_image = self.preprocess(image, room)

        difference = cv2.absdiff(reference_image, current_image)

        masked_difference = cv2.bitwise_and(difference, difference, mask=self.__masks[room])

        return masked_difference

    @staticmethod
    def compute_threshold(difference):
        _, tresh = cv2.threshold(
            difference,
            0,
            255,
            cv2.THRESH_OTSU
        )
        display_image(tresh, "Treshold")

        return tresh

    def detect_changes(self, image, room):
        difference = self.compute_difference(image, room)

        threshold_image = self.compute_threshold(difference)

        kernel = np.ones((5, 5), np.uint8)
        opened_image = cv2.morphologyEx(threshold_image, cv2.MORPH_CLOSE, kernel)
        display_image(opened_image, "Morphological")
        return opened_image

    def display_results(self, image, room):
        changes = self.detect_changes(image, room)

        contours, hierarchy = cv2.findContours(changes, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        output_image = image.copy()

        for i, contour in enumerate(contours):
            # Vérifier que le contour n'a pas de parent (hiérarchie[0][i][3] == -1 signifie pas de parent)
            if hierarchy[0][i][3] == -1:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 100 and h > 100:  # Ignorer les petits contours
                    cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 0, 255), 10)
                    cv2.putText(output_image, "Obstacle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                                4)

        display_image(output_image, "Obstacles")