'''
Spyce Invaders - slightly modified clone of Space Invaders classic game
implemented with pyxel (https://github.com/kitao/pyxel).

Shoot all the invaders before they reach you or destroy you!

Controls:
    ↑ and ↓ arrow keys to select options in menus,
    ENTER to choose option in menus,
    ← and → arrow keys to move the laser cannon left and right,
    SPACE to shoot the laser cannon,
    Q or P to pause the game.

Created by @skamieniarz (https://github.com/skamieniarz) in 2019.
'''

import pyxel

import consts
from cannon import Cannon
from explosion import Explosion
from invaders import Invaders
from menus import Menus
from ship import Ship


class SpyceInvaders:
    ''' Main game class. '''

    def __init__(self):
        pyxel.init(consts.SCREEN_SIZE['w'],
                   consts.SCREEN_SIZE['h'],
                   caption='Spyce Invaders',
                   scale=consts.SCALE)
        self.cannon = Cannon()
        self.invaders = Invaders()
        self.ship = Ship()
        self.menus = Menus()
        self.explosion = Explosion()
        self.state = 'start'
        pyxel.load('spyce_invaders.pyxel')
        pyxel.run(self.update, self.draw)

    def reset(self):
        ''' Resets the game. '''
        self.cannon = Cannon()
        self.invaders = Invaders()
        self.ship = Ship()
        self.menus = Menus()
        self.explosion = Explosion()
        self.state = 'game'

    def update(self):
        ''' Main update function. '''
        if self.state in consts.MENU_SCREENS:
            self.menus.navigation(self, self.cannon.lives)

        if self.state == 'game':
            if (pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_P)):
                self.state = 'pause'

            self.cannon.launch_beam()
            self.invaders.launch_projectile()
            self.cannon.update_position()

            if self.cannon.beams:
                self.cannon.update_beams()
                self.cannon.beam_hit_event(self.invaders.units, self.ship,
                                           self.explosion, self.menus)
                self.cannon.pop_invisible_beams()

            if self.invaders.projectiles:
                self.invaders.update_projectiles()
                self.invaders.projectile_hit_event(self.cannon, self.invaders,
                                                   self.explosion)
                self.invaders.pop_invisible_projectiles()

            self.invaders.units_march()
            self.invaders.check_arrival(self.cannon, self)
            self.invaders.shorten_approach_time_interval()
            self.invaders.next_wave()
            self.ship.update()

            if self.cannon.lives == 0:
                self.state = 'end'
                self.menus.save_score()

        self.explosion.clear_flashes()

    def draw(self):
        ''' Main draw function that draws game's objects. '''
        pyxel.cls(consts.BLACK)

        if self.state == 'start':
            self.menus.draw_menu_screen(consts.START_SCREEN)

        if self.state == 'controls':
            self.menus.draw_menu_screen(consts.CONTROLS_SCREEN)

        if self.state == 'game':
            self.cannon.draw(self.cannon)
            if self.cannon.beams:
                self.cannon.draw_beams()
            if self.invaders.projectiles:
                self.invaders.draw_projectiles()
            if self.invaders.units:
                self.invaders.draw_wave()
            if self.explosion.flashes:
                self.explosion.draw_flashes()
            self.ship.draw()
            self.menus.draw_score()
            self.menus.draw_lives(self.cannon.lives)

        if self.state == 'pause':
            self.menus.draw_score()
            self.menus.draw_lives(self.cannon.lives)
            self.menus.draw_menu_screen(consts.PAUSE_SCREEN)

        if self.state == 'end':
            if self.explosion.flashes:
                self.explosion.draw_flashes()
            self.menus.draw_score(final=True)
            self.menus.draw_menu_screen(consts.END_SCREEN)

        if self.state == 'scores':
            self.menus.draw_menu_screen(consts.SCORES_SCREEN)
            self.menus.draw_high_scores()


if __name__ == '__main__':
    SpyceInvaders()
