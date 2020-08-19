from abc import ABC, abstractmethod

class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
        
    def lighten(self, light_map):
        self.lmap = light_map
        self.inv_lights = []
        self.inv_obsts = []
        
        dim = (len(self.lmap[0]), len(self.lmap))
        self.find_objects()
        #print(f"dim={dim}")
        self.adaptee.set_dim(dim)
        self.adaptee.set_lights(self.inv_lights)
        self.adaptee.set_obstacles(self.inv_obsts) 
        
        return self.convert2sys_store(self.adaptee.generate_lights())
    
    def find_objects(self):
        #inv_lights = []
        for i in range(len(self.lmap)):
            for j in range(len(self.lmap[0])):
                if self.lmap[i][j] == 1:
                    self.inv_lights.append((j, i))
                elif self.lmap[i][j] == -1:
                    self.inv_obsts.append((j, i))

    def convert2sys_store(self, inv_lmap):
        sys_map = [[0 for i in range(self.adaptee.dim[0])] for _ in range(self.adaptee.dim[1])]
#         print(len(sys_map))
#         print(f"dim={self.adaptee.dim}")
#         print(f"inv_map size {len(inv_lmap[0])}x{len(inv_lmap)}")
        for i in range(self.adaptee.dim[0]):
            for j in range(self.adaptee.dim[1]):
                print(f"i={i}, j={j}")
                self.lmap[j][i] = inv_lmap[j][i]  
        return  self.lmap
        