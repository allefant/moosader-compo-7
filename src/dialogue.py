class Reply:
    char text[1024]
    char choices[4][10]
    int choice
    Dialogue *dialogue

import main, player
static import charsel, story, controls, render

global char const *npclist[] = {
    "CIA Secretary",
    "FBI Secretary",
    "NSA Secretary",
    "WTF Secretary",
    "CTU Secretary",
    "",
    "DHS Secretary",
    "Gun Specialist",
    "Guard",
    "",
    }

class Dialogue:
    char const *who
    int x
    int portrait[5]
    void (*cb)(Dialogue *, Reply *r)

static LandArray *dialogues

static Dialogue *def dialogue_add(char const *who,
        void (*cb)(Dialogue *, Reply *), char const *face, *hair, *eyes,
        *nose, *mouth):
    Dialogue *d; land_alloc(d)
    d->who = who
    d->cb = cb
    d->portrait[0] = charsel_get_part(face)
    d->portrait[1] = charsel_get_part(hair)
    d->portrait[2] = charsel_get_part(eyes)
    d->portrait[3] = charsel_get_part(nose)
    d->portrait[4] = charsel_get_part(mouth)
    land_array_add(dialogues, d)
    return d

static def guard_cb(Dialogue *d, Reply *r):
    sprintf(r->choices[0], "Bye")

    if d->x == 2:
        sprintf(r->text, """
I don't talk to you.
""")
        return

    if r->choice == 1:
        sprintf(r->text, """
Me? So you finally realize
that I'm not just the door
guard?

And you want me to join in
on a secret mission?

You won't regret this.
""")
        return
    
    if r->choice == 1:
        sprintf(r->text, """
Me? So you finally realize
that I'm not just the door
guard?

And you want me to join in
on a secret mission?

You won't regret this.
""")
        return
        
    if r->choice == 2:
        if d->x == 0:
            sprintf(r->text, """
Uh, what was that?
""")
            d->x = 1
        else:
            sprintf(r->text, """
Go die yourself :(
""")
            d->x = 2
        return
    
    if r->choice == 3:
        if d->x == 0:
            sprintf(r->text, """
You think you can insult
me just because I'm the
door guard?
""")
            
        return
    
    sprintf(r->choices[1], "Join")
    sprintf(r->choices[2], "Die")
    sprintf(r->choices[3], "Idiot")
    
    char const *name = the_game->monsters[the_game->player_id]->name;
    if strcmp(charsel_profession(), "Janitor") == 0:
        sprintf(r->text, """
Hey, you're not supposed
to use this entrance, you
are not an agent.
""")
    elif strcmp(charsel_profession(), "WTF") == 0:
        sprintf(r->text, """
Oh, it's you. The...
HA HA HA
the...
HA HA HA...
the... Wiki...

Sorry sir. Please enter,
agent %s.
""", name)
    else:
        sprintf(r->text, """
Ah, special agent
%s.
Good morning.
How are things going at
the %s?
""", name, charsel_profession())

static def secretary_cb(Dialogue *d, Reply *r):
    sprintf(r->choices[0], "Bye")
    sprintf(r->choices[1], "Join")

    char job[4]
    strncpy(job, d->who, 3)
    char const *p = charsel_profession()
    if strcmp(job, p) == 0:
        sprintf(r->text, """
Finally! There you are.

I assume you have been
informed about your new
orders.

You better get to the
airport soon.

""")
    elif strcmp(p, "Janitor") == 0:
        sprintf(r->text, """
Hey, I don't know you.

Aren't you the janitor?
""")
        sprintf(r->choices[1], "Yes")
        sprintf(r->choices[2], "No")
        sprintf(r->choices[3], "Maybe")
    else:
        sprintf(r->text, """
Hey, %s!

This is the %s, you don't
have clearance here!
""", p, job)

def dialogue_init():
    dialogues = land_array_new()
    
    dialogue_add("Guard", guard_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")

    dialogue_add("CIA Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")
    dialogue_add("FBI Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")
    dialogue_add("NSA Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")
    dialogue_add("WTF Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")
    dialogue_add("CTU Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")
    dialogue_add("DHS Secretary", secretary_cb,
        "face normal",
        "hair short",
        "eyes plain",
        "nose straight",
        "mouth goatee")

def dialogue_talk(int id, Reply *r):
    Player *m = the_game->monsters[id]
    int n = land_array_count(dialogues)
    for int i in range(n):
        Dialogue *d = land_array_get_nth(dialogues, i)
        if not strcmp(d->who, m->name):
            for int j in range(4):
                r->choices[j][0] = 0
            d->cb(d, r)
            r->dialogue = d
            r->choice = 0
            return

def dialogue_render(Reply *r):
    story_render(r->text)
    
    for int i in range(4):
        if r->choices[i][0]:
            text(28 + i * 6, 24, "%s%s",
                i == r->choice ? "*" : " ",
                r->choices[i])

    charsel_draw_portrait(1, 1, r->dialogue->portrait)

def dialogue_input(Player *self, int bits):
    
    Reply *r = &the_game->reply
    
    if bits & (1 << MoveLeft): r->choice--
    if bits & (1 << TurnLeft): r->choice--
    if bits & (1 << MoveRight): r->choice++
    if bits & (1 << TurnRight): r->choice++
    
    if r->choice < 0:
        r->choice += 4
    
    if r->choice >= 4:
        r->choice -= 4
    
    for int j in range(4):
        if r->choices[r->choice][0] == 0:
            r->choice++
            if r->choice == 4: r->choice = 0

    if bits & (1 << Interact):
        if r->choice == 0:
            the_game->state = "onwards"
        else:
            r->text[0] = 0
            dialogue_talk(self->focus, r)
