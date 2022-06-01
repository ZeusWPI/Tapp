# Pygame template - skeleton for a new pygame project
import pygame
import random
import os
from queue import Queue

# set up asset folders
from pygame import transform

from server import create_server

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

WIDTH = 1400  # width of our game window
HEIGHT = 960  # height of our game window
FPS = 30  # frames per second

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

bufferSize = 1024

clients = {}


class Player(pygame.sprite.Sprite):
    # def __init__(self):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = pygame.Surface((50, 50))
    #     self.image.fill(GREEN)
    #     self.rect = self.image.get_rect()
    #     self.rect.center = (WIDTH / 2, HEIGHT / 2)
    def __init__(self, uid: int, color: pygame.Color):
        self.uid = uid

        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(
            os.path.join(img_folder, "betterracket.png")
        ).convert()

        self.image = player_img
        self.image.set_colorkey(BLACK)

        # resize the image
        self.image = transform.scale(self.image, (70, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4 * 1 if uid == 1 else WIDTH / 4 * 3, HEIGHT / 2)

        self.color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        self.color_image.fill(color)
        self.image.blit(self.color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def move(self, event):
        [x, y, z] = [a * 10 for a in event]
        self.rect.x += x
        self.rect.y += z


def main():
    socket = create_server()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tapp - Tennis App")
    clock = pygame.time.Clock()

    racket = pygame.image.load("img/racket.png")
    all_sprites = pygame.sprite.Group()

    color1 = pygame.Color(0)
    hue = 20
    color1.hsla = (hue, 100, 50, 100)
    player1 = Player(1, color1)
    p1_address = None

    hue = 250
    color2 = pygame.Color(0)
    color2.hsla = (hue, 100, 50, 100)
    player2 = Player(2, color2)
    p2_address = None

    all_sprites.add(player1)
    all_sprites.add(player2)

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        try:
            bytesAddressPair = socket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = "Message from Client:{}".format(message)
            data = message.decode("utf-8").split(";")
            [x, y, z] = [float(a) for a in data]
            if address in clients:
                clients[address]["event"] = [x, y, z]
            else:
                clients[address] = {"event": [0, 0, 0]}
                if p1_address is None:
                    print("Player 2 connected")
                    p2_address = address
                else:
                    print("Player 1 connected")
                    p1_address = address
        except:
            pass

        if p1_address is not None:
            player1.move(clients[p1_address]["event"])
        if p2_address is not None:
            player2.move(clients[p2_address]["event"])

        all_sprites.update()

        # Draw / render
        # screen.fill(pygame.color.Color(1, 1, 1))
        screen.fill((96, 96, 64))
        all_sprites.draw(screen)

        # *after* drawing everything, flip the display
        pygame.display.flip()

        # keep loop running at the right speed
        clock.tick(FPS)

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
