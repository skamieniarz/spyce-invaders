''' Module containing Cannon class. '''

import random
from time import time

import pyxel

import consts


class Cannon:
    ''' Class containing methods and variables related to laser cannon and
        laser beams. '''
    def __init__(self):
        self.lives = 3
        self.x_cord = consts.CANNON_SCREEN_MARGIN
        self.y_cord = consts.SCREEN_SIZE['h'] - 20
        self.last_shot_attempt_time = 0
        self.shot_interval = 0.5
        self.beams = []

    @staticmethod
    def draw(cannon):
        ''' Draws a laser cannon from the image bank. '''
        pyxel.blt(cannon.x_cord, cannon.y_cord, 0,
                  consts.CANNON_ASSET[cannon.lives]['x'],
                  consts.CANNON_ASSET[cannon.lives]['y'],
                  consts.CANNON_ASSET['w'], consts.CANNON_ASSET['h'])

    def draw_beams(self):
        ''' Draws laser beams as pyxel lines. '''
        for laser_beam in self.beams:
            pyxel.line(laser_beam[0], laser_beam[1], laser_beam[0],
                       laser_beam[1] + 2, 8)

    def update_position(self):
        ''' Updates cannon's position according to pressed arrow key. '''
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT)
            ) and self.x_cord >= consts.CANNON_SCREEN_MARGIN:
            self.x_cord -= consts.CANNON_SPEED

        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT)
            ) and self.x_cord <= consts.SCREEN_SIZE['w'] - consts.CANNON_ASSET[
                'w'] - consts.CANNON_SCREEN_MARGIN:
            self.x_cord += consts.CANNON_SPEED

    def launch_beam(self):
        ''' When SPACE is pressed and time from last laser beam's launch is
            bigger than 0.5 second, launches beam. '''
        if ((pyxel.btn(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_SPACE)) and
                time() - self.last_shot_attempt_time >= self.shot_interval):
            self.last_shot_attempt_time = time()
            self.beams.append(
                [self.x_cord + consts.CANNON_ASSET['barrel'], self.y_cord])
            pyxel.play(1, 1)

    def update_beams(self):
        ''' Updates beams positions by BEAMS_SPEED value. '''
        for laser_beam in self.beams:
            laser_beam[1] -= consts.BEAMS_SPEED

    def pop_invisible_beams(self):
        ''' Pops invisible beams (which are already out of the screen) from the
            beams list. '''
        for beams_index, laser_beam in enumerate(self.beams):
            if laser_beam[1] < 0:
                self.beams.pop(beams_index)

    def beam_hit_event(self, invaders, ship, explosion, menus):
        ''' Performs beam hit event (pop the beam, set invader's active status
            to False or reset the ship, add explosion flash, update score)
            if any of cannon's beams hit any of the invaders or the ship. '''
        for beam_index, laser_beam in enumerate(self.beams):
            for invader_index, invader in enumerate(invaders):
                width_condition = (
                    invader[0] <= laser_beam[0] <=
                    (invader[0] + consts.INVADERS_ASSETS[invader[2]]['w']))
                height_condition = (invader[1] <= laser_beam[1] <=
                                    (invader[1] + consts.INVADERS_ASSETS['h']))
                if width_condition and height_condition and invader[3]:
                    self.beams.pop(beam_index)
                    invaders[invader_index][3] = False
                    pyxel.play(2, 0)
                    explosion.flashes.append({
                        'x': invader[0],
                        'y': invader[1],
                        'time': time()
                    })
                    menus.score += consts.POINTS_FOR_INVADER.get(invader[2])

            width_condition = (ship.x_cord <= laser_beam[0] <=
                               ship.x_cord + consts.SHIP_ASSET['w'])
            height_condition = (ship.y_cord <= laser_beam[1] <=
                                ship.y_cord + consts.SHIP_ASSET['h'])
            if width_condition and height_condition:
                pyxel.play(2, 0)
                explosion.flashes.append({
                    'x': ship.x_cord,
                    'y': ship.y_cord,
                    'time': time()
                })
                ship.reset()
                menus.score += random.choice(consts.POINTS_FOR_SHIP)
