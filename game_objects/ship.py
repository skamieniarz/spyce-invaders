''' Module containing Ship class. '''

import random
from time import time

import pyxel

import consts


class Ship:
    ''' Class containing methods and variables related to mystery ship. '''
    def __init__(self):
        self.x_cord = -(consts.SHIP_ASSET['w'])
        self.y_cord = 18
        self.last_occurrence_time = time()
        self.ship_appearance_interval = random.randint(25, 45)

    def draw(self):
        ''' Draws ship. '''
        pyxel.blt(self.x_cord, self.y_cord, 0, consts.SHIP_ASSET['x'],
                  consts.SHIP_ASSET['y'], consts.SHIP_ASSET['w'],
                  consts.SHIP_ASSET['h'])

    def reset(self):
        ''' Resets ship object's attributes. '''
        self.x_cord = -(consts.SHIP_ASSET['w'])
        self.last_occurrence_time = time()
        self.ship_appearance_interval = random.randint(25, 40)

    def update(self):
        ''' Updates ship's position and state. '''
        if time() - self.last_occurrence_time >= self.ship_appearance_interval:
            if self.x_cord >= consts.SCREEN_SIZE['w']:
                self.reset()
            else:
                self.x_cord += consts.SHIP_SPEED
