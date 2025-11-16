from typing import TypeVar, Generic
from animals import Animal, Dog, GermanShepherd

# Típusváltozók
T_co = TypeVar("T_co", covariant=True)      # Readonly / output csak
T_contra = TypeVar("T_contra", contravariant=True)  # Writeonly / input csak

class DoubleBox(Generic[T_co, T_contra]): # covriant használható return értékben de paraméterben nem, kontravariencia pedig fordítva
    def __init__(self, readonly_val: T_co, writeonly_val: T_contra):
        self.readonly_val = readonly_val    # T_co: csak olvasható
        self.writeonly_val = writeonly_val  # T_contra: csak írható
    def get_readonly(self) -> T_co:  # ← OK, covariant output
        return self.readonly_val
    def set_writeonly(self, val: T_contra) -> None:  # ← OK, contravariant input
        self.writeonly_val = val

# A gyakorlatban:
dog : Dog = Dog()
german_dog : GermanShepherd = GermanShepherd()
animal : Animal = Animal()

# nézzük egyszerű esetet:
def f(box: DoubleBox[Animal, Dog]) -> None:
    pass

# kérdés milyen DoubleBox-ot adhatunk át?
f(DoubleBox[Animal, Dog](animal, dog)) # Ez természetesen OK hisz egyeznek a típusok
# Első paraméternél természetesen minden úgyműködik mint ahogy tanultuk az LSP-ben, tehát helyettesíthetjük az Animal-t Dog-al
f(DoubleBox[Dog, Dog](dog, dog)) # OK
f(DoubleBox[GermanShepherd, Dog](german_dog, dog)) # OK

# Második paraméternél viszont NEM
f(DoubleBox[Animal, GermanShepherd](animal, german_dog))   # Hiba

# viszont visszafelé helyettesíthetünk: Egy ős osztály helyettesítheti a leszármazottat contravariáns paraméterben
f(DoubleBox[Animal, Animal](animal, animal))   # OK 
f(DoubleBox[Dog, Animal](dog, animal))   # OK -> első paraméterben Dog helyettesíti Animal-t, második paraméterben Animal helyettesíti Dog-ot


# Dog <: Animal 
# Azt tudjuk hogy: DoubleBox[Dog, Animal] <: DoubleBox[Animal, Dog]  mivel első paraméterben kovarians a másodikban kontravariáns
# ez itt mégis hibára fut:
animal_and_dog: DoubleBox[Animal, Dog] =  DoubleBox(Dog(), Animal())  # Itt még az eredeti Típusokra értelmezett assignációs szabályok érvényesek tehát nem helyettesíthetsz Dog-t Animal-lal

# Először hozd létre a double_box-ot Dog, Animal típusokkal:
dog_and_animal: DoubleBox[Dog, Animal] = DoubleBox(Dog(), Animal())

# erre a tipusra értelmezve már helyes az assignáció:
animal_and_dog2: DoubleBox[Animal, Dog] = dog_and_animal 

