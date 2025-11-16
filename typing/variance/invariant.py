from animals import Animal, Dog, Cat

def feed(animal: Animal) -> None:
    pass

def feed_all(animals: list[Animal]) -> None:
    pass

feed(Dog()) # Ez OK! mert Dog egy Animal
feed_all([Dog(),Dog()]) # Ez hiba! A listák invariánsak!

# Ha list[Dog] <: list[Animal] lenne, akkor ez működne:
dogs : list[Dog] = [Dog(), Dog()]

def add_cat(zoo: list[Animal]) -> None:
    zoo.append(Cat())

add_cat(dogs)  # Ennek hibának kell lennnie!

# A tuple típus mivel inmutable ezért kovariáns:

def switch_animals(pair: tuple[Animal, Animal]) -> tuple[Animal, Animal]:
    return (pair[1], pair[0])

dog_cat_pair: tuple[Dog, Cat] = (Dog(), Cat())
switched_pair = switch_animals(dog_cat_pair)  # Ez OK! Mert az eredeti dog_cat_pair nem változik meg, csak egy új tuple jön létre
