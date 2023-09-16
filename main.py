import pygame, random, string
 
TILE_SIZE = 12
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1250
 
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
maxStreamers = 100
listStreamers = []
letters = string.ascii_uppercase + string.digits + string.punctuation
 
class Streamer:
    def __init__(self) -> None:
        self.column = 0
        self.position = 0
        self.speed = 0
        self.text = ""
        self.streamerLength = 0
 
    def prepareStreamer(self):
        self.column = random.randint(0, SCREEN_WIDTH)
        self.position = 0
        self.speed = random.uniform(0.2, 0.5)
        #self.text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.streamerLength = random.randint(20, 80)
        self.text = ""
        for i in range(self.streamerLength):
            self.text += self.randomCharacter()
 
    def randomCharacter(self):
        return random.choice(letters)
 
for i in range(maxStreamers):
    s = Streamer()
    s.prepareStreamer()
    listStreamers.append(s)
 
# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MatrixRain')
clock = pygame.time.Clock()
running = True
 
font = pygame.font.Font('freesansbold.ttf', TILE_SIZE)
 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)
 
    for streamer in listStreamers:
        streamer.position += streamer.speed
        for i in range(len(streamer.text)):
            color = GREEN
            if streamer.speed <= 0.4:
                color = DARK_GREEN
            if i == 0:
                color = WHITE
            elif i <= 3:
                color = GRAY
 
            charIndex = abs((i - int(streamer.position)) % len(streamer.text))
            char = streamer.text[charIndex]
            charRendered = font.render(char, True, color)
            screen.blit(charRendered, (streamer.column, int(streamer.position - i) * TILE_SIZE))
 
            # occasionally glitch a character
            if random.randint(0, 1000) == 42:
                streamer.text = streamer.text[:i] + streamer.randomCharacter() + streamer.text[i + 1:]
 
        if (streamer.position - len(streamer.text)) * TILE_SIZE >= SCREEN_HEIGHT:
            streamer.prepareStreamer()
 
    # flip() the display to put your work on screen
    pygame.display.flip()
 
    clock.tick(60)  # limits FPS to 60
 
pygame.quit()