# tempat character dan semua sprite untuk JUMPS!
import pygame as pg
from constants import *
from random import choice, randrange
vct = pg.math.Vector2

## Class untuk mengambil spritesheet #####
class SpriteSheet(pg.sprite.Sprite):
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # fungsi untuk mengambil image dari spritesheet

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x , y, width, height))
        image = pg.transform.scale(image, (int(width * 0.75), int(height * 0.75)))
        return image

    def get_image_half(self, x, y, width, height):
        # mengambil image dari spritesheet dengan setengah scaling

        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x , y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

## Class player untuk pemain #############
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LYR
        self.groups = game.allSprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.boost_pwr = False
        self.current_fr = 0
        self.last_upd = 0
        self.load_img()
        self.image = self.standing_frame[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vct(40, HEIGHT - 100)
        self.vel = vct(0, 0)
        self.acc = vct(0, 0)

    def load_img(self):
        # image dari player

        self.standing_frame = [self.game.spritesheet_player1.get_image(0, 190, 66, 92),
                                self.game.spritesheet_player1.get_image(67, 190, 66, 92)]
        for fr in self.standing_frame:
            fr.set_colorkey(BLACK)
        
        self.walking_r = [self.game.spritesheet_player1.get_image(142, 0, 70, 94),
                            self.game.spritesheet_player1.get_image(0, 95, 70, 94),
                            self.game.spritesheet_player1.get_image(71, 95, 70, 94),
                            self.game.spritesheet_player1.get_image(142, 95, 70, 94),
                            self.game.spritesheet_player1.get_image(213, 0, 70, 94),
                            self.game.spritesheet_player1.get_image(284, 0, 70, 94)]
        
        self.walking_l = []
        for fr in self.walking_r:
            fr.set_colorkey(BLACK)
            self.walking_l.append(pg.transform.flip(fr, True, False))

        self.jumping_frame_r = self.game.spritesheet_player1.get_image(423, 95, 66, 94)
        self.jumping_frame_r.set_colorkey(BLACK)    
        self.jumping_frame_l = pg.transform.flip(self.jumping_frame_r, True, False)
        self.jumping_frame_l.set_colorkey(BLACK)    
    
    def jump(self):
        # fungsi untuk melompat

        self.rect.x += 2
        hit = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hit and not self.jumping:
            self.game.jump_snd.play()
            self.jumping = True
            self.vel.y = -PLAYER_JMP

    def jump_stop(self):
        # fungsi untuk menstop lompatan

        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        # fungsi update dari player

        self.animasi()
        self.acc = vct(0, PLAYER_GRV)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if key[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # menambah friksi ke player
        self.acc.x += self.vel.x * PLAYER_FRC

        # equasi motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # agar ga keluar frame screen dari game
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos


    def animasi(self):
        # fungsi untuk membuat animasi dari player

        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # animasi pas jalan
        if self.walking:
            if now - self.last_upd > 100:
                self.last_upd = now
                self.current_fr = (self.current_fr + 1) % len(self.walking_l)
                bot = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_r[self.current_fr]
                else:
                    self.image = self.walking_l[self.current_fr]
                self.rect = self.image.get_rect()
                self.rect.bottom = bot
                

        # animasi pas idle(diam)
        if not self.jumping and not self.walking:
            if now - self.last_upd > 345:
                self.last_upd = now
                self.current_fr = (self.current_fr + 1) % len(self.standing_frame)
                bot = self.rect.bottom
                self.image = self.standing_frame[self.current_fr]
                self.rect = self.image.get_rect()
                self.rect.bottom = bot

        # animasi pas lompat
        if self.jumping or self.boost_pwr:
            if now - self.last_upd > 50:
                self.last_upd = now
                bot = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.jumping_frame_r
                else:
                    self.image = self.jumping_frame_l

                self.rect = self.image.get_rect()
                self.rect.bottom = bot

        # membuat mask untuk collision
        self.mask = pg.mask.from_surface(self.image)

## class untuk platform di game ##########
class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y,):
        self._layer = PLAT_LYR
        self.groups = game.platforms, game.allSprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_objects.get_image_half(0, 288, 380, 94),
                    self.game.spritesheet_objects.get_image_half(213, 1662, 201, 100),
                    self.game.spritesheet_objects.get_image_half(0, 384, 380, 94),
                    self.game.spritesheet_objects.get_image_half(382, 204, 200, 100)]
        images_2 = [self.game.spritesheet_objects.get_image_half(0, 960, 380, 94),
                    self.game.spritesheet_objects.get_image_half(0, 864, 380, 94),
                    self.game.spritesheet_objects.get_image_half(218, 1558, 200, 100),
                    self.game.spritesheet_objects.get_image_half(382, 0, 200, 100)]
        if randrange(100) < PLATFORM_SPWN:
            self.image = choice(images_2)
        else:
            self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # untuk men-spawn powerup
        if randrange(100) < PWR_SPAWN:
            Pwup(self.game, self)

## Class untuk powerup di game ###########
class Pwup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = PWUP_LYR
        self.groups = game.powerup, game.allSprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet_objects.get_image_half(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        # fungsi update untuk powerup

        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


## Class untuk Enemy di game #############
class Enemy(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = ENEMIES_LYR        
        self.groups = game.allSprite, game.Enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up_l = self.game.spritesheet_enemies.get_image(0, 32, 72, 36)
        self.image_up_l.set_colorkey(BLACK)
        self.image_down_l = self.game.spritesheet_enemies.get_image(0, 0, 75, 31)
        self.image_down_l.set_colorkey(BLACK)
        self.image_up_r = pg.transform.flip(self.image_up_l, True, False)
        self.image_up_r.set_colorkey(BLACK)        
        self.image_down_r = pg.transform.flip(self.image_down_l, True, False)
        self.image_down_r.set_colorkey(BLACK)


        self.image = self.image_up_l
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        # fungsi update buat enemy

        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.vx < 0:
            if self.dy < 0:
                self.image = self.image_up_l
            else:
                self.image = self.image_down_l
        else:
            if self.dy < 0:
                self.image = self.image_up_r
            else:
                self.image = self.image_down_r
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy

        # untuk menghapus enemy jika melewati screen
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

## Class untuk awan di game background ###
class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LYR
        self.groups = game.allSprite, game.bg
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_img)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height  * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -30)

    def update(self):
        # fungsi update dari awan di game

        # untuk menghapus awan jika melewati batas screen tertentu
        if self.rect.top > HEIGHT * 2:
            self.kill()