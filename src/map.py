import main

def map_draw(int wx, wy, w, h):
    Player *player = the_game->monsters[the_game->player_id]

    int lx = player->x - w / 2
    int ly = player->y - h / 2
    for int j in range(h):
        int y = ly + j
        if y < 0: continue
        if y >= 25: continue
        for int i in range(w):
            int x = lx + i            
            if x < 0: continue
            if x >= 80: continue
            int id = the_game->monstermap[x + y * 80]
            char c
            if id: c = the_game->monsters[id]->letter
            else: c = the_game->dungeon[x + y * 80]
            screen[wx + i + (wy + j) * 80] = c
