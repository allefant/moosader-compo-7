import main
static import game, controls, charsel, item

class Player:
    int id
    int x, y, d
    int hp, max_hp
    int ammo, max_ammo
    int xp, level
    char name[20]
    char letter
    
    int inventory[11]
    int amount[11]
    
    int focus
    
    int next_in_party

# Directions:
#     0
#     N
# 3 W   E 1
#     S 
#     2
static int const ddx[] = {0, 1, 0, -1}
static int const ddy[] = {-1, 0, 1, 0}

bool def player_add_item(Player *self, int iid):
    for int i in range(11):
        if self->inventory[i] == iid:
            self->amount[i]++
            return True
    
    for int i in range(11):
        if not self->inventory[i]:
            self->inventory[i] = iid
            self->amount[i] = 1
            return True
    return False

char def player_get_map_xy(Player *self, int x, y):
    return the_game->dungeon[y * 80 + x]

int def player_get_monster_xy(Player *self, int x, y):
    if y < 0 or x < 0 or y >= 25 or x >= 80: return 0
    return the_game->monstermap[y * 80 + x]

def player_set_map_xy(Player *self, int x, y, char c):
    the_game->dungeon[y * 80 + x] = c

def player_set_monster_xy(Player *self, int x, y, int id):
    the_game->monstermap[y * 80 + x] = id

def player_get_map_forward_pos(Player *self, int offset, distance,
        int *x, *y):
    int dx = ddx[self->d]
    int dy = ddy[self->d]
    int rx = -dy
    int ry = dx
    *x = self->x + dx * distance + rx * offset
    *y = self->y + dy * distance + ry * offset
    return

char def player_get_map_forward(Player *self, int offset, distance):
    int x, y
    player_get_map_forward_pos(self, offset, distance, &x, &y)
    return player_get_map_xy(self, x, y)

int def player_get_monster_forward(Player *self, int offset, distance):
    int x, y
    player_get_map_forward_pos(self, offset, distance, &x, &y)
    return player_get_monster_xy(self, x, y)

Player *def player_new(int id, x, y, char letter, char const *name):
    Player *self; land_alloc(self)
    
    memcpy(self->name, name, 20)

    self->letter = letter
    self->id = id
    self->x = x
    self->y = y
    
    return self

def player_input(Player *self, int bits):
    int turn = -1
    int move_x = 0, move_y = 0

    int dx = ddx[self->d]
    int dy = ddy[self->d]

    if bits & (1 << TurnMoveNorth): turn = 0
    if bits & (1 << TurnMoveEast): turn = 1
    if bits & (1 << TurnMoveSouth): turn = 2
    if bits & (1 << TurnMoveWest): turn = 3
    
    if turn != -1:

        if turn == self->d:
            move_x = dx
            move_y = dy
            turn = -1
        else:
            self->d = turn
            dx = ddx[self->d]
            dy = ddy[self->d]
    
    int rx = -dy
    int ry = dx
    
    if move_x == 0 and move_y == 0 and turn == -1:
        if bits & (1 << MoveForward):
            move_x += dx
            move_y += dy
        if bits & (1 << MoveBackward):
            move_x -= dx
            move_y -= dy
            
        int m = bits & (1 << StrafeModifier)
        int ml = bits & (1 << MoveLeft)
        int mr = bits & (1 << MoveRight)
        int tl = bits & (1 << TurnLeft)
        int tr = bits & (1 << TurnRight)
            
        if (mr and not m) or (tr and m):
            move_x += rx
            move_y += ry
        if (ml and not m) or (tl and m):
            move_x -= rx
            move_y -= ry
        if (tl and not m) or (ml and m):
            self->d--
            if self->d < 0: self->d += 4
        if (tr and not m) or (mr and m):
            self->d++
            if self->d >= 4: self->d -= 4

    if move_x or move_y:
        int tx = self->x + move_x, ty = self->y + move_y
        int m = player_get_monster_xy(self, tx, ty)

        char cw = player_get_map_xy(self, tx, ty)

        if m == 0 and cw != ' ':
            # check for item to pick up
            for int i in range(1, 256):
                if not items[i].letter: break
                if items[i].letter == cw:
                    if player_add_item(self, i):
                        player_set_map_xy(self, tx, ty, ' ')
                    cw = ' '
            
        if m == 0 and cw == ' ':
            player_set_monster_xy(self, self->x, self->y, 0)
            self->x += move_x
            self->y += move_y
            player_set_monster_xy(self, self->x, self->y, self->id)

    self->focus = 0
    for int i in range(4):
        int m = player_get_monster_forward(self, 0, 1 + i)
        if m:
            self->focus = m
            break
