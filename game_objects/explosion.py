''' Module containing Explosion class. '''

from time import time

import pyxel

import consts


class Explosion:
    ''' Class responsible for drawing and clearing explosion flashes. '''
    def __init__(self):
        self.flashes = []

    @staticmethod
    def draw(flashes, asset):
        ''' Draws every explosion flash from image bank in the loop. '''
        for flash in flashes:
            pyxel.blt(flash['x'], flash['y'], 0, asset['x'], asset['y'],
                      asset['w'], asset['h'])

    def draw_flashes(self):
        ''' Draws all explosion flashes from flashes list. '''
        self.draw(self.flashes, consts.EXPLOSION_ASSET)

    @staticmethod
    def clear(flashes):
        ''' Clears every explosion flash in the loop. '''
        for index, flash in enumerate(flashes):
            if time() - flash['time'] >= consts.EXPLOSION_DISPLAY_TIME:
                flashes.pop(index)

    def clear_flashes(self):
        ''' Clears all explosion flashes from flashes list. '''
        self.clear(self.flashes)
