import os
import cv2
import pygame


class ImagesLoader:
    @staticmethod
    def load_images_of_a_room(folder_path, room_name):
        """
            Charger les images d'un dossie spcifié, les redimensionne en miniaturs et les convertit en surfases Pygame pour une utilisation graphique.
            Args:
                folder_path (str): Le chemin du dossier contenant les images a charge.
                room_name (str): Le nom de la pièc auquel les images appartiennent ("bedroom", "kitchen", "living_room"
            Returns:
                list: Une liste de tupels où chaque tupel contient :
                    - image_file (str): Le nom du fichier image.
                    - img (numpy.ndarray): L'image originale charge sous forme de tableau NumPy.
                    - thumbnail_surface (pygame.Surface): La miniature de l'image sous forme de surfase Pygame.
                    - room_name (str): Le nom de la piece associe a l'image.
        """

        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.JPG'))]
        images = []
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)

            img = cv2.imread(image_path)
            if img is None:
                print(f"Nous n'avons pas pu charger l imag suivante: {image_path}")
                continue

            print(f"L image suivante a ete chargee: {image_path}")

            thumbnail = cv2.resize(img, (300, 300))
            thumbnail = cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB)
            thumbnail_surface = pygame.surfarray.make_surface(thumbnail.swapaxes(0, 1))  # Convert to pygame surface

            images.append((image_file, img, thumbnail_surface, room_name))
        return images


