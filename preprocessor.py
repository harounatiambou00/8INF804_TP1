import cv2


class ImagesPreprocessor:
    def __init__(self, images):
        self.__images = images

    def convert_to_grayscale(self):
        if self.__images["bedroom_images_reference"] is not None:
            self.__images["bedroom_images_reference"] = cv2.cvtColor(self.__images["bedroom_images_reference"],
                                                                     cv2.COLOR_BGR2GRAY)
        if self.__images["kitchen_images_reference"] is not None:
            self.__images["kitchen_images_reference"] = cv2.cvtColor(self.__images["kitchen_images_reference"],
                                                                     cv2.COLOR_BGR2GRAY)
        if self.__images["living_room_images_reference"] is not None:
            self.__images["living_room_images_reference"] = cv2.cvtColor(
                self.__images["living_room_images_reference"], cv2.COLOR_BGR2GRAY)

        for i in range(len(self.__images["bedroom_images"])):
            if self.__images["bedroom_images"][i] is not None:
                self.__images["bedroom_images"][i] = cv2.cvtColor(self.__images["bedroom_images"][i],
                                                                  cv2.COLOR_BGR2GRAY)

        for i in range(len(self.__images["kitchen_images"])):
            if self.__images["kitchen_images"][i] is not None:
                self.__images["kitchen_images"][i] = cv2.cvtColor(self.__images["kitchen_images"][i],
                                                                  cv2.COLOR_BGR2GRAY)

        for i in range(len(self.__images["living_room_images"])):
            if self.__images["living_room_images"][i] is not None:
                self.__images["living_room_images"][i] = cv2.cvtColor(self.__images["living_room_images"][i],
                                                                      cv2.COLOR_BGR2GRAY)

    def adjust_brightness(image, reference_image):
        # Convertir les images en niveaux de gris
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

        # Calculer la luminosité moyenne des deux images
        mean_image = np.mean(gray_image)
        mean_reference = np.mean(gray_reference)

        # Calculer le facteur d'ajustement
        adjustment_factor = mean_reference / mean_image

        # Appliquer le facteur d'ajustement à l'image
        adjusted_image = cv2.convertScaleAbs(image, alpha=adjustment_factor, beta=0)

        return adjusted_image

    def equalize_histograms(self):
        if self.__images["bedroom_images_reference"] is not None:
            self.__images["bedroom_images_reference"] = cv2.equalizeHist(self.__images["bedroom_images_reference"])

        if self.__images["kitchen_images_reference"] is not None:
            self.__images["kitchen_images_reference"] = cv2.equalizeHist(self.__images["kitchen_images_reference"])

        if self.__images["living_room_images_reference"] is not None:
            self.__images["living_room_images_reference"] = cv2.equalizeHist(self.__images["living_room_images_reference"])

        for i in range(len(self.__images["bedroom_images"])):
            if self.__images["bedroom_images"][i] is not None:
                self.__images["bedroom_images"][i] = cv2.equalizeHist(self.__images["bedroom_images"][i])

        for i in range(len(self.__images["kitchen_images"])):
            if self.__images["kitchen_images"][i] is not None:
                self.__images["kitchen_images"][i] = cv2.equalizeHist(self.__images["kitchen_images"][i])

        for i in range(len(self.__images["living_room_images"])):
            if self.__images["living_room_images"][i] is not None:
                self.__images["living_room_images"][i] = cv2.equalizeHist(self.__images["living_room_images"][i])

    def preprocess(self):
        self.convert_to_grayscale()
        #self.equalize_histograms()
        return self.__images
