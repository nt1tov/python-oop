class Event:
    def __init__(self, t):
        self.kind = None
        self.dtype = None
        
class EventGet(Event):
    def __init__(self, t):
        self.kind = "get"
        self.dtype = t
        self.data = None

class EventSet(Event):
    def __init__(self, data):
        self.dtype = type(data)
        self.kind = "set"
        self.data = data


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor
    
    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)
        else:
            return None
           
class FloatHandler(NullHandler): 
    def handle(self, obj, event):
        if event.dtype == float:
            #print(f"{event.kind} {event.dtype} value in FloatHandler")
            if event.kind == 'get':
                print(f"returning {obj.float_field} ")
                return obj.float_field
            elif event.kind == 'set':
                obj.float_field = event.data
                return None
        else:
            #print("Передаю обработку дальше")
            return super().handle(obj, event)
            
class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.dtype == int:
            #print(f"{event.kind} {event.dtype} value in IntHandler")
            if event.kind == 'get':
                return obj.integer_field
            elif event.kind == 'set':
                obj.integer_field = event.data
                return None
        else:
            #print("Передаю обработку дальше")
            return super().handle(obj, event)

class StrHandler(NullHandler): 
    def handle(self, obj, event):
        if event.dtype == str:
            #print(f"{event.kind} {event.dtype} value in StrHandler")
            if event.kind == 'get':
                return obj.string_field
            elif event.kind == 'set':
                obj.string_field = event.data
                return None
        else:
            #print("Передаю обработку дальше")
            return super().handle(obj, event)
