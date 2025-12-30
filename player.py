class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 0
        self.stake = 0
        self.stake_gap = 0
        self.cards = []
        self.fold = False
        self.all_in = False
        self.check = False
        self.turn = True 
