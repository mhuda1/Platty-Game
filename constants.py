# game option/settings and stuff
TITLE = 'Jumps!'
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HIGHSCORE = 'Hs.txt'
SPRITESHEET = ['p2_spritesheet.png',
                'spritesheet_jumper.png',
                'enemies_spritesheet.png']

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRC = -0.12
PLAYER_GRV = 0.8
PLAYER_JMP = 20


# platform
PLATFORM_LST = [
        (0, HEIGHT - 60),
        (WIDTH / 2 - 50, HEIGHT * 3/4),
        (125, HEIGHT - 350),
        (350, 200),
        (175, 100)
    ]

# game properties
BOOST_PWR = 60
PWR_SPAWN = 5
PLATFORM_SPWN = 20
ENEMY_SPWN = 5000
PLAYER_LYR = 2
PWUP_LYR = 1
PLAT_LYR = 1
ENEMIES_LYR = 2
CLOUD_LYR = 0


# define colors
BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
SKYBLUE = (135, 206, 250)
DEEPSKYBLUE = (0, 19, 255)
DEEPSKYBLUE1 = (0, 75, 100)
ANOTHERBLUE = (173, 216, 230)

BG = DEEPSKYBLUE1