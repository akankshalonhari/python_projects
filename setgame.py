import random

class Table:
    def __init__(self, n=12):
        #print("init Table")
        self.cards = random.sample(Card.allcards(), n)
        print(self.cards)

    def find_sets(self):
        found = []
        print("find_sets")
        # given list of cards return sets
        for indexa, card1 in enumerate(self.cards):
            for indexb, card2 in enumerate(self.cards[indexa+1], indexa+1):
                for indexc, card3 in enumerate(self.cards[indexb+1], indexb+1):
                    if card1.is_set(card2, card3):
                        found.append((card1, card2, card3))
        print(found)
        return found

    def run_tests(self):
        #check to make sure that is set returns the correct results for various collections
        pass    

#Card is 4 tuple representing attributes with 0/1/2 values
class Card:
    def __init__(self, *attrs):
        print("init Card")
        self.attrs = attrs

    def is_set(self, card1, card2):
        print("is_set")
        def allsame(v0, v1, v2):    # checks for one attribute
            return v0==v1 and v1==v2
        def alldiff(v0, v1, v2):    # checks for one attribute
            return len({v0, v1, v2})==3
        return all(allsame(v0, v1, v2) or alldiff(v0, v1, v2)
                   for (v0, v1, v2) in zip(self.attrs, card1.attrs, card2.attrs))

    @staticmethod
    def allcards():
        print("init all Cards")
        return [ Card(att0, att1, att2, att3)
                    for att0 in (0, 1, 2)
                    for att1 in (0, 1, 2)
                    for att2 in (0, 1, 2)
                    for att3 in (0, 1, 2)
        ]
    
t=Table()
t.find_sets()