import pygame
from HomeAware import HomeAware
from loader import ImagesLoader

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("HomeAware - Détection des objets au sol")

home_aware = HomeAware()


def display_image_thumbnail_in_carousel(image, image_idx, total_images):
    """
        Affiche une seule image du carrousel (la miniature).

        Cette fonction prend une image (sous forme de tuple), son index dans le carrousel,
        et le nombre total d'images, puis affiche l'image sur l'écran avec des boutons de navigation
        et un bouton "Détecter".

        Args:
            image (tuple): Un tuple contenant le nom du fichier image, l'image originale,
                           la miniature, et le nom de la pièce.
            index_image (int): L'index de l'image actuelle dans le carrousel.
            nombre_total_images (int): Le nombre total d'images dans le carrousel.

        Returns:
            tuple: Un tuple contenant les rectangles de collision des boutons :
                   - bouton "Détecter"
                   - flèche gauche
                   - flèche droite
    """

    screen.fill((255, 255, 255))

    thumbnail = image[2]
    x = screen.get_width() // 2 - 150
    y = screen.get_height() // 2 - 150
    screen.blit(thumbnail, (x, y))

    detect_button_rect = pygame.Rect(x, y + 320, 330, 40)
    pygame.draw.rect(screen, (0, 128, 0), detect_button_rect)
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render('Détecter les objets au sol', True, (255, 255, 255))
    screen.blit(text_surface, (x + 10, y + 330))

    left_arrow_rect = pygame.Rect(50, screen.get_height() // 2 - 50, 50, 100)
    right_arrow_rect = pygame.Rect(screen.get_width() - 100, screen.get_height() // 2 - 50, 50, 100)

    pygame.draw.polygon(screen, (0, 0, 0), [(60, screen.get_height() // 2), (90, screen.get_height() // 2 - 30),
                                            (90, screen.get_height() // 2 + 30)])
    pygame.draw.polygon(screen, (0, 0, 0), [(screen.get_width() - 60, screen.get_height() // 2),
                                            (screen.get_width() - 90, screen.get_height() // 2 - 30),
                                            (screen.get_width() - 90, screen.get_height() // 2 + 30)])

    idx_text = f"{image_idx + 1} / {total_images}"
    idx_surface = font.render(idx_text, True, (0, 0, 0))
    screen.blit(idx_surface, (screen.get_width() // 2 - 30, 50))

    return detect_button_rect, left_arrow_rect, right_arrow_rect


def main():
    running = True
    clock = pygame.time.Clock()

    images = ImagesLoader.load_images_of_a_room("./Images/Chambre", 'bedroom') + ImagesLoader.load_images_of_a_room("./Images/Cuisine", 'kitchen') + ImagesLoader.load_images_of_a_room(
        "./Images/Salon", 'living_room')

    current_image_idx = 0

    while running:
        screen.fill((255, 255, 255))

        detect_button_rect, left_arrow_rect, right_arrow_rect = display_image_thumbnail_in_carousel(images[current_image_idx],
                                                                              current_image_idx, len(images))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if detect_button_rect.collidepoint(mouse_pos):
                    original_image = images[current_image_idx][
                        1]
                    room = images[current_image_idx][3]
                    print(
                        f"Detect clicked for image {images[current_image_idx][0]} in room {room}")
                    home_aware.display_results(original_image,
                                               room)

                if left_arrow_rect.collidepoint(mouse_pos):
                    current_image_idx = (current_image_idx - 1) % len(images)
                    print(f"Previous image, index: {current_image_idx}")

                # Right arrow clicked (next image)
                if right_arrow_rect.collidepoint(mouse_pos):
                    current_image_idx = (current_image_idx + 1) % len(images)
                    print(f"Next image, index: {current_image_idx}")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
