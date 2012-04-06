import main, player

float def monster_get_attack_points(Player *monster)
	float f = 2 ^ (monster->level / 5)
	return f

float def monster_get_defense_points(Player *monster)
	float f = 2 ^ (monster->level / 5)
	return f

float def monster_get_damage(Player *monster)
	float f = 2 ^ (monster->level / 5)
	return f * 2

def monster_attack(Player *monster, *other)
	float ap = monster_get_attack_points(monster)
	float dp = monster_get_defense_points(other)
	float p = ap / (ap + dp)
	float r = land_rnd(0, 1)
	if p > r:
		other->hp -= monster_get_damage(monster)

def monster_try_attack(Player *monster, *who)
    
    monster_attack(monster, who)
        

