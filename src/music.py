import main
import sound

static LandSound *notes[128][16]
static char const *tune = """
    A2^A2B2c3d1c6 A2^A2B2c3d1c6 f2c2A2F2F2E1G5 ^A2G2G2E1F9  z8
"""
static int pos = 0
static int tick_pos = 0
static int next_tick_pos = 0

int noteval[7] = {0, 2, -9, -7, -5, -4, -2}

def play_note(Envelope *e):
    int note = 0
    int duration = 0
    int octave = 0
    bool divide = False
    int divisor = 1
    int half = 0
    
    while True:
        int c = tune[pos]
        if not c:
            pos = 0
            c = tune[pos]

        if c >= 'A' and c <= 'G':
            if note: break
            c -= 'A'
            note = 69 + noteval[c]
        elif c >= 'a' and c <= 'g':
            if note: break
            c -= 'a'
            note = 69 + noteval[c] + 12
        elif c == 'z':
            if note: break
            note = 128
        elif c == '^':
            if note: break
            half = 1
        elif c == '_':
            if note: break
            half = -1
        elif c == ',':
            octave--
        elif c == '\'':
            octave++
        elif c >= '0' and c <= '9':
            if divide: divisor = c - '0'
            else:
                duration *= 10
                duration += c - '0'
        elif c == '/':
            divide = True

        pos++
    
    if not duration: duration = 1

    next_tick_pos = tick_pos + 8 * duration / divisor
    
    if note < 128:
        note += octave * 12 + half
        if not notes[note][duration]:
            e->hold = 8 * duration / 60.0 - e->attack - e->decay
            notes[note][duration] = sound_synthesize(e, note)
    
        land_sound_play(notes[note][duration], 1, 0, 1)

def music_tick():
    
    Envelope e = {
        .attack = 0.025,
        .decay = 0.025,
        .hold = 0,
        .release = 0.025,
        .volume = 0.75,
        .sustain = 0.4}
    
    if tick_pos == next_tick_pos:
        play_note(&e)

    tick_pos++
