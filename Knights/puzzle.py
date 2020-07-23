from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # A is either a knave or a knight
    Or(AKnight,AKnave),
    # If its Aknave then the sentence is false
    Implication(AKnave, Not(And(AKnave, AKnight))),
    # If its a Knight then the sentence is true
    Implication(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # A can't be a knave if its a knight
    Implication(AKnight, Not(AKnave)),
    # A could be either a knive or a knave
    Or(AKnight, AKnave),
    # B can't be a knave if its a knight
    Implication(BKnight, Not(BKnave)),
    # B could be either a knive or a knave
    Or(BKnight, BKnave),
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, BKnight),
    Implication(BKnight, AKnave),
    Implication(AKnave, BKnight),
    Implication(BKnave, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Or(AKnight, AKnave), Or(BKnight, BKnave), Or(CKnight, CKnave),
    Implication(BKnight,And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
