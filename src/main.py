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

import global land.land
static import walls, dungeon, font, map
import game

LandFont *font
char background_color[80 * 25]
char foreground_color[80 * 25]
global char screen[80 * 25]
global Game *the_game
    
def init():
    land_display_title("Asciifant")
    
    macro set(r, g, b, a):
        rgba[320 * y + x * 4 + 0] = r
        rgba[320 * y + x * 4 + 1] = g
        rgba[320 * y + x * 4 + 2] = b
        rgba[320 * y + x * 4 + 3] = a

    unsigned char rgba[80 * 192 * 4]
    for int y in range(192):
        for int x in range(80):
            if (x % 10) == 0 or (x % 10) == 9 or\
                (y % 16) == 0 or (y % 16) == 15:
                set(0, 0, 0, 255)                
            elif font_source[y * 80 + x] == '#':
                set(255, 255, 255, 255)
            elif font_source[y * 80 + x] == '.':
                set(0, 0, 0, 0)
                
    LandImage *image = land_image_new(80, 192)
    land_image_set_rgba_data(image, rgba)
    font = land_font_from_image(image, 1, (int []){32, 127});
    land_image_destroy(image)

    game_new()

def rectfill(int x1, y1, x2, y2, char c):
    for int y = y1 while y <= y2 with y++:
        for int x = x1 while x <= x2 with x++:
            screen[x + 80 * y] = c

def hline(int x1, y, x2):
    rectfill(x1, y, x2, y, '.')

def vline(int x, y1, y2):
    rectfill(x, y1, x, y2, '\'')

def dline(int x1, y1, n, dx, dy, c):
    int x = x1
    int y = y1
    for int i in range(n):
        screen[x + 80 * y] = c
        x += dx
        y += dy

def rect(int x1, y1, x2, y2):
    vline(x1, y1, y2)
    vline(x2, y1, y2)
    hline(x1 + 1, y1 - 1, x2 - 1)
    hline(x1 + 1, y2, x2 - 1)

def text(int x, y, char const *f, ...):
    char s[256]
    va_list args
    va_start(args, f)
    vsprintf(s, f, args)
    int n = strlen(s)
    for int i in range(n):
        screen[x + y * 80] = s[i]
        x++
    va_end(args)

def project(int x, y, z, *sx, *sy):
    int d = 12
    *sx = x * d / (z + d)
    *sy = y * d / (z + d)
    if x < 0:
        *sx += 39
    else:
        *sx += 40
    *sy += 12

def draw_wall(int x, y, int offset, distance, side):
    char c = player_get_map(the_game->player, offset, 1 + distance)
    char const *wall = None
    if c == '#': wall = wall0   
    if c == '+': wall = wall1
    
    if not wall: return
    
    int i, j, rowlen, ox, oy, w, h, d
    int values[4][5] = {
        {0, 0, 26, 25, 6},
        {32, 6, 14, 13, 2},
        {48, 8, 10, 9, 1},
        {59, 9, 8, 7, 0}}
    ox = values[distance][0]
    oy = values[distance][1]
    w = values[distance][2]
    h = values[distance][3]
    d = values[distance][4]
    
    if side == 0:
        for j in range(h):
            for i in range(w):                
                screen[x + i + (y + j) * 80] = wall[(ox + i) + (oy + j) * 80]
    elif side == 1 or side == 2:
        int s = 1
        if side == 2:
            s = -1
            oy += 25

        for j in range(h):
            if j < d:
                rowlen = j
            elif j < h - d:
                rowlen = d
            else:
                rowlen = h - j
            for i in range(rowlen):
                screen[x + i * s + (y + j) * 80] = wall[
                    (ox + w + i) + (oy + j) * 80]
    elif side == 3 or side == 4:
        int s = 1
        if side == 4:
            s = -1
            oy += 25
        # only for distance 2 right now
        for j in range(h):
            for i in range(3):
                screen[x + i * s + (y + j) * 80] = wall[
                    (ox + w + 9 + i) + (oy + j) * 80]

def draw_walls(int wx, wy):
    # distance 3 front
    draw_wall(wx + 9 - 14, wy + 9, -2, 3, 0)
    draw_wall(wx + 9 + 14, wy + 9, 2, 3, 0)
    
    draw_wall(wx + 9 - 7, wy + 9, -1, 3, 0)
    draw_wall(wx + 9 + 7, wy + 9, 1, 3, 0)
        
    draw_wall(wx + 9, wy + 9, 0, 3, 0)
    
    # distance 2 side
    draw_wall(wx + 9 - 9, wy + 8, -2, 2, 3)
    draw_wall(wx + 7 + 18, wy + 8, 2, 2, 4)

    draw_wall(wx + 9, wy + 8, -1, 2, 1)
    draw_wall(wx + 7 + 9, wy + 8, 1, 2, 2)
    
    # distance 2 front
    draw_wall(wx + 8 - 9, wy + 8, -1, 2, 0)
    draw_wall(wx + 8 + 9, wy + 8, 1, 2, 0)
    
    draw_wall(wx + 8, wy + 8, 0, 2, 0)
    
    # distance 1 side
    draw_wall(wx + 5 + 13, wy + 6, 1, 1, 2)
    draw_wall(wx + 7, wy + 6, -1, 1, 1)
    
    # distance 1 front
    draw_wall(wx + 6 - 13, wy + 6, -1, 1, 0)
    draw_wall(wx + 6 + 13, wy + 6, 1, 1, 0)
    
    draw_wall(wx + 6, wy + 6, 0, 1, 0)
    
    # distance 0 side
    draw_wall(wx + 1, wy + 0, -1, 0, 1)
    draw_wall(wx + 24, wy + 0, 1, 0, 2)
    
    # distance 0 front
    draw_wall(wx + 25, wy + 0, 1, 0, 0)
    draw_wall(wx - 25, wy + 0, -1, 0, 0)
    
    draw_wall(wx + 0, wy + 0, 0, 0, 0)

def update_screen():
    int wx = 40 - 13, wy = 0

    rectfill(40 - 13, 0, 40 + 12, 24, ' ')

    draw_walls(wx, wy)
    
    rectfill(0, 0, wx - 1, 24, ' ')
    rectfill(wx + 26, 0, 79, 24, ' ')

    if 0:
        int step = 0
        int x[4] = {-12, 12, -12, 12}, y[4] = {-12, -12, 12, 12}, z
        int px[4], py[4]
        int sx[4], sy[4]
        
        for int j in range(4):
            for int i in range(4):
                px[i] = sx[i]
                py[i] = sy[i]
                z = j * 12 + step * 3
                project(x[i], y[i], z, &sx[i], &sy[i])
                #screen[sx[i] + sy[i] * 80] = '*'
            rect(sx[0], sy[0] + 1, sx[3], sy[3])
            if j > 0:
                dline(px[0] + 1, py[0] + 1, sx[0] - px[0], 1, 1, '\\')
                dline(px[1] - 1, py[1] + 1, px[1] - sx[1], -1, 1, '/')
                dline(px[2] + 1, py[2], sx[2] - px[2], 1, -1, '/')
                dline(px[3] - 1, py[3], px[3] - sx[3], -1, -1, '\\')
    
    #int x = 40 - 13 + step, y = 1 + step
    #int w = 26 - step * 2, h = 24 - step * 2
    #int s = 4
    #for int j in range(2):
    #    rect(x, y, x + w - 1, y + h - 1)
    #    dline(x + 1, y, s, 1, 1, '\\')
    #    dline(x + 1, y + h - 1, s, 1, -1, '/')
    #    dline(x + w - 2, y + h - 1, s, -1, -1, '\\')
    #    dline(x + w - 2, y, s, -1, 1, '/')
    #    x += s
    #    y += s
    #    w -= s * 2
    #    h -= s * 2
    #    s--
    #rect(x, y, x + w - 1, y + h - 1)
    
    rect(59, 1, 79, 12)
    text(60, 0, "Map")
    
    rectfill(60, 1, 60 + 18, 1 + 10, 127)
    map_draw(60, 1, 19, 11)
    screen[80 * 6 + 69] = '@'
    
    rect(0, 1, 26, 24)
    for int i in range(5):
        hline(1, i * 5, 25)
        text(1, i * 5, "Party Member")
    
    rect(59, 13, 79, 24)
    text(60, 12, "Inventory")
    
    rect(53, 1, 58, 24)

def tick():
    if land_closebutton(): land_quit()
    if land_key_pressed(LandKeyEscape): land_quit()
    
    int keymap = 0
    if land_key_pressed(LandKeyLeft): keymap |= 8
    if land_key_pressed(LandKeyRight): keymap |= 2
    if land_key_pressed(LandKeyUp): keymap |= 1
    if land_key_pressed(LandKeyDown): keymap |= 4
    if land_key(LandKeyLeftShift): keymap <<= 4
    if land_key(LandKeyRightShift): keymap <<= 4
    if land_key(LandKeyLeftAlt): keymap <<= 4
    if land_key(LandKeyRightAlt): keymap <<= 4
    if land_key_pressed('q'): keymap |= 128
    if land_key_pressed('e'): keymap |= 32
    if land_key_pressed('w'): keymap |= 1
    if land_key_pressed('s'): keymap |= 4
    if land_key_pressed('a'): keymap |= 8
    if land_key_pressed('d'): keymap |= 2

    player_input(the_game->player, keymap)
    
    update_screen()

def draw():
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

land_begin_shortcut(80 * 16, 25 * 28 + 20, 60, LAND_OPENGL | LAND_WINDOWED,
    init, NULL, tick, draw, NULL, NULL)
