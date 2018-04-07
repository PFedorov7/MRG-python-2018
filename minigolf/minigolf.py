import collections

class Player:
    def __init__(self, player):
        self._player = player
        self.score = 1

    @property
    def name(self):
    	return self._player

class HitsMatch:

    def __init__(self, numbers, players):

        self.numbers = numbers
        self.players = players
        self.status = True

        self.value = 0
        self.hole = 1
        self.big = [i for i in range(0, numbers)]
        self.table = HitsMatch.default_table(numbers, players)

    def hit(self, success = False):

        if (self.hole <= self.numbers):  
            if (success == False):
                self.players[self.big[self.value]].score += 1
                if (self.players[self.big[self.value]].score == 10):
                    self.make_table(self.big.pop(self.value))
                if (self.value + 1 >= len(self.big)):
                    self.value = 0
                else:
                    self.value += 1
            else:

                self.make_table(self.big.pop(self.value))
                if(self.value + 1 >= len(self.big)):
                    self.value = 0

            if(len(self.big) == 0):
                self.status = False
                self.value = self.hole
                self.big = [i for i in range(0, self.numbers)]
                self.hole += 1
                for player in self.players:
                    player.score = 1
        else:
            raise RuntimeError('The match is over')

    def make_table(self, index):
        my_list = list(self.table[self.hole])
        my_list[index] = self.players[index].score
        my_tuple = tuple(my_list)
        self.table[self.hole] = my_tuple


    @staticmethod
    def default_table(numbers, players):
        none_line = tuple([ None for i in range(0,len(players))])
        name_line = tuple(player.name for player in players)
        table = [none_line for i in range(1, numbers + 2)] 
        table[0] = name_line
        return table

    @property
    def finished(self):
        return self.hole > self.numbers

    def get_table(self):
        return self.table

    def get_winners(self):
        if (self.hole > self.numbers):  
            total = collections.defaultdict(int)
            for line in self.table[1:]:
                for player in self.big:
                    total[player] += line[player]
            last_list = sorted(total.items(), key=lambda x: x[1])
            max_score = last_list[0][1]
            champions = []
            for champion in total:
                if(max_score >= total[champion]):
                    champions.append(self.players[champion])
            return champions
        else:
            raise RuntimeError('The match is over')

class HolesMatch:
    pass
