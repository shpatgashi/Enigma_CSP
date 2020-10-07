from typing import Tuple, Optional


class Constraint:

    def __init__(self, offset, c1: dict, c2: dict = None):
        self.c1 = c1
        self.c2 = c2
        self.offset = offset


constraints = [
    Constraint(c1={'nationality': 'England'}, c2={'color': 'Red'}, offset=0),               # Anglezi jeton në shtëpinë e kuqe
    Constraint(c1={'pet': 'Dog'}, c2={'nationality': 'Spain'}, offset=0),                   # Spanjolli zotëron qenin
    Constraint(c1={'nationality': 'Norway'}, offset=0),                                     # Norvegjezi jeton ne shtepinë e parë
    Constraint(c1={'drink': 'Milk'}, offset=2),                                             # Qumështi pihet në shtepinë e mesme
    Constraint(c1={'cigarette': 'Marlboro'}, c2={'color': 'Yellow'}, offset=0),             # Marlboro thithet në shtëpinë e verdhë.
    Constraint(c1={'cigarette': 'Winston'}, c2={'pet': 'Snail'}, offset=0),                 # Konsumuesi i duhanit Winston zotëron kërmij.
    Constraint(c1={'drink': 'Orange Juice'}, c2={'cigarette': 'Lucky Strike'}, offset=0),   # Konsumuesi i duhanit Lucky Strike pi lëng portokalli.
    Constraint(c1={'drink': 'Tea'}, c2={'nationality': 'Ukraine'}, offset=0),               # Ukrainasi pi çaj.
    Constraint(c1={'cigarette': 'Parliament'}, c2={'nationality': 'Japan'}, offset=0),      # Japonezët pinë duhenin Parlament.
    Constraint(c1={'drink': 'Coffee'}, c2={'color': 'Green'}, offset=0),                    # Kafja pihet në shtëpinë e gjelbër.
    Constraint(c1={'color': 'Ivory'}, c2={'color': 'Green'}, offset=1),                     # Shtëpia e gjelbër është menjëherë në të djathtë të shtëpisë së fildishtë.
    Constraint(c1={'cigarette': 'Chesterfield'}, c2={'pet': 'Fox'}, offset=[-1, 1]),        # Njeriu që pi duhan Chesterfields jeton në shtëpinë pranë burrit me dhelpra.
    Constraint(c1={'nationality': 'Norway'}, c2={'color': 'Blue'}, offset=[-1, 1]),         # Norvegjiani jeton pranë shtëpisë blu.
    Constraint(c1={'cigarette': 'Marlboro'}, c2={'pet': 'Horse'}, offset=[-1, 1]),          # Marlboro konsumohet në shtëpinë pranë shtëpisë ku mbahet kali.
]


class House:
    def __init__(self, color=None, nationality=None, drink=None, pet=None, cigarette=None):
        self.color = color
        self.nationality = nationality
        self.drink = drink
        self.pet = pet
        self.cigarette = cigarette

    def __str__(self):
        return " | ".join(
            (str(self.color), str(self.nationality), str(self.drink), str(self.pet), str(self.cigarette))) + " |"


h_1, h_2, h_3, h_4, h_5 = House(), House(), House(), House(), House()
Houses = [h_1, h_2, h_3, h_4, h_5]


def set_constraint(constraint: Constraint):
    for index, house in enumerate(Houses):
        valid, other_house = eligible_to_put_in_house(constraint, house)
        if valid:
            house.__setattr__(list(constraint.c1.keys())[0], constraint.c1[list(constraint.c1.keys())[0]])
            if constraint.c2 is not None:
                if other_house is None:
                    house.__setattr__(list(constraint.c2.keys())[0], constraint.c2[list(constraint.c2.keys())[0]])
                else:
                    other_house.__setattr__(list(constraint.c2.keys())[0], constraint.c2[list(constraint.c2.keys())[0]])

            if constraints.index(constraint) == 13:
                return True

            if set_constraint(constraints[constraints.index(constraint) + 1]):
                return True

            house.__setattr__(list(constraint.c1.keys())[0], None)
            if constraint.c2 is not None:
                if other_house is None:
                    house.__setattr__(list(constraint.c2.keys())[0], None)
                else:
                    other_house.__setattr__(list(constraint.c2.keys())[0], None)

    return False


def eligible_to_put_in_house(constraint: Constraint, house) -> Tuple[bool, Optional[House]]:
    c1_actual_val = getattr(house, list(constraint.c1.keys())[0], None)
    c1_tentative_val = constraint.c1[list(constraint.c1.keys())[0]]

    if constraint.c2 is None:
        if Houses.index(house) != constraint.offset:
            return False, None
        if c1_actual_val is None or c1_actual_val == c1_tentative_val:
            return True, None
        return False, None

    c2_actual_val = getattr(house, list(constraint.c2.keys())[0], None)
    c2_tentative_val = constraint.c2[list(constraint.c2.keys())[0]]

    if constraint.offset == 0:
        if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (c2_actual_val is None or c2_actual_val == c2_tentative_val):
            return True, None

    elif isinstance(constraint.offset, int):
        if Houses.index(house) + constraint.offset > 4:
            return False, None

        next_house = Houses[Houses.index(house) + constraint.offset]
        # offset shows how far away is the second house from the first house
        next_house_c2_val = getattr(next_house, list(constraint.c2.keys())[0], None)

        if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (
                next_house_c2_val is None or next_house_c2_val == c2_tentative_val):
            return True, next_house

    else:
        if Houses.index(house) + 1 > 4:
            # try left
            next_house = Houses[Houses.index(house) - 1]
            next_house_c2_val = getattr(next_house, list(constraint.c2.keys())[0], None)
            if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (
                    next_house_c2_val is None or next_house_c2_val == c2_tentative_val):
                return True, next_house

        elif Houses.index(house) - 1 < 0:
            # try right
            next_house = Houses[Houses.index(house) + 1]
            next_house_c2_val = getattr(next_house, list(constraint.c2.keys())[0], None)
            if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (
                    next_house_c2_val is None or next_house_c2_val == c2_tentative_val):
                return True, next_house

        else:
            # try right
            next_house = Houses[Houses.index(house) + 1]
            next_house_c2_val = getattr(next_house, list(constraint.c2.keys())[0], None)
            if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (
                    next_house_c2_val is None or next_house_c2_val == c2_tentative_val):
                return True, next_house
            # try left
            next_house = Houses[Houses.index(house) - 1]
            next_house_c2_val = getattr(next_house, list(constraint.c2.keys())[0], None)
            if (c1_actual_val is None or c1_actual_val == c1_tentative_val) and (
                    next_house_c2_val is None or next_house_c2_val == c2_tentative_val):
                return True, next_house

    return False, None


if __name__ == '__main__':
    if set_constraint(constraints[0]):
        for house in Houses:
            if getattr(house, 'drink', None) is None:
                missing_drink_house = house
            if getattr(house, 'pet', None) is None:
                missing_pet_house = house
            print(house)
    print(
        f'\n\nZebra belongs to the {missing_pet_house.color} house.\nThe {missing_drink_house.nationality} guy who smokes {missing_drink_house.cigarette} drinks a lot of water.')
