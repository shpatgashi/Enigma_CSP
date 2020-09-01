class House:
    instances = list()

    def __init__(self, color=None, nationality=None, drink=None, pet=None, cigarette=None):
        self.color = color
        self.nationality = nationality
        self.drink = drink
        self.pet = pet
        self.cigarette = cigarette

        self.__class__.instances.append(self)

    def __str__(self):
        return " | ".join(
            (str(self.color), str(self.nationality), str(self.drink), str(self.pet), str(self.cigarette))) + " |"


h_1, h_2, h_3, h_4, h_5 = House(nationality='Norway'), House(), House(drink='Milk'), House(), House()
houses = [h_1, h_2, h_3, h_4, h_5]


class Constraint:
    instances = []

    def __init__(self, offset, c1, c2=None):
        self.c1 = c1
        self.c2 = c2
        self.offset = offset
        self.__class__.instances.append(self)

    def check_value(self, c_key, c_val):
        if {c_key: c_val} not in (self.c1, self.c2):
            return True
        if type(self.offset) == list:
            if self.position(self.c1) - self.position(self.c2) in self.offset:
                return True
        else:
            if self.position(self.c1) - self.position(self.c2) == self.offset:
                return True
        return False

    @staticmethod
    def position(x):
        key, val = list(x.keys())[0], x[list(x.keys())[0]]
        for house in houses:
            if getattr(house, key) == val:
                return houses.index(house)

        x = list(map(lambda h: (houses.index(h) if getattr(h, key) is None else None), houses))
        return next(item for item in x if item is not None)

    def __str__(self):
        return " ".join([str(self.position(self.c1)), str(self.position(self.c2))])



constraints = [
    Constraint(c1={'nationality': 'England'}, c2={'color': 'Red'}, offset=0),                 # Anglezi jeton në shtëpinë e kuqe
    Constraint(c2={'pet': 'Dog'}, c1={'nationality': 'Spain'}, offset=0),                     # Spanjolli zotëron qenin
    Constraint(c1={'cigarette': 'Marlboro'}, c2={'color': 'Yellow'}, offset=0),               # Marlboro thithet në shtëpinë e verdhë.
    Constraint(c1={'cigarette': 'Chesterfield'}, c2={'pet': 'Fox'}, offset=[-1, 1]),          # Njeriu që pi duhan Chesterfields jeton në shtëpinë pranë burrit me dhelpra.
    Constraint(c1={'nationality': 'Norway'}, c2={'color': 'Blue'}, offset=[-1, 1]),           # Norvegjiani jeton pranë shtëpisë blu.
    Constraint(c1={'cigarette': 'Winston'}, c2={'pet': 'Snail'}, offset=0),                   # Konsumuesi i duhanit Winston zotëron kërmij.
    Constraint(c1={'drink': 'Orange Juice'}, c2={'cigarette': 'Lucky Strike'}, offset=0),     # Konsumuesi i duhanit Lucky Strike pi lëng portokalli.
    Constraint(c1={'drink': 'Tea'}, c2={'nationality': 'Ukraine'}, offset=0),                 # Ukrainasi pi çaj.
    Constraint(c1={'cigarette': 'Parliament'}, c2={'nationality': 'Japan'}, offset=0),        # Japonezët pinë duhenin Parlament.
    Constraint(c1={'cigarette': 'Marlboro'}, c2={'pet': 'Horse'}, offset=[-1, 1]),            # Marlboro konsumohet në shtëpinë pranë shtëpisë ku mbahet kali.
    Constraint(c1={'drink': 'Coffee'}, c2={'color': 'Green'}, offset=0),                      # Kafja pihet në shtëpinë e gjelbër.
    Constraint(c1={'drink': 'Coffee'}, c2={'color': 'Ivory'}, offset=1)                       #Shtëpia e gjelbër është menjëherë në të djathtë të shtëpisë së fildishtë.
]

colors = ['Yellow', 'Red', 'Blue', 'Green', 'Ivory']
nationalities = ['Spain', 'England', 'Japan', 'Ukraine']
pets = ['Fox', 'Horse', 'Dog', 'Snail', 'Zebra']
cigarettes = ['Marlboro', 'Lucky Strike', 'Parliament', 'Winston', 'Chesterfield']
drinks = ['Water', 'Coffee', 'Tea', 'Orange Juice']


class SolveEnigma:

    @staticmethod
    def check_constraints(c_key, c_val):
        return all([constraint.check_value(c_key, c_val) for constraint in constraints])

    def add_drink(self, house):
        if house.drink is not None:
            return self.add_color(houses[houses.index(house) + 1])

        for drink in drinks:
            if self.check_constraints('drink', drink):
                house.drink = drink
                drinks.remove(drink)

                if houses.index(house) == 4:
                    return True

                if self.add_color(houses[houses.index(house) + 1]):
                    return True

                else:
                    drinks.append(drink)
                    house.drink = None

        return False

    def add_cigarette(self, house):
        if house.cigarette is not None:
            return self.add_drink(house)

        for cigarette in cigarettes:
            if self.check_constraints('cigarette', cigarette):
                house.cigarette = cigarette
                cigarettes.remove(cigarette)
                if self.add_drink(house):
                    return True
                else:
                    cigarettes.append(cigarette)
                    house.cigarette = None

        return False

    def add_pet(self, house):
        if house.pet is not None:
            return self.add_cigarette(house)

        for pet in pets:
            if self.check_constraints('pet', pet):
                house.pet = pet
                pets.remove(pet)
                if self.add_cigarette(house):
                    return True
                else:
                    pets.append(pet)
                    house.pet = None

        return False

    def add_nationality(self, house):
        if house.nationality is not None:
            return self.add_pet(house)

        for nationality in nationalities:
            if self.check_constraints('nationality', nationality):
                house.nationality = nationality
                nationalities.remove(nationality)
                if self.add_pet(house):

                    return True
                else:
                    nationalities.append(nationality)
                    house.nationality = None
        return False

    def add_color(self, house):
        if house.color is not None:
            return self.add_nationality(house)

        for color in colors:
            if self.check_constraints('color', color):
                house.color = color
                colors.remove(color)

                if self.add_nationality(house):
                    return True
                else:
                    colors.append(color)
                    house.color = None
        return False


SolveEnigma().add_color(houses[0])
for h in houses:
    print(h)
