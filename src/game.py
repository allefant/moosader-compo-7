import main
import player
static import dungeon, menu, controls, title, charsel

class Game:
    int player_id
    Player *monsters[256]
    char dungeon[80 * 25]
    char monstermap[80 * 25]

def scan_starting_positions():
    int n = 1
    for int y in range(25):
        for int x in range(80):
            char const *name = None
            if the_game->dungeon[y * 80 + x] == '@':
                name = charsel_name()
                the_game->player_id = n
            elif the_game->dungeon[y * 80 + x] == 'A':
                name = "The Allefant"
            if the_game->dungeon[y * 80 + x] == 'Z':
                name = "Zombie"
            
            if name:
                the_game->monstermap[y * 80 + x] = the_game->dungeon[y * 80 + x]
                the_game->dungeon[y * 80 + x] = ' '
                Player *m = player_new(n, x, y, name)
                the_game->monsters[n++] = m

Game *def game_new():
    Game *self; land_alloc(self)
    the_game = self
    memcpy(self->dungeon, dungeon1, 80 * 25)
    
    scan_starting_positions()
    
    return self

def game_enter():
    menu_root()
    state = "game"

def game_tick():
    Player *player = the_game->monsters[the_game->player_id]

    if land_key_pressed(LandKeyEscape):
        title_enter()
        return

    int keymap = controls_get_keymap()
    player_input(player, keymap)
