''' Module containing Menus class. '''

import json
from datetime import datetime

import pyxel

import consts


class Menus:
    ''' Class containing methods and variables related to game's menus like
        start, pause or score menus and navigating in them. '''
    def __init__(self):
        self.score = 0
        self.score_saved = False
        self.selected_item = 1
        self.options = {1: consts.GREEN, 2: consts.WHITE, 3: consts.WHITE}

    def draw_score(self, final=False):
        ''' Draws score text and score amount at the top of the screen. If
            it's a final score (final=True) at the end screen, it will be
            drawn slightly lower. '''
        y_cord = consts.SCORE_TEXT[
            'y'] + consts.MEDIUM_MARGIN if final else consts.SCORE_TEXT['y']
        x1_cord = consts.LIVES_TEXT['x'] if final else consts.SCORE_TEXT['x']
        x2_cord = consts.LIVES_VALUE['x'] if final else consts.SCORE_VALUE['x']
        pyxel.text(x1_cord, y_cord, 'SCORE', consts.WHITE)
        pyxel.text(x2_cord, y_cord, str(self.score), consts.GREEN)

    @staticmethod
    def draw_lives(lives):
        ''' Draws information regaring current amount of lives. '''
        pyxel.text(consts.LIVES_TEXT['x'], consts.LIVES_TEXT['y'], 'LIVES',
                   consts.WHITE)
        pyxel.text(consts.LIVES_VALUE['x'], consts.LIVES_VALUE['y'],
                   str(lives), consts.GREEN)

    def draw_high_scores(self):
        ''' Draws top 5 scores with a date. '''
        high_scores = self.get_high_scores()
        margin = 0
        for score in high_scores:
            pyxel.text(consts.TOP_TEXT['x'], consts.TOP_TEXT['y'] + margin,
                       str(score[0]), consts.WHITE)
            pyxel.text(consts.TOP_TEXT['x'] + 80,
                       consts.TOP_TEXT['y'] + margin, str(score[1]),
                       consts.GREEN)
            margin += 15

    def draw_menu_screen(self, texts):
        ''' Draws all menu options from menu options list. '''
        pyxel.text(consts.TOP_TEXT['x'], consts.TOP_TEXT['y'],
                   texts['top_text'], consts.WHITE)
        for index, text in enumerate(texts['options']):
            pyxel.text(
                consts.SMALL_MARGIN, consts.SCREEN_SIZE['h'] -
                (len(texts['options']) - index) * consts.MEDIUM_MARGIN, text,
                self.options[index + 1])

    def make_selected_item_green(self, items):
        ''' Changes color of currently selected menu options to green and
            also sets other options' color to white. '''
        if pyxel.btnp(pyxel.KEY_UP) and self.selected_item > 1:
            self.selected_item -= 1
        if pyxel.btnp(pyxel.KEY_DOWN) and self.selected_item < items:
            self.selected_item += 1
        for option in self.options:
            self.options.update({option: consts.WHITE})
        self.options.update({self.selected_item: consts.GREEN})

    def navigation(self, game, lives):
        ''' Main navigation function that changes game's state according to
            current game state and selected item. '''
        items = 3
        if game.state == 'start':
            if pyxel.btnp(pyxel.KEY_ENTER
                          ) and self.selected_item == 1 and lives >= 1:
                game.state = 'game'
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 2:
                game.state = 'controls'
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 3:
                pyxel.quit()
        elif game.state == 'controls':
            items = 2
            if pyxel.btnp(pyxel.KEY_ENTER
                          ) and self.selected_item == 1 and lives >= 1:
                game.state = 'game'
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 2:
                pyxel.quit()
        elif game.state == 'pause':
            if pyxel.btnp(pyxel.KEY_ENTER
                          ) and self.selected_item == 1 and lives >= 1:
                game.state = 'game'
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 2:
                game.reset()
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 3:
                pyxel.quit()
        elif game.state == 'end':
            if pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 1:
                game.reset()
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 2:
                game.state = 'scores'
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 3:
                pyxel.quit()
        elif game.state == 'scores':
            items = 2
            if pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 1:
                game.reset()
            elif pyxel.btnp(pyxel.KEY_ENTER) and self.selected_item == 2:
                pyxel.quit()
        self.make_selected_item_green(items)

    @staticmethod
    def read_scores():
        ''' Reads scores from scores.json file and returns them as dict. '''
        try:
            with open('scores.json') as scores_file:
                scores_data = json.load(scores_file)
        except FileNotFoundError:
            with open('scores.json', 'w') as scores_file:
                json.dump({}, scores_file)
        finally:
            with open('scores.json') as scores_file:
                scores_data = json.load(scores_file)
        return scores_data

    def save_score(self):
        ''' Saves score to scores.json file. '''
        if not self.score_saved:
            scores_data = self.read_scores()
            scores_data.update(
                {datetime.now().strftime('%Y-%m-%d %H:%M:%S'): self.score})
            with open('scores.json', 'w') as scores_file:
                json.dump(scores_data, scores_file)
        self.score_saved = True

    def get_high_scores(self):
        ''' Returns top 5 scores in a list. '''
        scores_data = self.read_scores()
        scores = []
        sorted_scores = []
        for _, score in scores_data.items():
            scores.append(score)
        scores.sort(reverse=True)
        for score in scores[:5]:
            sorted_scores.append([
                list(scores_data.keys())[list(
                    scores_data.values()).index(score)], score
            ])
        return sorted_scores
