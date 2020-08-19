from abc import ABC, abstractmethod

class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base       

    def get_positive_effects(self):
        return self.base.get_positive_effects()
    

    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    @abstractmethod
    def get_stats(self):
        pass


class AbstractNegative(AbstractEffect):
    @abstractmethod
    def get_negative_effects(self):
        pass
    
    
class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass

class Berserk(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Berserk"]

    def get_stats(self):
        stat_dynamic = self.base.get_stats()
        
        up7 = ['Strength', 'Endurance', 'Luck', 'Agility']
        down3 = ['Perception', 'Charisma', 'Intelligence']
        for stat in up7:
            stat_dynamic[stat] += 7
        for stat in down3:
            stat_dynamic[stat] -= 3
        stat_dynamic['HP'] += 50
        
        return stat_dynamic

class Curse(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Curse"]
    
    def get_stats(self):
        stat_dynamic = self.base.get_stats()
        main_stats = ['Strength', 'Endurance', 'Luck', 'Agility', 
                        'Perception', 'Charisma', 'Intelligence']
        for stat in main_stats:
            stat_dynamic[stat] -= 2
            
        return stat_dynamic

class Blessing(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Blessing"]
    #def get_

    def get_stats(self):
        stat_dynamic = self.base.get_stats()
        main_stats = ['Strength', 'Endurance', 'Luck', 'Agility', 
            'Perception', 'Charisma', 'Intelligence']
        for stat in main_stats:
            stat_dynamic[stat] += 2
            
        return stat_dynamic

class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["EvilEye"]
    
    def get_stats(self):
        stat_dynamic = self.base.get_stats()
        stat = 'Luck'
        stat_dynamic[stat] -= 10
            
        return stat_dynamic

class Weakness(AbstractNegative):
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Weakness"]
    
    def get_stats(self):
        stat_dynamic = self.base.get_stats()
        stats = ['Strength', 'Endurance', 'Agility']
        for stat in stats:
            stat_dynamic[stat] -= 4
            
        return stat_dynamic