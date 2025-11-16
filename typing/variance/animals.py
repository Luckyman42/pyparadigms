
class Animal:
    def speak(self) -> str:
        return "Some sound"

class Dog(Animal):
    def speak(self) -> str:
        return "Woof"

class GermanShepherd(Dog):
    def speak(self) -> str:
        return "Loud Woof"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow"

