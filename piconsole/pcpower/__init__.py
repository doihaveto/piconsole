from . import views, utils, settings

NAME = 'pcpower'
DISPLAY_NAME = 'PC Power'
ENDPOINT = 'pcpower' # name of function that displays the app content

for pc in settings.PCS:
    utils.gpio_setup(pc)
