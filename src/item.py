import main

class Item:
    char letter
    char const *name

global Item items[256]

def items_init():
    items[1].letter = 'o'
    items[1].name = "Easter Egg"
