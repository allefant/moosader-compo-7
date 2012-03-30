import main
static import walls, map, title, monsters

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
    vline(x1, y1 + 1, y2)
    vline(x2, y1 + 1, y2)
    hline(x1 + 1, y1, x2 - 1)
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

def blit(char * to_addr, int to_w, tx, ty,
    char const *from_addr, int from_w, fx, fy, w, h):
    for int j in range(h):
        for int i in range(w):                
            to_addr[tx + i + (ty + j) * to_w] =\
                from_addr[(fx + i) + (fy + j) * from_w]

def blit_mirror_masked(char * to_addr, int to_w, tx, ty,
    char const *from_addr, int from_w, fx, fy, w, h):
    for int j in range(h):
        for int i in range(w):   
            char c = from_addr[(fx + i) + (fy + j) * from_w]
            if c == ' ': continue
            if c == 'e': c = ' '
            to_addr[tx - i + (ty + j) * to_w] = c
                

static def blit_masked(char * to_addr, int to_w, tx, ty,
    char const *from_addr, int from_w, fx, fy, w, h):
    for int j in range(h):
        for int i in range(w):        
            char c = from_addr[(fx + i) + (fy + j) * from_w]
            if c == ' ': continue
            if c == 'e': c = ' '
            to_addr[tx + i + (ty + j) * to_w] = c

def draw_wall(int x, y, int offset, distance, side):
    char c = player_get_map_forward(the_game->player, offset, 1 + distance)
    char const *wall = None
    bool monster = False
    #bool mirror = False
    
    if c == '#': wall = wall0   
    if c == '+': wall = wall1
    if c == 'M': wall = monster0; monster = True
    if c == 'A': wall = monster1; monster = True

    if not wall: return

    int ox, oy, w, h, d
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
        if monster: blit_masked(screen, 80, x, y, wall, 80, ox, oy, w, h)
        else: blit(screen, 80, x, y, wall, 80, ox, oy, w, h)
    elif side == 1 or side == 2:
        bool mirror = False
        if side == 2:
            mirror = True
            oy += 25

        if monster: pass
        elif mirror: blit_mirror_masked(screen, 80, x, y, wall, 80, ox + w, oy, d, h)
        else: blit_masked(screen, 80, x, y, wall, 80, ox + w, oy, d, h)

    elif side == 3 or side == 4:
        bool mirror = False
        if side == 4:
            mirror = True
            oy += 25
        # only for distance 2 right now
        if monster: pass
        elif mirror: blit_mirror_masked(screen, 80, x, y, wall, 80, ox + w + 9, oy, 3, h)
        else: blit_masked(screen, 80, x, y, wall, 80, ox + w + 9, oy, 3, h)

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

def game_render():
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
            rect(sx[0], sy[0], sx[3], sy[3])
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
    
    rect(59, 0, 79, 12)
    text(60, 0, "Map")
    
    rectfill(60, 1, 60 + 18, 1 + 10, 127)
    map_draw(60, 1, 19, 11)
    screen[80 * 6 + 69] = '@'
    
    rect(0, 0, 26, 24)
    for int i in range(5):
        hline(1, i * 5, 25)
        text(1, i * 5, "Party Member")
    
    rect(59, 12, 79, 24)
    text(60, 12, "Inventory")
    
    rect(53, 0, 58, 24)