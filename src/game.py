import main
import player
static import dungeon, menu, controls, title

class Game:
    Player *player
    char dungeon[80 * 25]

Game *def game_new():
    Game *self; land_alloc(self)
    the_game = self
    memcpy(self->dungeon, dungeon1, 80 * 25)
    self->player = player_new()
    return self

def game_enter():
    menu_root()
    state = "game"

def game_tick():
    if land_key_pressed(LandKeyEscape):
        title_enter()
        return

    int keymap = controls_get_keymap()
    player_input(the_game->player, keymap)
