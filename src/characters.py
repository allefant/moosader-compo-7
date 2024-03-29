***scramble

import sys; sys.path.append("src")
from parse_utils import *

rows = []
for row in r'''
/\_              _/\
\_ \_          _/ _/
  \_ \_      _/ _/ 
    \_ \____/ _/       
      \_    _/
        \  /
       _/  \_
     _/ ____ \_      
   _/ _/    \_ \_ 
 _/ _/        \_ \_
/ _/            \_ \
\/                \/
example
####################

     _________
    /         \             
   /           \   
  /             \   
 |   _       _   | 
 |  (_)     (_)  | 
 |               | 
  \      _      / 
   \     _     /
    \_________/   
       |   |   
example
####################

   _____________
  /             \
 /               \ 
X                 X
/  _____________  \
\ / (_)     (_) \ /
/ \             / \
\ /      _      \ /
/ \\    ___    // \
\ / \_________/ \ /
/ \    |   |    / \
example
####################

   _____________
  /             \
 /               \
|  /VVVVVVVVVVV\  |
| / ___     ___ \ |
| | (_)     (_) | |
| |             | |
| |      _      | |
| |\     _     /| |
VVV \_________/ VVV  
       |   |   
example
####################

    ___________
   /           \ 
  / ___________ \
 / /           \ \  
 |/ ___     ___ \|
  | (_)     (_) |
  |      |      | 
  |             |
   \    ___    / 
    \_________/   
       |   |      
example
####################

     
    ___________
   /           \
  /  __     __  \  
 _| /  \_ _/  \ |_
 \  (_)     (_)  /
  |     /_\     | 
  /             \
  \   / ___ \   / 
   \___________/   
      |     |      
example
####################

   _____________
  /             \
 /               \
|  /VVVVVVVVVVV\  |
| /___       ___\ |
| |\__)     (__/| |
| |             | |
| |     _ _     | |
| |\    ___    /| |
VVV \_________/ VVV  
       |   |   
example
####################

     _________
   _/         \_             
  /_/\_______/\_\   
 //             \\   
/|               |\ 
|| [ o ]   [ o ] ||
\|      / \      |/ 
  \    (. .)    / 
   \    ___    /
    \_________/   
       |   |   
example
####################

     _________
    /         \             
   /           \   
  /             \   
 |               | 
(|               |) 
 |               | 
  \             / 
   \           /
    \_________/   
       |   |   
face normal
####################

     _________
    /         \
   /           \
  /             \  
 _|             |_
 \               /
  |             | 
  /             \
  \             / 
   \___________/   
      |     | 
face bumpy
####################

    ___________
   /           \
  /             \   
 |               |   
 |               | 
[|               |] 
 |               | 
 |               | 
 |               |
  \_____________/  
       |   |   
face square
####################

     _________
    /         \             
   /           \   
  /             \   
 |               | 
(|               |) 
 "               " 
  "             " 
   """""   """""
    """""""""""   
       """""   
face bearded
####################

    ___________
   /           \             
  /             \   
 |               |   
 |               | 
(|               |) 
 "               " 
 "               "
 """""""""""""""""
 """"""""""""""""" 
   """""""""""""
face big bearded
####################

    ___________
   /           \ 
  / ___________ \
 / /´          \ \  
 |/´            \|





     
hair short
####################

   _____________
  /             \
 /               \
|  /VVVVVVVVVVV\  |
| /´            \ |
| |´            | |
| |´            | |
| |´            | |
| |´            | |
VVV´            VVV  
               
hair fringe
####################

    ___________
   /           \ 
  /             \
 /               \  
 \_______________/





     
hair page
####################
     
    ||||||||||| 
   |           |
  | ___________ |
 | /´          \ |  
 |/´            \|
                
                  



     
hair standing
####################
     _________
    |         |
    |_________|
   
   
   
                   
                  



     
hair weird
####################

   _____________
  /             \
 /               \ 
X                 X
/  _____________  \
\ /´            \ /
/ \´            / \
\ /´            \ /
/ \´            / \
\ /´            \ /
/ \´            / \
hair curls
####################











    
hair bald
####################

    e_________e
   _/         \_             
  /_/\_______/\_\   
 //´            \\   
/|´              |\ 
||´              ||
\|´              |/ 
                  
                
                  
          
hair medium
####################

   _____________
  /             \
 /               \
|                 |  
|    ___  ______  |
|   /´  |/´     | |
|  /´   '´      | /
| /´            |/ 
|/´             ' 
'                  
                  
hair left
####################

   _____________
  /             \
 /               \ 
/                 \
|  _____________  |
| /´            \ |
| |´            | |
| |´            | |
|´                |
|´                |
|´                |
hair long
####################

    _____ _____
   /     |     \
  / _____|_____ \ 
 | /´          \ |
 |/´            \|
                   
                   
                   
                   
                   
                   
hair parted
####################
  /\  /\   /\  /\
  \ \_\ \_/ /_/ /
/\ \           / /\
\ \/ /\/\_/\/\ \/ / 
 \  /´        \  /
 / /´          \ \
 \/´            \/   
                   
                   
                   
                   
                   
hair wild
####################

   ______ ______
  /      |      \
 /  _____|_____  \ 
/  /´          \  \
| /´            \ |
| |´            | |
| |´            | |
| |´            | |
|´                |
|´                |
|´                |
hair parted long
####################
     ,-------,
   __\       /__
  /   '-----'   \
 /   __     __   \ 
/   /´/_____\´\   \
|  /´          \  |
| |´            | |
| |´            | |
| |´            | |
|´                |
|´                |
|´                |
hair tuft
####################

   _____________
  /             \
 /   _________   \ 
/   /´        \   \
|  /´          \  |
| |´            | |
| |´            | |
 \|´            |/ 
                   
                   
                   
hair middle
####################

   _____________
  /             \
 /               \ 
/   ____/\_____   \
|  /´          \  |
| |´            | |
| |´            | |
 \|´            |/ 
                   
                   
                   
hair middle cut
####################
     .-------.
   _/_________\_
  /             \
 /  ___________  \ 
/  /´          \  \
\ /´            \ /
/ \´            / \
\ /´            \ /
/ \´            / \
\ /´            \ /
/ \´            / \
\ /´            \ /
hair pony
####################




  
    ___´    ___    
    (_)´    (_)    

                   
       
       
       
eyes plain
####################





   ___´      ___   
    \_)´    (_/





eyes asian
####################





   ____´    ____   
     o ´     o      





eyes stare
####################





   ___´      ___   
   \__)´    (__/





eyes alien
####################




     __     __     
    /  \_´_/  \   
    (_)´    (_)   
    
    
    
    
    
eyes gorilla
####################




  
    ___´    ___
   [___]´  [___]

                   
       
       
       
eyes spectacles
####################




  
     _´      _     
    (_)´    (_)    

                   
       
       
       
eyes small
####################




  
                   
    ___´    ___

                   
       
       
       
eyes shut
####################




  
    \|/´    \|/
    (_)´    (_)      
              
                   
       
       
       
eyes star
####################




  
    ___´    ___           
     $´      $
              
                   
       
       
       
eyes $$
####################








         _
          


nose small
####################







         | 
            
          


nose straight
####################








         |
          


nose hawk
####################







           
       (. .)
             


nose round
####################







        / \
       (. .)
             


nose big
####################






         |
         | 
         |   
          


nose long
####################






        |e|
        |e|
        |e| 
          


nose horse
####################









        ___


mouth normal
####################









         _


mouth small
####################









      / ___ \


mouth wrinkle
####################









       _____  
       \___/

mouth laugh
####################









       \___/  
       

mouth smirk
####################









        === 
       

mouth tight lips
####################









        O   
       

mouth whistle left
####################









         O   
       

mouth whistle
####################









          O   
       

mouth whistle right
####################









        ___   
       /___\

mouth angry
####################









       """""
       "---"
       """""
mouth goatee
####################








    "         " 
     """"_""""
            
            
mouth moustache
####################
'''[1:].splitlines():
    row = row.rstrip()
    row += " " * (20 - len(row))
    rows += [row.replace("´", chr(0))]

parse("\nglobal char const *portraits[] = {")
n = len(rows) // 14
for i in range(n):
    for j, row in enumerate(rows[i * 14:i * 14 + 13]):
        if j < 12:
            row2 = trans_part(row)
        else:
            row2 = row

        parse('    "' + row2.replace("\\", "\\\\").replace('"', '\\"') + '"')
    parse(",")
parse("}\n")
parse("global int const characters_count = " + str(n))
***
