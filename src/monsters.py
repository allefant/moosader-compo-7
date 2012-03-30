***scramble

import sys; sys.path.append("src")
from parse_utils import *

rows = []
for row in r"""
                           
                          \
                           \
                            \
                             \
                              \
                               \             
         ________              |              \
        /        \             |     ____      \         
       |  _    _  |            |    /    \     |   ____   \         \
       | (_)  (_) |            |   | O  O |    |  |.  .|  |   __     |
       |    __    |            |    \____/     |  |____|  |  |__|    |
        \________/             |    _,'',_     |    ''    |   /\     |
         __|  |__              |   /|    |\    |  /|  |\  |   \/     |
        /        \             |  / |____| \   |   |__|   |   ||     |
       /          \            |     |´ |      |   |´ |   |          |
      /            \           |     |´ |      |   |´ |   /         /
     / /|        |\ \          |     |´ |      /
    / /´|  ____  |´\ \         |              /
   / |´ | |´   | |´ | \        /
   \_/´ | |´   | |´ \_/       /
        | |´   | |           /
        | |´   | |          /
        | |´   | |         /
        /_\´   /_\        /
 /\  ________________  /\    
/  \/                \/  \\
\  /                  \  / \
 \ |                  | /   \
  \|    __/    \__    |/     \
   |   (__)    (__)   |       \
   |                  |        \   ________   
  / \                / \       |/\/        \/\\
 /   \_            _/   \      |\ |        | / \   ____           
/      \_        _/      \     | \|  O  O  |/  |/\/    \/\\   __    \
|        \      /        |     | /\_      _/\  |\ |.  .| /|/\/  \/\  |
|         |    |         |     ||   \    /   | |/\|    |/\|\| .. |/  |
|         |    |         |     ||    \  /    | ||  \  /  ||/ \  / \  |
|         |    |         |     ||     ||     | ||   \/   |||  \/  |  |
|         | __ |         |     ||     \/     | |\   __   /|\ ____ /  |
|         |/  \|         |     | \    __    /  | | /  \ | |/_\  /_\  |
|         |\__/|         |     | |   /  \   |  |/__\  /__\/         /
|          \__/          |     | |  |    |  |  /
|                        |     |/____\  /____\/
 \          __          /     /
 |         /´ \         |     /
 |        |´   |        |    /
 |        |´   |        |   /
 |        |´   |        |  /
/_________\´   /_________\/
 __________ 26 __________   
|                        |\
|                        |e\
|                        |ee\
|                        |eee\
|                        |eeee\
|                        |eeeee\ ____ 14 ____
|                        |eeeee||            |\
|                        |eeeee||            |e\ __ 10 __          
|                        |eeeee||            |e||        |\ _  8 _ e\
|                        |eeeee||            |e||        |||      |ee|
|                        |eeeee||            |e||        |||      |ee|
25                      25eeeee|13          13e|9        9|7      7ee|
|                        |eeeee||            |e||        |||      |ee|
|                        |eeeee||            |e||        |||      |ee|
|                        |eeeee||            |e||        |||_  8 _|ee|
|                        |eeeee||            |e||__ 10 __|/        e/
|                        |eeeee||            |e/                   
|                        |eeeee||____ 14 ____|/
|                        |eeeee/
|                        |eeee/
|                        |eee/
|                        |ee/
|                        |e/
|__________ 26 __________|/
"""[1:].splitlines():
    row = row.rstrip()
    row += " " * (80 - len(row))
    rows += [row.replace("´", chr(0))]

def trans(row):
    splits = [0, 26, 32, 46, 48, 58, 59, 67, 70, 80]
    newrow = ""
    a = splits[0]
    for b in splits:
        newrow += trans_part(row[a:b])
        a = b
    return newrow

for i in range(len(rows) // 25):
    parse("\nglobal char const *monster%d = " % i)

    for row in rows[i * 25:i * 25 + 25]:
        row = trans(row)
        parse('    "' + row.replace("\\", "\\\\") + '"')

    for row in rows[i * 25:i * 25 + 25]:
        row = trans(row)
        row = ["\\" if x == "/" else "/" if x == "\\" else x for x in row]
        parse('    "' + "".join(row).replace("\\", "\\\\") + '"')
***
