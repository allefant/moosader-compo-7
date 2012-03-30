***scramble
story = """
It's the spring of 2045. The hippy rebellion has been going on for over 33 years
by now. Now, finally, the US government has hired you to put an end to the hippy
movement. Assemble a team, go to Antarctica and defeat their leader.

Intro:

You choose your name and appearance and attributes by filling out an ID card.

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
Foes: car

-> exit to Canada
-> exit to Mexico

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



"""[1:]
x = story
x = x.replace("\"", "\\\"")
x = x.replace("\n", "\\n")
parse("char const *story = \"" + x + "\"")
***
