import main
static import menu, title, characters, render, font, area

static int charsel_portrait[5]
static int part_sel
static char const *part_names[] = {"face ", "eyes ", "hair ", "nose ", "mouth "}
static char char_name[20] = "Indy D. V. Loper"
static int profession
static int cursor_pos
static int alignment

static char const *organizations[] = {
    "Central Intelligence Agency",
    "Federal Bureau of Investigation",
    "National Security Agency",
    "Department of Homeland Security",
    "Counter Terrorism Unit",
    "Employee Access Card",
    "Wikileaks Task Force",
    }
static char const *logos[] = {
    "CIA",
    "FBI",
    "NSA",
    "DHS",
    "CTU",
    "",
    "WTF",
    }
static char const *jobs[] = {
    "CIA",
    "FBI",
    "NSA",
    "DHS",
    "NCTC",
    "Janitor",
    "WTF"
    }
static char const *titles[] = {
    "Special Agent ",
    "Special Agent ",
    "Special Agent ",
    "Special Agent ",
    "Special Agent ",
    "",
    "Special Agent ",
    }

#static char const *alignments[] = {
#    "Lawful Good",
#    "Neutral Good",
#    "Chaotic Good", 
#    "Lawful Neutral",
#    "True Neutral",
#    "Chaotic Neutral", 
#    "Lawful Evil",
#    "Neutral Evil",
#    "Chaotic Evil",
#    }

static def select_next(int part, d):
    int sel = charsel_portrait[part]
    for int i in range(characters_count):
        sel += d + characters_count
        sel %= characters_count
        int n = strlen(part_names[part])
        if memcmp(portraits[sel] + 12 * 20, part_names[part], n) == 0:
            break
    charsel_portrait[part] = sel

int def charsel_get_part(char const *name):
    for int i in range(characters_count):
        int n = strlen(name)
        if memcmp(portraits[i] + 12 * 20, name, n) == 0:
            return i
    return 0

static def com_select(Menu *menu, char const *command):
    int d = 0

    if land_key_pressed(LandKeyLeft):
        d = -1
    
    if land_key_pressed(LandKeyRight):
        d = 1
    
    if land_key_pressed(LandKeyEnter):
        d = 1
    
    if not d: return

    if strcmp(menu->name, "Face") == 0: part_sel = 0
    if strcmp(menu->name, "Eyes") == 0: part_sel = 1
    if strcmp(menu->name, "Hair") == 0: part_sel = 2
    if strcmp(menu->name, "Nose") == 0: part_sel = 3
    if strcmp(menu->name, "Mouth") == 0: part_sel = 4

    select_next(part_sel, d)

static char const *def get_help(char const *name):
    if strcmp(name, "Name") == 0: return "Type a new name."
    if strcmp(name, "Face") == 0: return "Change the face shape."
    if strcmp(name, "Eyes") == 0: return "Change the eye shape."
    if strcmp(name, "Hair") == 0: return "Change the hair style."
    if strcmp(name, "Nose") == 0: return "Change the nose shape."
    if strcmp(name, "Mouth") == 0: return "Change the mouth shape."
    if strcmp(name, "Job") == 0: return "Change the job."
    if strcmp(name, "Align") == 0: return "Change the alignment."
    if strcmp(name, "Done") == 0: return "Embark on your mission!"
    return ""

static def com_name(Menu *menu, char const *command):
    """
    
    0 1 2 3
    _ _ _ 0
    
    """
    int k, u;
    if not land_keybuffer_empty():
        char *name = char_name
        int s = sizeof(char_name) - 2
        
        land_keybuffer_next(&k, &u);
        
        if k == LandKeyLeft:
            if cursor_pos > 0: cursor_pos--
        elif k == LandKeyRight:
            if cursor_pos < s and name[cursor_pos]: cursor_pos++
        elif u == 8:
            if cursor_pos > 0:
                cursor_pos--
                memmove(name + cursor_pos, name + cursor_pos + 1,
                    s - cursor_pos + 1)
        elif u == 127:
            memmove(name + cursor_pos, name + cursor_pos + 1,
                s - cursor_pos + 1)            
        elif u >= 32 and u <= 127:
            memmove(name + cursor_pos + 1, name + cursor_pos,
                s - cursor_pos)
            name[cursor_pos] = u
            if cursor_pos < s: cursor_pos++

static def com_change(Menu *menu, char const *command):
    int d = 0

    if land_key_pressed(LandKeyLeft):
        d = -1
    
    if land_key_pressed(LandKeyRight):
        d = 1
    
    if land_key_pressed(LandKeyEnter):
        d = 1
    
    if not d: return
    
    if strcmp(menu->name, "Job") == 0:
        profession += 7 + d
        profession %= 7
    
    if strcmp(menu->name, "Align") == 0:
        alignment += 9 + d
        alignment %= 9

static def com_start(Menu *menu, char const *command):
    if land_key_pressed(LandKeyEnter):
        area_enter()

def charsel_enter():
    state = "charsel"
    
    for int i in range(5):
        if charsel_portrait[i] == 0:
            select_next(i, 1)

    menu_root()
    menu_pos(1, 1, 2)
    menu_focus(menu_add("Name", com_name))
    menu_add("Face", com_select)
    menu_add("Hair", com_select)
    menu_add("Eyes", com_select)
    menu_add("Nose", com_select)
    menu_add("Mouth", com_select)
    menu_add("Job", com_change)
    #menu_add("Align", com_change)
    menu_add("Done", com_start)

def charsel_tick():
    if land_key_pressed(LandKeyEscape):
        title_enter()
        return

def charsel_draw_portrait(int px, py, int *portrait):
    for int p in range(5):
        for int j in range(12):
            for int i in range(20):
                char c = portraits[portrait[p]][i + j * 20]
                if p == 0 or c != ' ':
                    if c == 'e': c = ' '
                    screen[px + i + (py + j) * 80] = c

def charsel_render():
    memset(screen, 0, 80 * 25)

    int x = 10
    int y = 0
    int right = 55
    int bottom = 18
    
    rect(x, y, right, bottom)
    
    text(x + 1, y + 1, organizations[profession])
    
    int px = x + 1
    int py = y + 2
    charsel_draw_portrait(px, py, charsel_portrait)

    #memcpy(screen + 1 + 14 * 80, portraits[charsel_portrait[part_sel]] + 12 * 20, 20)
    text(1, 24, get_help(menu_get_focus()))

    px = x + 1
    py = bottom - 2
    text(px, py - 1, "%s", titles[profession])
    text(px, py, "%s", char_name)
    text(px, py + 1, "%s", jobs[profession])
    
    if strcmp(menu_get_focus(), "Name") == 0:
        if land_get_ticks() % 60 < 30:
            screen[py * 80 + px + cursor_pos] = '_'

    char const *s = "Washington, D.C."
    text(right - strlen(s), bottom - 1, s)

    s = "Pentagon"
    text(right - strlen(s), y + 1, s)

    px = x + 21
    py = y + 3
    char const *s2 = logos[profession]
    for int i in range((int)strlen(s2)):
        blit(screen, 80, px + i * 8, py,
            font_glyphs[(int)s2[i]], 10, 1, 1, 7, 13)

    #px = right + 2
    #py = 1
    #for int aj in range(3):
    #    int px2 = px
    #    for int ai in range(3):            
    #        if aj * 3 + ai == alignment:
    #            text(px2, py + aj * 3, alignments[alignment])
    #        else:
    #            text(px2, py + aj * 3, "[]")
    #        px2 += 3
    #        if ai == alignment % 3: px2 += 12

    #int py2 = py + 9
    #if alignment < 3:
    #    text(px, py2++, "- may only kill evil")
    
    #if alignment % 3 == 0:
    #    text(px, py2++, "- cannot commit crimes")
    
    #if alignment % 3 == 2:
    #    text(px, py2++, "- can join the cult")

char const *def charsel_name():
    return char_name

char const *def charsel_profession():
    return jobs[profession]
