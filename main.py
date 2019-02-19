# JUMPS! by mushaffa huda - platform game
# Art by Kenney.nl
# Happy by https://opengameart.org/users/rezoner
# Happy Adventure by https://opengameart.org/users/TinyWorlds

import pygame as pg
import random
from constants import *
from sprites import *
from os import path

##### ENDLESS PLATFROM GAME #######

class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.gamerun = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load()

    def load(self):
        # load data from the system to the game

        # load highscore
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HIGHSCORE), 'w') as r:
            try:
                self.highscore = int(r.read())
            except: 
                self.highscore = 0

        # load sprite image
        self.spritesheet_player1 = SpriteSheet(path.join(img_dir, SPRITESHEET[0]))
        self.spritesheet_objects = SpriteSheet(path.join(img_dir, SPRITESHEET[1]))
        self.spritesheet_enemies = SpriteSheet(path.join(img_dir, SPRITESHEET[2]))

        # load sound files
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Jump5.wav'))
        self.boost_pwup_snd = pg.mixer.Sound(path.join(self.snd_dir, 'boost.wav'))
        self.fall_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt3.wav'))
        self.hit_snd = pg.mixer.Sound(path.join(self.snd_dir, 'Hit_Hurt.wav'))

        # load clouds
        self.cloud_img = []
        for i in range(1, 4):
            self.cloud_img.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())

    def new_game(self):
        # initiate new game

        self.points = 0
        self.allSprite = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerup = pg.sprite.Group()
        self.Enemy = pg.sprite.Group()
        self.bg = pg.sprite.Group()
        self.player = Player(self)
        self.enemy_timer = 0
        for pl in PLATFORM_LST:
            Platform(self, *pl)
        pg.mixer.music.load(path.join(self.snd_dir, 'happy.ogg'))
        for i in range(7):
            c = Cloud(self)
            c.rect.y += 450
        self.run_game()

    def run_game(self):
        # ngeloop gamenya

        pg.mixer.music.play(loops = -1)
        self.play = True
        while self.play:
            self.clock.tick(FPS)
            self.update()
            self.events()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        # update part dari gamenya

        self.allSprite.update()

        # player stand on platform only if falling
        if self.player.vel.y > 0:
            hit = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hit:
                lowest = hit[0]
                for i in hit:
                    if i.rect.bottom > lowest.rect.bottom:
                        lowest = i
                if lowest.rect.left - 10 < self.player.pos.x < lowest.rect.right + 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = hit[0].rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False
                        self.player.boost_pwr = False
        
        # player reach 1/4 top of screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 10:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for c in self.bg:
                c_velo = random.randrange(2, 5)
                c.rect.y += max(abs(self.player.vel.y / c_velo), 2)
            for e in self.Enemy:
                e.rect.y += max(abs(self.player.vel.y), 2)
            for p in self.platforms:
                p.rect.y += max(abs(self.player.vel.y), 2)
                if p.rect.top >= HEIGHT:
                    p.kill()
                    self.points += 10

        # spawning new platforms
        while len(self.platforms) < 6:
            width = random.randrange(45, 150)
            Platform(self, random.randrange(0, WIDTH - width),
                        random.randrange(-50, -30),
                    )

        # spawn enemy
        now = pg.time.get_ticks()
        if now - self.enemy_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.enemy_timer = now
            Enemy(self)

        # player hit powerup
        Pwup_hit = pg.sprite.spritecollide(self.player, self.powerup, True)
        for p in Pwup_hit:
            if p.type == 'boost':
                self.boost_pwup_snd.play()
                self.player.vel.y = -BOOST_PWR
                self.player.jumping = False
                self.player.boost_pwr = True

        # player hit enemy
        enem_hit = pg.sprite.spritecollide(self.player, self.Enemy, False, pg.sprite.collide_mask)
        if enem_hit:
            self.hit_snd.play()
            self.play = False

        # GAMEOVER!
        if self.player.rect.bottom > HEIGHT:
            for i in self.allSprite:
                i.rect.y -= max(self.player.vel.y, 10)
                if i.rect.bottom < 0:
                    i.kill()
            if len(self.platforms) == 0:
                self.fall_snd.play()
                self.play = False

    def events(self):
        # game events - player input

        for e in pg.event.get():
            # check for closing window using GUI
            if e.type == pg.QUIT:
                if self.play:
                    self.play = False
                self.gamerun = False
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE or e.key == pg.K_UP:
                    self.player.jump()
            if e.type == pg.KEYUP:
                if e.key == pg.K_SPACE or e.key == pg.K_UP:
                    self.player.jump_stop()
    def draw(self):
        # drawing the game in the screen

        self.screen.fill(BG)
        self.allSprite.draw(self.screen)
        self.drawtext(str(self.points), 22, WHITE, WIDTH / 2, 15)
        # do this last
        pg.display.flip()

    def start_screen(self):
        # start menu screen

        pg.mixer.music.load(path.join(self.snd_dir, 'happy_adventure.ogg'))
        pg.mixer.music.play(loops = -1)
        self.screen.fill(BG)
        self.drawtext(TITLE, 56, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawtext('Use Arrow key to move and spacebar to jump', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawtext('Press any key to play', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.drawtext('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        self.drawtext('credits: ', 15, WHITE, 25, HEIGHT - 60)
        self.drawtext('-Art by Kenney.nl', 15, WHITE, 50, HEIGHT - 40)
        self.drawtext('-Music by rezoner and TinyWorlds', 15, WHITE, 99, HEIGHT - 20)
        self.drawtext('-by Mushaffa Huda', 15, WHITE, WIDTH / 2, 210)
        pg.display.flip()
        self.waitKey_event()
        pg.mixer.music.fadeout(500)

    def go_screen(self):
        # game over screen

        if self.gamerun:
            pg.mixer.music.load(path.join(self.snd_dir, 'happy_adventure.ogg'))
            pg.mixer.music.play(loops = -1)
            self.screen.fill(BG)
            self.drawtext('GAME OVER CUY!', 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.drawtext('Score : ' + str(self.points), 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.drawtext('Press any key to play again', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            if self.points > self.highscore:
                self.highscore = self.points
                self.drawtext('NEW HIGHSCORE MANTAP!', 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40) 
                with open(path.join(self.dir, HIGHSCORE), 'w') as r:
                    r.write(str(self.points))
            else:
                self.drawtext('High Score: ' + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            pg.display.flip()
            self.waitKey_event()
            pg.mixer.music.fadeout(500)
        return

    def waitKey_event(self):
        # menunggu pemain untuk memencet key di start atau gameover screen

        wait = True
        while wait:
            self.clock.tick(FPS)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    wait = False
                    self.gamerun = False
                if e.type == pg.KEYUP:
                    wait = False
                    
    def drawtext(self, text, size, color, x, y):
        # fungsi untuk menggambar text ke screen

        font = pg.font.Font(self.font_name, size)
        text_srf = font.render(text, True, color)
        text_rect = text_srf.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_srf, text_rect)

game = Game()
game.start_screen()

# the game loop to run the game
while game.gamerun:
    game.new_game()
    game.go_screen()

pg.quit()   # quitting the game :)