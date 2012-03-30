import main, com
static import render

class Menu:
    char *name
    void (*cb)(Menu *m, char const *command)
    int x, y

    Menu *first_child, *last_child
    Menu *next, *prev

static int mx, my, spacing
static Menu *root, *focus

char const *def menu_get_focus():
    if focus: return focus->name
    return ""

def menu_pos(int x, y, s):
    mx = x
    my = y
    spacing = s

Menu *def menu_add(char const *name, void (*cb)(Menu *m, char const *command)):
    Menu *self
    land_alloc(self)
    if name: self->name = land_strdup(name)
    self->cb = cb
    self->x = mx
    self->y = my
    my += spacing

    if root:
        if root->last_child:
            self->prev = root->last_child
            root->last_child->next = self
        else:
            root->first_child = self
        root->last_child = self

    return self

def menu_del(Menu *self):
    if not self: return
    Menu *next
    for Menu *menu = self->first_child while menu with menu = next:
        land_free(menu)
        next = menu->next
    land_free(self->name)
    land_free(self)

def menu_root():
    menu_del(root)
    root = None
    focus = None
    root = menu_add(None, None)

def menu_focus(Menu *self):
    focus = self

def menu_init():
    pass

def menu_tick():
    if not root: return

    if land_key_pressed(LandKeyDown):
        if focus:
            focus = focus->next
            if not focus: focus = root->first_child
    
    if land_key_pressed(LandKeyUp):
        if focus:
            focus = focus->prev
            if not focus: focus = root->last_child
    
    if focus and focus->cb:
        focus->cb(focus, "tick")

def menu_render():
    if not root: return
    for Menu *menu = root->first_child while menu with menu = menu->next:
        char focused[3] = "  "
        if menu == focus: focused[0] = '*'
        text(menu->x, menu->y, "%s%s", focused, menu->name)
        

