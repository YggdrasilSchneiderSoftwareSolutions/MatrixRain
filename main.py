import pygame, random, string, os
 
# Change this to toogle fullscreen
fullScreen = True
 
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
katakana = ""
for i in range(96):
    katakana += chr(int('0x30a0', 16) + i)
letters += katakana
 
class Streamer:
    def __init__(self) -> None:
        self.column = 0
        self.position = 0
        self.speed = 0
        self.text = ""
        self.streamerLength = 0
 
    def prepareStreamer(self) -> None:
        self.column = random.randint(0, SCREEN_WIDTH)
        self.position = 0
        self.speed = random.uniform(0.2, 0.5)
        #self.text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.streamerLength = random.randint(20, 80)
        self.text = ""
        for i in range(self.streamerLength):
            self.text += self.randomCharacter()
 
    def randomCharacter(self) -> str:
        return random.choice(letters)
 
# pygame setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
 
if fullScreen:
    desktopSize = pygame.display.get_desktop_sizes()
    SCREEN_WIDTH = desktopSize[0][0]
    SCREEN_HEIGHT = desktopSize[0][1]
    maxStreamers = 200
 
for i in range(maxStreamers):
    s = Streamer()
    s.prepareStreamer()
    listStreamers.append(s)
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('MatrixRain')
clock = pygame.time.Clock()
running = True
 
font = pygame.font.Font('freesansbold.ttf', TILE_SIZE)
fontKana = pygame.font.Font('NotoSansJP-Regular.ttf', TILE_SIZE)
 
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
            # if we get the kana and ascii from the same font-file, the app gets very slow. So we split those two
            if katakana.find(char) == -1:
                charRendered = font.render(char, True, color)
            else:
                charRendered = fontKana.render(char, True, color)
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
