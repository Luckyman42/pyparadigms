# A függvények input paraméterben kovariánsak, az output paraméterben pedig kontravariánsak.
from typing import Callable

class Complex:
    float_part: float
    imagenary_part: float
    def __init__(self, float_part: float, imagenary_part: float):
        self.float_part = float_part
        self.imagenary_part = imagenary_part

class Rational(Complex):
    numerator: int
    denominator: int
    def __init__(self, numerator: int, denominator: int):
        super().__init__(numerator / denominator, 0.0)
        self.numerator = numerator
        self.denominator = denominator

class Integer(Rational):
    value : int
    def __init__(self, value: int):
        super().__init__(value, 1)


def floor(r: Rational) -> Integer:
    return Integer(r.numerator)

def to_rational(i: Integer) -> Rational:
    return Rational(i.value, 1)

def call(func: Callable[[Integer], Rational], arg: Integer) -> Rational:
    return func(arg)


# Call function-nek van egy függvény paramétere ami I->R, itt feltehetjük a kérdésst mivel lehet helyetetsíteni ezt a függvényt? mi az ő altípusa?
call(floor, Integer(5)) # A floor egy R->I függvény, mégis helyes!

# Tudjuk hogy I <: R, a függvények input paraméterben kontravariáns míg output paraméterben kovariáns, tehát:
# floor : R -> I 
# paraméterként egy I -> R függvényt várunk
# Kontravariancia miatt input paraméterben az ős helyettesítheti az utódát, míg output paraméterben az utód helyettesítheti az ősét
# R -> I <: I -> R

def call2(func: Callable[[Rational], Rational], arg: Rational) -> Rational: 
    return func(arg)

def complex_to_integer(c: Complex) -> Integer:
    return Integer(int(c.float_part))

call2(complex_to_integer, Rational(3,4)) # Ez is OK! mert C -> I  <: R -> R

# Hogy miért van ez? Az LSP miatt:
# Tegyük fel hogy van egy függvényünk ami egy R -> R függvényünk.
# eddig használtuk ezt a függvényt valamilyen környezetben, adtunk neki egy Rational-t és visszakapunk egy Rational-t

# ha én ezt egy Integer -> Rational függvénnyel helyettesítem, akkor ez a függvény egy Rational-t fog kapni ami helytelen mert egy típust mindig csak az alosztályaival helyettesíthetünk
# így láthatjuk hogy ha eddig volt egy Racionálison értelmezett függvény és adok egy integeren értelmezettet akkor azzal szűkítem a befogadható tartományt, ami hiba.
# Viszont ha adok egy Complexen értelmezettet akkor azzal bővítem a befogadható tartományt, ami OK.

# Nézzük a másik irányt, a visszatérési értéket.

# Eddig ez a függvény egy Racionált adott vissza, ha én ezt egy Complexet visszaadó függvénnyel helyettesítem akkor azzal bővítem a visszatérési érték tartományát,
#     de ezt a függvény visszatérését valahogy valahol felhasználtam ahol Racionálist vártam, ha Complexet kapok akkor ott azon a ponton nem helyettesíthetném vele.
# Ellenben ha szükítem a visszatérési értéket Integerre akkor azzal szükítem a visszatérési érték tartományát, ami engedett mivel ahol Racionálist vártam eddig ott az Integer is megfelel. 