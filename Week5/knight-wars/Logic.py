import Service
import Objects

class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    sprite_size = None
    is_dead = False

    show_start = True

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero

    def interact(self):
        for obj in self.objects:
            if list(obj.position) == self.hero.position:
                
                if type(obj) != Objects.Enemy:
                    self.delete_object(obj)     
                    obj.interact(self)
                else:
                    obj.interact(self)
                    if obj.hp == 0:
                        self.delete_object(obj)
                    if self.hero.hp == 0:
                        self.notify("You are dead!!")
                        self.is_dead = True
                        self = Service.reload_game(self)

                #

    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] - 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] -= 1 
        self.interact()

    def move_down(self):
        self.score -= 0.02
        if self.map[self.hero.position[1] + 1][self.hero.position[0]] == Service.wall:
            return
        self.hero.position[1] += 1  
        self.interact()

    def move_left(self):
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] - 1] == Service.wall:
            return
        self.hero.position[0] -= 1 
        self.interact()

    def move_right(self):
        self.score -= 0.02
        if self.map[self.hero.position[1]][self.hero.position[0] + 1] == Service.wall:
            return
        self.hero.position[0] += 1
        self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)
