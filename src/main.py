# TODO:
# - beeper sound (playing still alive?)
#
# - maybe fade out and in slightly on each step (so if the picture doesn't
#   change at all, like in a long corridor, there would still be a sense of
#   something happening)
#
# - give each party member a cooldown time after which they can do something
#   (swing sword, cast spell, ...) again. different actions have different
#   cooldowns. that way during fights figuring out a good rotation of the 5
#   party members could be an interesting gameplay aspect
#
# - Dialog messages with animated portrait (eyes, mouth)
#
# - XFiles style date and location.
#
# - hippy elephants are quite intelligent

import global land.land
static import walls, dungeon, font, map, characters, render
static import menu, title, controls, charsel, area, sound, music
import dialogue, game

char background_color[80 * 25]
char foreground_color[80 * 25]
global char screen[80 * 25]
global Game *the_game
global char const *state = "title"

def init():
    land_display_title("Antarctica")

    font_create()
    
    controls_init()

    game_new()

    menu_init()
    title_enter()

def tick():
    if land_closebutton(): land_quit()

    if strcmp(state, "game") ==  0:
        game_tick()
    elif strcmp(state, "title") ==  0:
        title_tick()
    elif strcmp(state, "charsel") == 0:
        charsel_tick()
    elif strcmp(state, "area") == 0:
        area_tick()
    
    menu_tick()
    
    music_tick()

static char const *lyrics[] = {
    "I", "am", "the", "Al", "le", "fant", "!", "",
    "I", "roam", "through", "out", "the", "land", "!", "",
    "Look", "ing", "for", "the", "food", "I", "want", "",
    "Sing", "ing", "all", "the", "way", "...", "...", "...",
    "I", "am", "the", "Al", "le", "fant", "!", "",
    "I", "roam", "through", "out", "the", "land", "!", "",
    "Where", "have", "my", "ba", "na", "nas", "gone", "?",
    "No", "where", "to", "be", "found", ":(", ":(", ":(",
    "And", "so", "my", "sto", "mach", "growls", "", "",
    "Won't", "eat", "no", "o", "ther", "food", "", "",
    "Find", "no", "ba", "na", "na", "tree", "", "",
    "Oh", "no", "how", "can", "this", "be", ":(", "",
    }

def draw():
    
    if strcmp(state, "title") == 0:
        
        title_render((music_ticks() / 15) % 2)
        
        int word = (music_ticks() / 30)
        char s[256] = ""
        for int i in range(word - 1, word + 1):
            if i >= 0 and i < 12 * 8:
                strcat(s, " ")
                strcat(s, lyrics[i])
        int l = strlen(s)
        text((80 - l) / 2 - 2, 2, s)
        
    elif strcmp(state, "game") == 0:
        game_render()
    elif strcmp(state, "charsel") == 0:
        charsel_render()
    elif strcmp(state, "area") == 0:
        area_render()
    menu_render()
    
    land_clear(0, 0, 0, 1)
    land_color(1, 0.6, 0.4, 1)
    land_reset_transform()
    land_scale(2, 2)

    for int y in range(25):
        for int x in range(80):
            char s[] = " "
            s[0] = screen[x + 80 * y]
            land_text_pos(x * 8, 5 + y * 14)
            land_print(s)
    
    land_reset_transform()

land_begin_shortcut(80 * 16, 25 * 28 + 20, 60, LAND_OPENGL | LAND_WINDOWED,
    init, NULL, tick, draw, NULL, NULL)
