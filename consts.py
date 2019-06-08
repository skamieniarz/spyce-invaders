''' Module containing constants. '''

# GAME OPTIONS
SCREEN_SIZE = {'w': 250, 'h': 200}  # 255 is max for both
SCALE = 3

# CANNON
CANNON_SPEED = 2
BEAMS_SPEED = 5

# INVADERS
INVADERS_PROJECTILES_SPEED = 3
INVADERS_MARCHING_SPEED = 2
APPROACH_SHORTENING_INTERVAL = 5
APPROACH_SHORTENING_VALUE = 0.1
MARCHING_SOUND_SPEEDS = {
    1.0: 60,
    0.9: 55,
    0.8: 50,
    0.7: 45,
    0.6: 40,
    0.5: 35,
    0.4: 30,
    0.3: 25,
    0.2: 20,
    0.1: 15,
    0.0: 10
}

# SHIP
SHIP_SPEED = 1

# ↑ one can experiment with values above ↑
# ↓ one does not simply experiment with values below ↓

# COLORS
BLACK = 0
WHITE = 7
GREEN = 11

# SCORE, LIVES AND MENU
SMALL_MARGIN = 5
MEDIUM_MARGIN = 10
BIG_MARGIN = 25
TOP_TEXT = {'x': SMALL_MARGIN, 'y': SMALL_MARGIN}
LIVES_TEXT = {'x': SMALL_MARGIN, 'y': SMALL_MARGIN}
LIVES_VALUE = {'x': LIVES_TEXT['x'] + BIG_MARGIN, 'y': LIVES_TEXT['y']}
SCORE_TEXT = {'x': LIVES_VALUE['x'] + MEDIUM_MARGIN, 'y': LIVES_TEXT['y']}
SCORE_VALUE = {'x': SCORE_TEXT['x'] + BIG_MARGIN, 'y': LIVES_TEXT['y']}
MENU_SCREENS = ['start', 'controls', 'pause', 'end', 'scores']
START_SCREEN = {
    'top_text': 'SPYCE INVADERS',
    'options': ['START', 'CONTROLS', 'QUIT']
}
CONTROLS_SCREEN = {
    'top_text': '''CONTROLS:
    \n< AND > ARROW KEYS TO MOVE THE LASER CANNON,
    \nSPACE TO SHOOT,
    \nQ OR P TO PAUSE THE GAME.''',
    'options': ['START', 'QUIT']
}
PAUSE_SCREEN = {'top_text': '', 'options': ['CONTINUE', 'RESTART', 'QUIT']}
END_SCREEN = {
    'top_text': 'THE INVASION WAS SUCCESSFUL.',
    'options': ['START AGAIN', 'HIGH SCORES', 'QUIT']
}
SCORES_SCREEN = {'top_text': '', 'options': ['START AGAIN', 'QUIT']}

# LASER CANNON
CANNON_ASSET = {
    1: {
        'x': 34,
        'y': 33
    },
    2: {
        'x': 18,
        'y': 33
    },
    3: {
        'x': 2,
        'y': 33
    },
    'w': 13,
    'h': 13,
    'barrel': 6
}
CANNON_SCREEN_MARGIN = 2

# INVADERS
FIRST_INVADER = {'x': 5, 'y': 30}
INVADERS_ASSETS = {
    'x1': 1,
    'x2': 17,
    'w': 14,
    'h': 8,
    1: {
        'y': 68,
        'w': 12
    },
    2: {
        'y': 52,
        'w': 14
    },
    3: {
        'y': 84,
        'w': 12
    }
}
INVADERS_AMOUNT_PER_ROW = 11
INVADERS_ROWS = 5
POINTS_FOR_INVADER = {1: 10, 2: 20, 3: 40}
INVADERS_SCREEN_MARGIN = 2

# SHIP
SHIP_ASSET = {'x': 0, 'y': 3, 'w': 16, 'h': 7}
POINTS_FOR_SHIP = [50, 100, 150, 200]

# EXPLOSIONS
SMALL_EXPLOSION_ASSET = {'x': 3, 'y': 18, 'w': 9, 'h': 8}
EXPLOSION_ASSET = {'x': 18, 'y': 17, 'w': 10, 'h': 11}
EXPLOSION_DISPLAY_TIME = 0.2
