import random, findbyid

class NotFoundException(Exception):
    pass

def findByID(Cls):
    class FindByIDFactory(object):
        used_ids = []

        def __init__(self, *args, **kwargs):
            cls = type(self)
            self.own_instance = Cls( *args, **kwargs)

            if not hasattr(cls, "has_instantiated_before"):
                print("reset")
                cls.instances = []
                cls.has_instantiated_before = True

            self.ID = cls.__getFreeID()
            cls.instances.append(self)

        @classmethod
        def __getFreeID(cls) -> int:
            while True:
                id = random.randint(10000, 100000)
                if id not in cls.used_ids:
                    break
            cls.used_ids.append(id)
            return id

        @classmethod
        def findByID(cls, ID: int) -> object:

            for i in cls.instances:
                if i.ID == ID:
                    return i
            else:
                raise NotFoundException("Invalid ID!")

        @classmethod
        def getInstances(cls) -> list:
            return cls.instances


    return FindByIDFactory

@findByID
class Dummy():
    def __init__(self):
        # super().__init__()
        print("Moi")

a = Dummy()
b = Dummy()

print(list(map( lambda a: a.ID, Dummy.getInstances())))
print(Dummy.getInstances())

# print(a.ID, b.ID)

print(a is Dummy.findByID(a.ID))
print(b is Dummy.findByID(b.ID))
