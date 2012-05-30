import main

enum ControllerFlags:
    TurnLeft
    TurnRight
    MoveForward
    MoveBackward
    MoveLeft
    MoveRight
    TurnMoveNorth
    TurnMoveSouth
    TurnMoveWest
    TurnMoveEast
    StrafeModifier
    
    Interact

    ControllerFlagsCount

class Control:
    int key
    bool is_active
    bool is_modifier

static Control mapping[ControllerFlagsCount][4]

static def newkey(int flag, key):
    for int i in range(4):
        if not mapping[flag][i].is_active:
            mapping[flag][i].is_active = True
            mapping[flag][i].key = key
            return

static def newkeymod(int flag, key):
    for int i in range(4):
        if not mapping[flag][i].is_active:
            mapping[flag][i].is_active = True
            mapping[flag][i].key = key
            mapping[flag][i].is_modifier = true
            return

def controls_init():
    memset(mapping, 0, sizeof mapping)
    newkey(TurnLeft, LandKeyLeft)
    newkey(TurnLeft, 'q')
    newkey(TurnRight, LandKeyRight)
    newkey(TurnRight, 'e')
    newkey(MoveForward, LandKeyUp)
    newkey(MoveForward, 'w')
    newkey(MoveBackward, LandKeyDown)
    newkey(MoveBackward, 's')
    newkey(MoveLeft, 'a')
    newkey(MoveRight, 'd')
    newkey(TurnMoveNorth, LandKeyPad + 8)
    newkey(TurnMoveSouth, LandKeyPad + 2)
    newkey(TurnMoveWest, LandKeyPad + 4)
    newkey(TurnMoveEast, LandKeyPad + 6)
    newkeymod(StrafeModifier, LandKeyLeftShift)
    newkeymod(StrafeModifier, LandKeyRightShift)
    newkeymod(StrafeModifier, LandKeyLeftAlt)
    newkeymod(StrafeModifier, LandKeyRightAlt)
    
    newkey(Interact, LandKeyEnter)
    newkey(Interact, ' ')

int def controls_get_keymap():
    int keymap = 0
    for int i in range(ControllerFlagsCount):
        for int j in range(4):
            Control *c = &mapping[i][j]
            if not c->is_active: continue
            if c->is_modifier:
                if land_key(c->key): keymap |= 1 << i
            else:
                if land_key_pressed(c->key): keymap |= 1 << i
    return keymap
