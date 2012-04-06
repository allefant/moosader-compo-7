import main
static import render, menu, title
static int start_tick
static int pos

char const *area_name = "Capitol\nWashington, D.C.\nApril 1st, 2045"

def area_enter():
    menu_root()
    state = "area"
    start_tick = land_get_ticks()
    pos = 0

def area_tick():
    if land_key_pressed(LandKeyEnter):
        game_enter()
    
    if land_key_pressed(LandKeyEscape):
        game_enter()

def area_render():
    title_render(1)
    
    int n = (land_get_ticks() - start_tick) / 2
    
    if n > (int)strlen(area_name):
        n = strlen(area_name)

    int x = 1, y = 1
    for int i in range(n):
        if area_name[i] == '\n':
            x = 1
            y++
        else:
            screen[y * 80 + x] = area_name[i]
            x++
    
