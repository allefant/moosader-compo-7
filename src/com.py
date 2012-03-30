import main, menu
static import charsel

def com_new_game(Menu *menu, char const *command):
    if land_key_pressed(LandKeyEnter):
        charsel_enter()

def com_continue(Menu *menu, char const *command):
    if land_key_pressed(LandKeyEnter):
        game_enter()

def com_quit(Menu *menu, char const *command):
    if land_key_pressed(LandKeyEnter):
        land_quit()
