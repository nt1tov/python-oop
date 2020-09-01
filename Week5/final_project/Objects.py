from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine):
        pass

class AbstractObject(ABC):
    def __init_(self):
        pass
    
    def draw(self, display):
        pass

class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine):
        self.action(engine)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

  

    def draw(self,  surf):
        self.sprite_size = surf.game_engine.sprite_size
        surf.blit(self.sprite, (self.position[0] * self.sprite_size, self.position[1]*self.sprite_size))


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
    
    def draw(self,  surf, pos):
        self.sprite_size = surf.game_engine.sprite_size
        surf.blit(self.sprite, (pos[0] * self.sprite_size, pos[1]*self.sprite_size))

    def calc_damage(self):
        return (self.stats["strength"]  + self.stats["intelligence"]//2 + self.stats["luck"]//4) * self.level


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.hp = xp
        self.level =  stats['experience'] // 100
        self.exp = stats['experience']
        self.gold = stats['experience'] // 10

    # FIXME
    #@abstractmethod
    def interact(self, engine):
        self.hp = max(0, self.hp - engine.hero.calc_damage())
        engine.hero.hp =  max(0,  engine.hero.hp - self.calc_damage())
        if engine.hero.hp > 0:
            engine.hero.exp += self.exp

    def calc_damage(self):
        return self.stats["strength"]  + self.stats["intelligence"]//2 + self.stats["luck"]//4

        

# class Rat(Enemy):
#     pass

# class Knight(Enemy):
#     pass

# class Naga(Enemy):
#     pass

# class Dragon(Enemy):
#     pass


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 7
        self.stats['endurance'] += 7
        self.stats['luck'] += 7
        self.stats['intelligence'] -= 3


class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 2
        self.stats['endurance'] += 2
        self.stats['luck'] += 2
        self.stats['intelligence'] += 2


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 4
        self.stats['endurance'] -= 4

# FIXME
# add classes