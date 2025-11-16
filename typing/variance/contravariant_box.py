from typing import TypeVar, Generic
from animals import Animal, Dog

T_contra = TypeVar("T_contra", contravariant=True)  # T_contra egy kontravariant típusváltozó

class Box(Generic[T_contra]):
    def __init__(self, value: T_contra):
        self.value = value

# Ez azt jelenti, hogy T-re nézve a Box kovariáns ami azt jelenti hogy csak olvasni tudja írni nem!

dog = Dog()
box_of_dog : Box[Dog] = Box(dog)

def get_animal_from_box(box: Box[Animal]) -> Animal:
    return box.value

get_animal_from_box(box_of_dog)  # Ez Hiba! mert Box kontravariáns, nem helyettesítheti egy box[Dog] egy box[Animal]-t

class WrongBox(Generic[T_contra]):
    def __init__(self, value: T_contra):
        self.value = value
    def get_value(self) -> T_contra: # Hiba! T_contra nem használható outputként
        return self.value
