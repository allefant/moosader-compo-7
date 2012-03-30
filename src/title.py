static import menu

def title_enter():
    state = "title"
    menu_root()
    
    menu_pos(65, 10, 3)
    menu_add("New Game", com_new_game)
    menu_focus(menu_add("Continue", com_continue))
    menu_add("Quit", com_quit)

def title_tick():
    if land_key_pressed(LandKeyEscape):
        land_quit()

def title_render():
    memcpy(screen, title, 80 * 25)

***scramble
x = r"""
                                                                              
                            _                                                   
                           / \               __-----                           
                          | \ \             /   _-_ |                           
                          | |  \_---------_/   |    |                           
                          |    _/              /    /                           
                      ____ \  / __   __       |    |                            
                     /    \ \_| U    U __          /                            
                    /   __ \__\   ____/ /|   ------    _--                     
                   /   /  \      _\______|  _/|       |   |                     
                   \__/    \    / \_      _/  |       /  /                      
                    --_     \__/  | \____/    |   ___/  |                       
                   |  |          /|           |__/ ____/                        
                    \ \_________/ |           |___/                             
                     \___________/|           |                                 
                                  |           |                                 
                                  /           |                                 
                                 /            /                                 
                                                                                
                              A N T A R C T I C A                               
                                                                                
                                Moosader compo 7                                
                                    entry by                                    
                                    Allefant                                    
                                                                                
"""
x2 = ""
for row in x.split("\n")[1:]:
    x2 += row + " " * (80 - len(row))
x = x2
x = x.replace("\\", "\\\\")
parse('global char const *title = "%s"' % x)
***
