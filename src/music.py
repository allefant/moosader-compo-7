import main
import sound

static LandSound *samples[128][64]

class Note:
    int timestamp
    int note
    int ticks
    int next_index
    int prev_index

class NotesPlayer:
    int sample_pos
    int last_note
    int first_note
    int highest_index
    int oldest_active_note
    Note notes[8192]

class ABCParser:
    char const *tune
    int pos
    int repeat_start_pos
    bool repeating
    
    int ticks64
    
    int timestamp

    int key_note
    int key_scale
    int chord_note
    int chord_type
    
    int chord_tick
    
    int note_numerator
    int note_denominator
    
    int meter_numerator
    int meter_denominator
    
    NotesPlayer *player

static NotesPlayer global_player
static char const *current_tune

global char const *music_tune1 = """
X: 0
T: Allefant Song
M: 2/4
L: 1/8
K: Am
|: "Am"A2^A2B2 "F" c3d1c4z2 | "Am"A2^A2B2 "F" c3d1c4z2 | "F" f2c2A2F2 "C"  F2E1G3z2 | "C" ^A2G2G2 "F" E1 F7z2 :|
|: "C" E2 G2 c1 "F" x1 B4 A2 F2 z2 | "Bdim" D2F2B2 "C" A4G2E2 z2 :|
"""

global char const *music_tune2 = """
X: 0
T: Katyusha
M: 2/4
L: 1/8
K: Am
[| "Am"A3 B | c3 A | cc BA | "E7"B2 E2 | B3 c | d3 B | dd cB | "Am"A4 ||
|: "Am"e2 "F"a2 | "C"g2 "A7"ag | "Dm"ff ed | "Am"e2 A2 | "Dm"zf2 d | "Am"e3 c | "E7"BE cB | "Am"A4 :|
K: Em
[| "Em"E3 F | G3 E | GG FE | "B7"F2 B,2 | F3 G | A3 F | AA GF | "Em"E4 ||
|: "Em"B2 "C"e2 | "G"d2 "E7"ed | "Am"cc BA | "Em"B2 E2 | "Am"zc2 A | "Em"B3 G | "B7"FB, GF | "Em"E4 :|
K: Gm
[| "Gm"G3 A | B3 G | BB AG | "D7"A2 D2 | A3 B | c3 A | cc BA | "Gm"G4 ||
|: "Gm"d2 "E"g2 | "B"f2 "G7"gf | "Cm"ee dc | "Gm"d2 G2 | "Cm"ze2 c | "Gm"d3 B | "D7"AD BA | "Gm"G4 :|
K: Dm
[| "Dm"D3 E | F3 D | FF ED | "A7"E2 A,2 | E3 F | G3 E | GG FE | "Dm"D4 ||
|: "Dm"A2 "B"d2 | "F"c2 "D7"dc | "Gm"BB AG | "Dm"A2 D2 | "Gm"zB2 G | "Dm"A3 F | "A7"EA, FE | "Dm"D4 :|
"""

static LandStream *stream

static int const notevals[2][7] = {
    {0, 2, 4, 5, 7, 9, 11},
    {0, 2, 3, 5, 7, 8, 10}}

int def noteval(int key, int scale, int note):
    """
    key: 0..6
    note: 0..6
    scale: 0: major
           1: minor
    """

    int table[8]
    int base = notevals[0][key]
    for int i in range(7):
        int j = (key + i) % 7
        table[j] = (base + notevals[scale][i]) % 12

    return table[note]

static def read_fraction(char const *s, int *num, *den):
    bool divide = False
    int l = strlen(s)
    for int i in range(l):
        int c = s[i]
        if c >= '0' and c <= '9':
            if divide: *den = c - '0'
            else: *num = c - '0'
        elif c == '/':
          divide = True

static char const *note_names[12] = {"C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B"}

static int chords[][5] = {
    {99},
    {0, 4, 7, 99}, # major
    {0, 3, 7, 99}, # minor
    {0, 4, 7, 10, 99}, # major 7th
    {0, 3, 6, 99}, # diminished
    }

char *def note_string(int note, char *out):
    out[0] = 0
    if note == 0:
        strcat(out, "-")
    elif note == 128:
        strcat(out, "z")
    else:
        int octave = note / 12
        note %= 12
        strcat(out, note_names[note])
        if octave < 5:
            for int i in range(5 - octave):
                strcat(out, ",")
        elif octave >= 6:
            out[strlen(out) - 1] += 'a' - 'A'
            
            for int i in range(7, octave):
                strcat(out, "'")    
    return out

static def note_add(NotesPlayer *player, int note, ticks, timestamp):
    int prev = player->last_note
    int i = player->highest_index++
    if i == 0:
        i++
        player->highest_index++
        if player->highest_index >= 8192:
            player->highest_index--
            printf("FIXME: music is fixed length right now!\n")

    if prev:
        while prev:
            if timestamp > player->notes[prev].timestamp: break
            prev = player->notes[prev].prev_index

    if prev:
        player->notes[i].prev_index = prev
        player->notes[i].next_index = player->notes[prev].next_index
        player->notes[prev].next_index = i
    else:
        player->notes[i].prev_index = 0
        player->notes[i].next_index = player->first_note
        player->first_note = i
    
    if player->notes[i].next_index:
        player->notes[player->notes[i].next_index].prev_index = i
    else:
        player->last_note = i

    player->notes[i].timestamp = timestamp
    player->notes[i].ticks = ticks
    player->notes[i].note = note
    
    #printf("%d <- %d -> %d (%d..%d)\n", notes[i].prev_index, i,
    #    notes[i].next_index, first_note, last_note)

static int def letter_to_note(int c):
    c -= 'C'
    if c < 0: c += 7
    return c

static def parse_note(ABCParser *abc):
    int note = 0
    int duration = 0
    int octave = 0
    bool divide = False
    int divisor = 1
    int half = 0
    bool string = False
    char stringval[100]

    while True:
        int c = abc->tune[abc->pos]

        if not c:
            break
        if c == '\n':
            break

        abc->pos++
        
        int next_c = abc->tune[abc->pos]

        if string:
            int s = strlen(stringval)
            if c == '"':
                abc->chord_note = letter_to_note(stringval[0])
                abc->chord_type = 1
                if s >= 2:
                    if stringval[1] == 'm':
                        abc->chord_type = 2
                    elif stringval[1] == '7':
                        abc->chord_type = 3
                    elif stringval[1] == 'd':
                        abc->chord_type = 4
                string = False
            else:
                stringval[s] = c
                stringval[s + 1] = 0
            continue
            
        if c == '"':
            stringval[0] = 0
            string = True
        elif c >= 'A' and c <= 'G':
            if note: abc->pos--; break
            note = 60 + noteval(abc->key_note, abc->key_scale,
                letter_to_note(c))
        elif c >= 'a' and c <= 'g':
            if note: abc->pos--; break
            note = 60 + noteval(abc->key_note, abc->key_scale,
                letter_to_note(c + 'C' - 'c')) + 12
        elif c == 'z':
            if note: abc->pos--; break
            note = 128
        elif c == 'x':
            if note: abc->pos--; break
            note = 128
        elif c == '^':
            if note: abc->pos--; break
            half = 1
        elif c == '_':
            if note: abc->pos--; break
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
        elif c == '|':
            if next_c == ':':
                #printf("repeat start\n")
                abc->pos++
                abc->repeat_start_pos = abc->pos
        elif c == ':':
            if next_c == '|':
                if abc->repeating:
                    abc->pos++
                    abc->repeating = False
                else:
                    #printf("repeating\n")
                    abc->pos = abc->repeat_start_pos
                    abc->repeating = True
    
    if not duration: duration = 1
    
    int ticks = abc->ticks64 * 64 * abc->note_numerator * duration
    ticks /= divisor * abc->note_denominator
    
    if note < 128:
        note += octave * 12 + half
        
        #char s[100]
        #printf("Note: %9d: %d %s%d\n", abc->timestamp, note, note_string(note, s), duration)
        
        note_add(abc->player, note, ticks, abc->timestamp)
        
    if abc->chord_type:
        
        int chord_span = abc->ticks64 * 64 * abc->meter_numerator / abc->meter_denominator / 2

        while abc->chord_tick < abc->timestamp + ticks:
        
            int i = 0
            int chord_octave = 4
            int base = chord_octave * 12 + notevals[0][abc->chord_note]

            note_add(abc->player, base + chords[abc->chord_type][0] - 12, chord_span / 4,
                    abc->chord_tick)
            
            while chords[abc->chord_type][i] != 99:
                note_add(abc->player, base + chords[abc->chord_type][i], chord_span / 4,
                    abc->chord_tick + chord_span / 2)
                i++

            abc->chord_tick += chord_span
    
    abc->timestamp += ticks

static def parse_notes(ABCParser *abc):
    while True:
        char c = abc->tune[abc->pos]
        if not c: break
        if c == '\n': break
        parse_note(abc)

def music_parse_abc(char const *tune, NotesPlayer *player):
    int tag = 0
    int const OUTSIDE = 0
    int const INSIDE = 1
    int const COMMENT = 2
    int mode = OUTSIDE
    char line[1024]

    ABCParser abc_
    ABCParser *abc = &abc_
    abc->player = player
    abc->pos = 0
    abc->tune = tune
    abc->timestamp = 0
    abc->key_note = 0
    abc->key_scale = 0
    abc->chord_note = 0
    abc->chord_type = 0
    abc->note_numerator = 1
    abc->note_denominator = 8
    abc->chord_tick = 0
    abc->repeat_start_pos = 0
    abc->repeating = False
    abc->ticks64 = 1500
    abc->meter_numerator = 2
    abc->meter_denominator = 4

    while True:
        char c = abc->tune[abc->pos++]
        if not c: break
        if mode == OUTSIDE:
            if c <= 32: continue
            if c == '%':
                mode = COMMENT
                continue

            if tune[abc->pos] == ':':
                if (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
                    abc->pos++
                    tag = c
                    mode = INSIDE
                    line[0] = 0
                    continue

            #timestamp_start = timestamp
            abc->pos--
            parse_notes(abc)
            #timestamp_end = timestamp
            #timestamp = timestamp_start
            
        elif mode == INSIDE:
            int s = strlen(line)
            if c == '\n':
                mode = OUTSIDE
                if tag == 'K':
                    abc->key_note = 0
                    abc->key_scale = 0
                    #printf("K:%s\n", line)
                    #timestamp = timestamp_end
                    for int i in range(s):
                        if line[i] >= 'A' and line[i] <= 'G':
                            abc->key_note = letter_to_note(line[i])
                        if line[i] == 'm':
                            abc->key_scale = 1
                elif tag == 'L':
                    read_fraction(line, &abc->note_numerator,
                        &abc->note_denominator)
                    #printf("L:%s %d/%d\n", line, abc->note_numerator, abc->note_denominator)
                elif tag == 'M':
                    read_fraction(line, &abc->meter_numerator,
                        &abc->meter_denominator)
                    #printf("M:%s %d/%d\n", line, abc->meter_numerator, abc->meter_denominator)
            else:
                line[s] = c
                line[s + 1] = 0
        elif mode == COMMENT:
            if c == '\n':
                mode = OUTSIDE

int def timestamp_to_samples(int ticks):
    return ticks

int def mix_note(NotesPlayer *player, Envelope *e, Note *note, int16_t *b, int count):
    
    if not samples[note->note][note->ticks / 750]:
        e->hold = note->ticks / 750 / 64.0 - e->attack - e->decay
        samples[note->note][note->ticks / 750] = sound_synthesize(e, note->note)
        
    LandSound *sample = samples[note->note][note->ticks / 750]

    int start = timestamp_to_samples(note->timestamp)
    int n = land_sound_length(sample)

    if start >= player->sample_pos + count: return 1
    if player->sample_pos >= start + n: return -1

    int16_t *s = land_sound_sample_pointer(sample)
    
    if start + n > player->sample_pos + count:
        n = player->sample_pos + count - start
    
    if start < player->sample_pos:
        n += start - player->sample_pos
        s += (player->sample_pos - start) * 2
        start = player->sample_pos

    if player->sample_pos < start:
        b += (start - player->sample_pos) * 2

    macro mix(a, b):
        v = a + b
        if v < -32768: v = -32768
        if v > 32767: v = 32767
        a = v

    for int i in range(n):
        int v
        mix(b[i * 2 + 0], s[i * 2 + 0])
        mix(b[i * 2 + 1], s[i * 2 + 1])
    
    return 0
    
def music_play_tune(char const *tune):
    NotesPlayer *player = &global_player
    
    player->highest_index = 0
    player->first_note = 0
    player->last_note = 0
    music_parse_abc(tune, player)
    current_tune = tune
    player->oldest_active_note = player->first_note
    player->sample_pos = 0

def music_tick():

    NotesPlayer *player = &global_player
    
    if not current_tune: return
    
    if not stream:
        stream = land_stream_new(8192, 4, 48000, 16, 2)

    int16_t *b = land_stream_buffer(stream)
    if not b: return

    memset(b, 0, 8192 * 4)
    #for int i in range(4096):
    #    int c = sin(((sample_pos + i) / 48000.0) * 440.0 * LAND_PI * 2) * 32767
    #    b[i * 2 + 0] = c / 2
    #    b[i * 2 + 1] = c / 2

    if not player->oldest_active_note:
        player->oldest_active_note = player->first_note
        player->sample_pos = 0

    Envelope e = {
        .attack = 0.025,
        .decay = 0.025,
        .hold = 0,
        .release = 0.025,
        .volume = 0.2,
        .sustain = 0.1}
    
    int ni = player->oldest_active_note
    while True:            
        Note *n = player->notes + ni
        if n->note > 0 and n->note < 128:
            int r = mix_note(player, &e, n, b, 8192)
            if r == 1: break
            if r == -1 and ni == player->oldest_active_note:
                player->oldest_active_note = n->next_index
        ni = n->next_index
        if not ni:
            
            break
        n = player->notes + ni


    land_stream_fill(stream)

    player->sample_pos += 8192
    
