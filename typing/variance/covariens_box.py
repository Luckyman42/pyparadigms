from typing import TypeVar, Generic
from animals import Animal, Dog

T_co = TypeVar("T_co", covariant=True)  # T_co egy kovariáns típusváltozó

class Box(Generic[T_co]):
    def __init__(self, value: T_co):
        self.value = value
    def get_value(self) -> T_co:
        return self.value

# Ez azt jelenti, hogy T-re nézve a Box kovariáns ami azt jelenti hogy csak olvasni tudja írni nem!

dog = Dog()
box_of_dog : Box[Dog] = Box(dog)

def get_animal_from_box(box: Box[Animal]) -> Animal:
    return box.value

get_animal_from_box(box_of_dog)  # Ez OK! mert Box kovariáns, Listával nem tudna működni mert az invariant!

class WrongBox(Generic[T_co]):
    def __init__(self, value: T_co):
        self.value = value
    def set_value(self, val: T_co) -> None: # Hiba! T_co nem használható inputként
        self.value = val