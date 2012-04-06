static import main

global char const *story = """
It's the spring of 2045.

The hippy rebellion has
been going on for over 33
years by now.

Finally, the US government
has hired you to put an
end to the hippy movement.

Assemble a team, go to
Antarctica and defeat
their leader.







"""

def story_render(char const *text):
    int x = 27
    int y = 1
    char const *pos = text + 1
    for int i in range(20):
        int j = 0
        while *pos and *pos != '\n':
            screen[y * 80 + x] = *pos
            x++
            pos++
            j++
        while j < 26:
            screen[y * 80 + x] = ' '
            x++
            j++
        if not *pos: break
        pos++
        y++
        x = 27

***scramble
story = """

Intro:

Your stats:

Strength:
    100% attack with melee weapons
    50% defense against melee weaons
    50% defense against magic weapons
    25% defense against ranged weapons

Dexterity
    100% attack with ranged
    50% defense against melee
    50% defense against ranged

Intelligence
    100% attack with magic
    25% defense against ranged
    25% defense against magic

Max HP

Max MP


Rough Plot:
___
Washington DC, April 1st 2045

Plot: Your job is to assemble a team (or not) then figure out a way to reach
Antarctica.
Friends: tbd, a selection of about 10 maybe?
Foes: zombies at arlington graveyard

-> exit to Canada
-> exit to Mexico

quotes

CIA Agent: "Hi there, FBI! Forgot we have no clearance here have we?"

Assistant Director: "It's gotten dark. Avoid walking through Arlington because
of teh Zombies."

___
Canada, April 2nd 2045

You reach Canada.

Plot: Get to Antarctica
Friends: The Canadian Moose
Foes: Crazy hippy mooses, grisly hippy grizzly bears

-> return to DC
-> head on to the arctis on the USS Nautilus

___
Mexico, April 2nd 2045

You reach Mexico.

Plot: Get to Antarctica
Friends: tbd
Foes: tbd

- bord a ship bound to Antarctica
- bord a plane bound to Antarctica

___
Atlantic, April 3nd 2045

On the ship.

Plot: Get to Antarctica
Friends: tbd
Foes: tbd

- arrive on Antarctica

___
Antarctica, McMurdo station

You arrive on a coastal outpost, either by ship or plane.

Plot: Get to Antarctica
Friends: tbd
Foes: tbd

By now your team should be fully assembled, there won't be any further
recruitable characters.

- return to DC by plane
- travel to the hippy camp

___
Antarctica, hippy camp

Finally the game starts.

Friends: none
Foes: hippies

- return to McMurdo
- enter the dungeons

___
Antarctica, hippy dungeons

With your full (or not) party you now fight through the hippy dungeons to get
stronger and finally face the Allefant.



"""
***

