import main
static import game

class Player:
    int x, y, d
    
static int const ddx[] = {0, 1, 0, -1}
static int const ddy[] = {-1, 0, 1, 0}

char def player_get_map(Player *self, int offset, distance):
    int dx = ddx[self->d]
    int dy = ddy[self->d]
    int rx = -dy
    int ry = dx
    int x = self->x + dx * distance + rx * offset
    int y = self->y + dy * distance + ry * offset
    return the_game->dungeon[y * 80 + x]

Player *def player_new():
    Player *self; land_alloc(self)
    
    for int y in range(25):
        for int x in range(80):
            if the_game->dungeon[y * 80 + x] == 'S':
                the_game->dungeon[y * 80 + x] = ' '
                self->x = x
                self->y = y
    
    return self

def player_input(Player *self, int bits):
    int turn = -1

    if bits == 1: turn = 0
    if bits == 2: turn = 1
    if bits == 4: turn = 2
    if bits == 8: turn = 3
    
    if turn == -1: return
    
    if turn != self->d:
        self->d = turn
    else:
        char c = player_get_map(self, 0, 1)
        if c == ' ':
            int dx = ddx[self->d]
            int dy = ddy[self->d]
            self->x += dx
            self->y += dy

        
