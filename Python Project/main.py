# install pygame in terminal: pip install pygame
import pygame
import time
import random

pygame.font.init()

# Set a width and height for the game window
WIDTH, HEIGHT = 1540, 780

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_VEL = 8

STAR_WIDTH = 20
STAR_HEIGHT = 40
STAR_VEL = 3

# Create the Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set a name for the window
pygame.display.set_caption("This is my pygame")

# Set a background image
background = pygame.transform.scale(pygame.image.load("background2.jpeg"), (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)
END_FONT = pygame.font.SysFont("arial", 150)


# making a draw function
def draw(player, elapsed_time, stars):
    # draws an image
    WIN.blit(background, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # draw Missiles
    for star in stars:
        pygame.draw.rect(WIN, "red", star)

    # Draw the player
    pygame.draw.rect(WIN, "light blue", player)
    pygame.display.update()


def main():
    run = True

    # make a player
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Create a clock to determine the FPS
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    # creating missiles
    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    # Main loop to continuously run the game
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            # Detect if the window is closed
            if event.type == pygame.QUIT:
                run = False
                break
        # Player Movement
        keys = pygame.key.get_pressed()

        # Finds left arrow key. Replace "LEFT" with any key and sets screen bounds
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = END_FONT.render("You Lost!", 1, "red")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(5000)
            break

        draw(player, elapsed_time, stars)
    pygame.quit()


if __name__ == "__main__":
    main()
