import pygame, os
from sys import exit
from random import randint, choice

HEIGHT, WIDTH = 800, 400
FPS = 60
VEL = 4


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(os.path.join('graphics', 'player_walk_1.png')).convert_alpha()
        player_walk_2 = pygame.image.load(os.path.join('graphics', 'player_walk_2.png')).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(os.path.join('graphics', 'jump.png')).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load(os.path.join('graphics', 'fly1.png')).convert_alpha()
            fly_2 = pygame.image.load(os.path.join('graphics', 'fly2.png')).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(os.path.join('graphics', 'snail1.png')).convert_alpha()
            snail_2 = pygame.image.load(os.path.join('graphics', 'snail2.png')).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    win.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
win = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Simple game')
clock = pygame.time.Clock()
text_font = pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50)
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

ground_surface = pygame.image.load(os.path.join('graphics', 'ground.png')).convert()
sky_surface = pygame.image.load(os.path.join('graphics', 'Sky.png')).convert()

# enter screen
player_stand = pygame.image.load(os.path.join('graphics', 'player_stand.png')).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1.3)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title_surface = text_font.render('WELCOME', False, (111, 196, 169))
title_rect = title_surface.get_rect(center=(400, 100))

game_message = text_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 300))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        win.blit(sky_surface, (0, 0))
        win.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(win)
        player.update()

        obstacle_group.draw(win)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        win.fill((94, 129, 162))
        win.blit(player_stand, player_stand_rect)

        score_message = text_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 300))

        if score == 0:
            win.blit(title_surface, title_rect)
            win.blit(game_message, game_message_rect)
        else:
            win.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)
