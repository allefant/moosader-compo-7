import main
import player
static import dungeon

class Game:
    Player *player
    char dungeon[80 * 25]

Game *def game_new():
    Game *self; land_alloc(self)
    the_game = self
    memcpy(self->dungeon, dungeon1, 80 * 25)
    self->player = player_new()
    return self
