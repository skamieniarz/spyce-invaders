''' Module containing Invaders class. '''

import random
from time import time

import pyxel

import consts


class Invaders:
    ''' Class containing methods and variables related to invaders' wave and
        their projectiles. '''
    def __init__(self):
        self.units = []
        self.wave = 1
        self.step = 1
        self.units_direction_right = True
        self.populate_invaders(self.wave)
        self.approach_interval = 1.0
        self.last_approach_time = 0
        self.last_interval_shortening_time = 0
        self.projectiles = []
        self.projectile_launch_interval = 5
        self.last_shot_time = 0

    def draw_wave(self):
        ''' Draws all invaders in a loop according to invader type and current
            step. '''
        x_cord = 'x1' if self.step % 2 == 0 else 'x2'
        for invader in self.units:
            if invader[3]:
                pyxel.blt(invader[0], invader[1], 0,
                          consts.INVADERS_ASSETS[x_cord],
                          consts.INVADERS_ASSETS[invader[2]]['y'],
                          consts.INVADERS_ASSETS['w'],
                          consts.INVADERS_ASSETS['h'])

    def draw_projectiles(self):
        ''' Draws all projectiles that are in projectiles list. '''
        for projectile in self.projectiles:
            pyxel.pix(projectile[0], projectile[1], consts.WHITE)

    def populate_invaders(self, wave):
        ''' Populates units list with invaders lists with the following
            structure:
                invader[0] (int):  x coordinate,
                invader[1] (int):  y coordinate,
                invader[2] (int):  type,
                invader[3] (bool): state (alive or not)
        '''
        for rows_index in range(consts.INVADERS_ROWS):
            if rows_index in [0]:
                invader_type = 3
            elif rows_index in [1, 2]:
                invader_type = 2
            else:
                invader_type = 1
            for invaders_index in range(consts.INVADERS_AMOUNT_PER_ROW):
                self.units.append([
                    consts.FIRST_INVADER['x'] + (20 * invaders_index),
                    consts.FIRST_INVADER['y'] + (self.wave * 4) +
                    (15 * rows_index), invader_type, True
                ])

    def set_marching_sounds(self):
        ''' Sets marching sounds on different sound slots with a speed
            according to current approach interval value. '''
        pyxel.sound(2).set(
            note='F#1',
            tone='T',
            volume='1',
            effect='F',
            speed=consts.MARCHING_SOUND_SPEEDS[self.approach_interval])
        pyxel.sound(3).set(
            note='E1',
            tone='T',
            volume='1',
            effect='F',
            speed=consts.MARCHING_SOUND_SPEEDS[self.approach_interval])
        pyxel.sound(4).set(
            note='D1',
            tone='T',
            volume='1',
            effect='F',
            speed=consts.MARCHING_SOUND_SPEEDS[self.approach_interval])
        pyxel.sound(5).set(
            note='C1',
            tone='T',
            volume='1',
            effect='F',
            speed=consts.MARCHING_SOUND_SPEEDS[self.approach_interval])

    def update_invaders_step(self):
        ''' Updates current value of invaders step. It is counted to 4 because
            of 4 different marching sounds. '''
        if self.step == 4:
            self.step = 1
        else:
            self.step += 1

    def units_march(self):
        ''' Performs invaders' units marching movement by updating every
            invader's position every approach interval according to current
            wave direction. When at least one of the invaders reaches the
            edge of the screen, the wave performs close-up movement. Marching
            sound is played with each step. '''
        if (self.units and
                time() - self.last_approach_time >= self.approach_interval):
            self.set_marching_sounds()
            if self.units_direction_right:
                for invader in self.units:
                    invader[0] += consts.INVADERS_MARCHING_SPEED
                    pyxel.play(3, self.step + 1)
            else:
                for invader in self.units:
                    invader[0] -= consts.INVADERS_MARCHING_SPEED
                    pyxel.play(3, self.step + 1)

            invaders_x_cords = [
                invader[0] for invader in self.units if invader[3]
            ]
            if invaders_x_cords:
                if (max(invaders_x_cords) >=
                        consts.SCREEN_SIZE['w'] - consts.INVADERS_ASSETS['w'] -
                        consts.INVADERS_SCREEN_MARGIN):
                    self.units_direction_right = False
                    for invader in self.units:
                        invader[1] += consts.INVADERS_MARCHING_SPEED
                        pyxel.play(3, self.step + 1)

                if min(invaders_x_cords) <= consts.INVADERS_SCREEN_MARGIN:
                    self.units_direction_right = True
                    for invader in self.units:
                        invader[1] += consts.INVADERS_MARCHING_SPEED
                        pyxel.play(3, self.step + 1)

            self.update_invaders_step()
            self.last_approach_time = time()

    def launch_projectile(self):
        ''' Launches projectile by randomly chosen invader if time from last
            projectile's launch is bigger than randomly chosen value between
            1 second and projectile launch interval. '''
        random_start = 1 if self.wave <= 9 else 0
        if time() - self.last_shot_time >= random.randint(
                random_start, self.projectile_launch_interval):
            shootable_invaders = []
            for invader in self.units:
                if invader[3]:
                    shootable_invaders.append(invader)
            if shootable_invaders:
                random_invader = random.choice(shootable_invaders)
                self.last_shot_time = time()
                self.projectiles.append([
                    random_invader[0] + round(consts.INVADERS_ASSETS['w'] / 2),
                    random_invader[1] + consts.INVADERS_ASSETS['h']
                ])

    def update_projectiles(self):
        ''' Updates every projectile position by invaders projectiles
            speed. '''
        for projectile in self.projectiles:
            projectile[1] += consts.INVADERS_PROJECTILES_SPEED

    def pop_invisible_projectiles(self):
        ''' If any projectile reaches the edge of the screen, pops it from
            projectiles list. '''
        for index, projectile in enumerate(self.projectiles):
            if projectile[1] > consts.SCREEN_SIZE['h']:
                self.projectiles.pop(index)

    def projectile_hit_event(self, cannon, invaders, explosion):
        ''' Performs projectile hit event (pop projectile, add explosion flash,
            increase cannon shot interval, subtract one life, play explosions
            sound) if any of invaders' projectile hit the laser cannon. '''
        for projectile_index, projectile in enumerate(self.projectiles):
            if (cannon.x_cord <= projectile[0] <=
                (cannon.x_cord + consts.CANNON_ASSET['w'])
                    and cannon.y_cord <= projectile[1] <=
                (cannon.y_cord + consts.CANNON_ASSET['h'])):
                invaders.projectiles.pop(projectile_index)
                pyxel.play(2, 0)
                explosion.flashes.append({
                    'x': cannon.x_cord,
                    'y': cannon.y_cord - consts.SMALL_MARGIN,
                    'time': time()
                })
                if cannon.lives >= 1:
                    cannon.lives -= 1
                    cannon.shot_interval += 0.1

    def check_arrival(self, cannon, game):
        ''' Checks if any of the invaders reached the cannon. '''
        invaders_arrived = [
            invader[1] + consts.INVADERS_ASSETS['h'] >= cannon.y_cord
            for invader in self.units if invader[3]
        ]
        if any(invaders_arrived):
            game.state = 'end'

    def shorten_approach_time_interval(self):
        ''' Shorten approach interval if shortening interval is up. '''
        if self.approach_interval > 0 and time() - \
                self.last_interval_shortening_time > \
                    consts.APPROACH_SHORTENING_INTERVAL:
            self.approach_interval = round(
                self.approach_interval - consts.APPROACH_SHORTENING_VALUE, 1)
            self.last_interval_shortening_time = time()

    def next_wave(self):
        ''' Generates next wave of invaders if all invaders from previous wave
            were destroyed. Sligthly shortens the projectile launch interval
            maximum value (by a second). '''
        if all(not invader[3] for invader in self.units):
            self.units = []
            self.wave += 1
            self.populate_invaders(self.wave)
            self.approach_interval = round(1.0 - (self.wave * 0.1), 1)
            self.units_direction_right = True
            self.last_interval_shortening_time = time()
            self.last_shot_time = time()
            if self.projectile_launch_interval > 2:
                self.projectile_launch_interval -= 1
