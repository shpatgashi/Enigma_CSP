class House:
    instances = list()

    def __init__(self, color=None, nationality=None, drink=None, pet=None, cigarette=None):
        self.color = color
        self.nationality = nationality
        self.drink = drink
        self.pet = pet
        self.cigarette = cigarette

        self.__class__.instances.append(self)


h_1, h_2, h_3, h_4, h_5 = House(nationality='Norway'), House(), House(drink='Milk'), House(), House()
houses = [h_1, h_2, h_3, h_4, h_5]


class Constraint:
    def __init__(self, position, c1, c2=None):
        self.c1 = c1
        self.c2 = c2
        self.position = position

    def check_value(self, c_key, c_val):

        if {c_key: c_val} not in (self.c1, self.c2):
            return True

        if type(self.position) == list:
            if self.positioning(self.c1) - self.positioning(self.c2) in self.position:
                return True
        else:
            if self.positioning(self.c1) - self.positioning(self.c2) == self.position:
                return True

        return False

    @staticmethod
    def positioning(x):
        key, val = list(x.keys())[0], x[list(x.keys())[0]]
        for house in houses:
            if getattr(house, key) == val:
                return houses.index(house)
            else:
                return list(map(lambda h: houses.index(h), houses))[0]


constraints = [Constraint(c1={'nationality': 'England'}, c2={'color': 'Red'}, position=0),
               Constraint(c1={'nationality': 'Spain'}, c2={'pet': 'Dog'}, position=0),
               Constraint(c1={'color': 'Yellow'}, c2={'cigarette': 'Marlboro'}, position=0),
               Constraint(c1={'pet': 'Fox'}, c2={'cigarette': 'Chesterfield'}, position=[1, -1]),
               Constraint(c1={'nationality': 'Norway'}, c2={'color': 'Blue'}, position=[1, -1]),
               Constraint(c1={'pet': 'Snail'}, c2={'cigarette': 'Winston'}, position=0),
               Constraint(c1={'cigarette': 'Lucky Strike'}, c2={'drink': 'Orange Juice'}, position=0),
               Constraint(c1={'nationality': 'Ukraine'}, c2={'drink': 'Tea'}, position=0),
               Constraint(c1={'nationality': 'Japan'}, c2={'cigarette': 'Parliament'}, position=0),
               Constraint(c1={'cigarette': 'Marlboro'}, c2={'pet': 'Horse'}, position=[1, -1]),
               Constraint(c1={'drink': 'Coffee'}, c2={'color': 'Green'}, position=0),
               Constraint(c1={'color': 'Green'}, c2={'color': 'Ivory'}, position=1)]

colors = ['Green', 'Yellow', 'Blue', 'Red', 'Ivory']
nationalities = ['Ukraine', 'England', 'Spain', 'Japan', 'Norway']
pets = ['Fox', 'Snail', 'Dog', 'Zebra', 'Horse']
drinks = ['Orange Juice', 'Water', 'Tea', 'Milk', 'Coffee']
cigarettes = ['Marlboro', 'Chesterfield', 'Winston', 'Lucky Strike', 'Parliament']


def check_constraints(c_key, c_val):
    return all([constraint.check_value(c_key, c_val) for constraint in constraints])


def add_drink(house):
    if house.drink is not None:
        return True

    for drink in drinks:
        if check_constraints('drink', drink):
            house.drink = drink
            drinks.remove(drink)
            return True

    return False


def add_cigarette(house):
    if house.cigarette is not None:
        return add_drink(house)

    for cigarette in cigarettes:
        if check_constraints('cigarette', cigarette):
            house.cigarette = cigarette
            cigarettes.remove(cigarette)
            if add_drink(house):
                return True
            else:
                cigarettes.append(cigarette)
                house.cigarette = None

    return False


def add_pet(house):
    if house.pet is not None:
        return add_cigarette(house)

    for pet in pets:
        if check_constraints('pet', pet):
            house.pet = pet
            pets.remove(pet)
            if add_cigarette(house):
                return True
            else:
                pets.append(pet)
                house.pet = None

    return False


def add_nationality(house):
    if house.nationality is not None:
        return add_pet(house)

    for nationality in nationalities:
        if check_constraints('nationality', nationality):
            house.nationality = nationality
            nationalities.remove(nationality)
            if add_pet(house):
                return True
            else:
                nationalities.append(nationality)
                house.nationality = None
    return False


def add_color(house):
    if house.color is not None:
        return add_nationality(house)

    for color in colors:
        if check_constraints('color', color):
            house.color = color
            colors.remove(color)
            if add_nationality(house):
                return True
            else:
                colors.append(color)
                house.color = None
    return False


def add_houses(index=0):
    if index == 4:
        return True

    if add_color(houses[index]):
        return add_houses(index + 1)


add_houses()
for h in houses:
    print(h.color, h.nationality, h.cigarette, h.drink, h.pet)
