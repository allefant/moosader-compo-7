import main
import player, dialogue
static import dungeon, menu, controls, title, charsel, item, music

class Game:
    int player_id
    Player *monsters[256]
    char dungeon[80 * 25]
    int monstermap[80 * 25]
    
    char const *state
    
    Reply reply

def scan_starting_positions():
    int npc = 0
    int n = 1
    for int y in range(25):
        for int x in range(80):
            char const *name = None
            char c = the_game->dungeon[y * 80 + x]
            if c == '@':
                name = charsel_name()
                the_game->player_id = n
            elif c >= '0' and c <= '9':
                npc = c - '0'
                the_game->dungeon[y * 80 + x] = ' '
            elif c == 'A':
                name = "The Allefant"
            elif c == 'Z':
                name = "Zombie"
            elif c == 'H':
                name = npclist[npc]
            elif c == 'D':
                name = npclist[npc]
            
            if name:
                the_game->dungeon[y * 80 + x] = ' '
                the_game->monstermap[y * 80 + x] = n
                Player *m = player_new(n, x, y, c, name)
                the_game->monsters[n++] = m

Game *def game_new():
    Game *self; land_alloc(self)
    the_game = self
    memcpy(self->dungeon, dungeon1, 80 * 25)
    
    items_init()
    dialogue_init()
    
    scan_starting_positions()
    
    self->state = "new"
    
    return self

def game_enter():
    
    music_play_tune(music_tune2)
    
    menu_root()
    state = "game"

def game_tick():
    Player *player = the_game->monsters[the_game->player_id]

    if land_key_pressed(LandKeyEscape):
        title_enter()
        return

    if strcmp(the_game->state, "new") == 0:
        if land_key_pressed(LandKeyEnter):
            the_game->state = "onwards"
    elif strcmp(the_game->state, "dialogue") == 0:
        int keymap = controls_get_keymap()
        dialogue_input(player, keymap)
    else:
        int keymap = controls_get_keymap()
        player_input(player, keymap)
