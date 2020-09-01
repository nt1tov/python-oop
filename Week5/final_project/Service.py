import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size, angle=0):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    icon = pygame.transform.rotate(icon, angle)
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


def reload_game(engine):
    global level_list
    level_list_max = len(level_list) - 1
    if engine.is_dead:
        engine.is_dead = False
        restore_hp(engine)
    else:
        engine.level += 1
        generator = level_list[min(engine.level, level_list_max)]
        _map = generator['map'].get_map()
        engine.objects = []
        engine.load_map(_map)
        engine.add_objects(generator['obj'].get_objects(_map))
    engine.hero.position = [1, 1]
    
    #engine.add_hero(hero)
    return engine


def restore_hp(engine):
    engine.score += 0.1
    engine.hero.hp = engine.hero.max_hp
    engine.notify("HP restored")


def apply_blessing(engine):
    if engine.hero.gold >= int(20 * 1.5**engine.level) - 2 * engine.hero.stats["intelligence"]:
        engine.score += 0.2
        engine.hero.gold -= int(20 * 1.5**engine.level) - \
            2 * engine.hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(engine.hero)
            engine.notify("Blessing applied")
        else:
            engine.hero = Objects.Berserk(engine.hero)
            engine.notify("Berserk applied")
    else:
        engine.score -= 0.1


def remove_effect(engine):
    if engine.hero.gold >= int(10 * 1.5**engine.level) - 2 * engine.hero.stats["intelligence"] and "base" in dir(engine.hero):
        engine.hero.gold -= int(10 * 1.5**engine.level) - \
            2 * engine.hero.stats["intelligence"]
        engine.hero = engine.hero.base
        engine.hero.calc_max_HP()
        engine.notify("Effect removed")


def add_gold(engine):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(engine.hero)
        engine.notify("You were cursed")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
        engine.hero.gold += gold
        engine.notify(f"{gold} gold added")


class MapFactory(yaml.YAMLObject):
    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()

    @classmethod
    def from_yaml(cls, loader, node):
        _map = cls.get_map()
        _obj = cls.get_objects()

        # FIXME
        # get _map and _obj

        _obj.config = loader.construct_mapping(node)

        return {'map': _map, 'obj': _obj}


class EndMap(MapFactory):

    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else floor1
         
        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []
            self.config = {}

        def get_objects(self, _map):
            return self.objects


class EmptyMap(MapFactory):

    yaml_tag = "!empty_map"

    class Map:
        def __init__(self):

            #add map
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 7)]
         
        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []
            self.config = {}

        def get_objects(self, _map):

            prop = object_list_prob['objects']["stairs"]
            for i in range(random.randint(prop['min-count'], prop['max-count'])):
                coord = (random.randint(1, 39), random.randint(1, 39))
                intersect = True
                while intersect:
                    intersect = False
                    if _map[coord[1]][coord[0]] == wall:
                        intersect = True
                        coord = (random.randint(1, 39),
                                    random.randint(1, 39))
                        continue
                    for obj in self.objects:
                        if coord == obj.position or coord == (1, 1):
                            intersect = True
                            coord = (random.randint(1, 39),
                                        random.randint(1, 39))

                self.objects.append(Objects.Ally(
                    prop['sprite'], prop['action'], coord))

            return self.objects

class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []
            self.config = {}

        def get_objects(self, _map):

            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, 30), random.randint(1, 22))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects


class SpecialMap(MapFactory):

    yaml_tag = "!special_map"

    class Map:
        def __init__(self):
             #add map
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]
         
        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []
            self.config = {}

      
        def get_objects(self, _map):
            
            #add objects
            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))
            #add allys
            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))
                    self.objects.append(Objects.Ally(prop['sprite'], prop['action'], coord))
            #add enemys
            for obj_name in self.config:
                print(obj_name)
                prop = object_list_prob['enemies'][obj_name]
                for i in range(self.config[obj_name]):
                    coord = (random.randint(1, 30), random.randint(1, 22))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Enemy(prop['sprite'], prop, prop['experience'], coord))
            return self.objects

wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    angles = [0, 90, 180]
    floor_texture_pack = ["stone-ground"]

    wall[0] = create_sprite(os.path.join("texture", "wall-1.png"), sprite_size, angle=angles[random.randint(0, len(angles)-1)])
    floor1[0] = create_sprite(os.path.join("texture", "stone-ground-2.png"), sprite_size, angle=angles[random.randint(0, len(angles)-1)])
    floor2[0] = create_sprite(os.path.join("texture", "stone-ground-2.png"), sprite_size, angle=angles[random.randint(0, len(angles)-1)])
    floor3[0] = create_sprite(os.path.join("texture", "stone-ground-2.png"), sprite_size, angle=angles[random.randint(0, len(angles)-1)])

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read(), Loader=yaml.Loader)
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'][0] = create_sprite(os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'][0] = create_sprite(
            os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy]
        prop['sprite'][0] = create_sprite(os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read(), Loader=yaml.Loader)['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
