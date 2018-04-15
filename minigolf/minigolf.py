import collections

class Player:
    def __init__(self, player):
        self._player = player
        self.score = 1
        self.attempt = 0
        self.success = 0

    @property
    def name(self):
    	return self._player

class Match:
    hole = 1
    nice_hit = 0
    def default_hole(self):
        Match.hole = 1
    def default_nice_hit(self):
        Match.nice_hit = 0
    def inc_hole(self):
        Match.hole += 1
    def set_nice_hit(self):
        Match.nice_hit = 1

    def __init__(self, numbers, players):
        self.numbers = numbers
        self.players = players
        self.generator = Match.generate_players(numbers, players)
        self.table = Match.default_table(numbers, players)
        self.default_hole()
        self.default_nice_hit()

    @staticmethod
    def generate_players(numbers, players):
        iterations = numbers * 10
        if(Match.hole > 1):
            players.append(players.pop(0))
        while (iterations):
            for value in range(0, numbers):
                yield players[value]
            iterations -+ 1

    @staticmethod
    def default_table(numbers, players):
        none_line = tuple([ None for i in range(0,len(players))])
        name_line = tuple(player.name for player in players)
        table = [none_line for i in range(1, numbers + 2)] 
        table[0] = name_line
        return table

    def make_table(self, next_player):
        my_list = list(self.table[0])
        player_index = my_list.index(next_player.name)
        my_list1 = list(self.table[Match.hole])
        my_list1[player_index] = next_player.score
        my_tuple = tuple(my_list1)
        self.table[Match.hole] = my_tuple

    def get_table(self):
        return self.table

    @property
    def finished(self):
        return Match.hole > self.numbers

    def next_hole(self):
        self.generator = HitsMatch.generate_players(self.numbers, self.players)
        for player in self.players:
            player.success = 0
            player.attempt = 0
        self.inc_hole()
        self.default_nice_hit()

    def get_winners(self):
        if (HolesMatch.hole > self.numbers):  
            total = collections.defaultdict(int)
            for line in self.table[1:]:
                for index, player in enumerate(line):
                    total[index] += player
            last_list = sorted(total.items(), key=lambda x: x[1])
            return self.check_winner(last_list, total)
        else:
            raise RuntimeError('The match is over')

class HitsMatch(Match):
    def hit(self, success = False):
        next_player = next(self.generator)

        while(next_player.success):
            next_player = next(self.generator)

        if (HitsMatch.hole <= self.numbers):
            if(success):
                next_player.success = 1
                next_player.score = next_player.attempt + 1
                self.make_table(next_player)
            else:
                next_player.score = 0
                next_player.attempt += 1
                if (next_player.attempt == 9):
                    next_player.score = 10
                    next_player.success = 1
                    self.make_table(next_player)
            hits = 0
            for player in self.players:
                hits += player.success
            if(hits == self.numbers):
                self.next_hole()
        else:
            raise RuntimeError('The match is over')

    def check_winner(self, last_list, total):
        max_score = last_list[0][1]
        champions = []
        for champion in total:
            if(max_score >= total[champion]):
                champions.append(self.players[champion])
        return champions


class HolesMatch(Match):
    def hit(self, success = False):
        next_player = next(self.generator)

        if (HolesMatch.hole <= self.numbers):
            if(success):
                next_player.score = 1
                self.make_table(next_player)
                self.set_nice_hit()
            else:
                next_player.score = 0
                next_player.attempt += 1
                if (HolesMatch.nice_hit):
                    self.make_table(next_player)
                    if (next_player.name == self.players[-1].name):
                        self.next_hole()
                if (next_player.attempt == 10):
                    self.make_table(next_player)
                    if (next_player.name == self.players[-1].name):
                        self.next_hole()
        else:
            raise RuntimeError('The match is over')

    def check_winner(self, last_list, total):
        max_score = last_list[-1][1]
        champions = []
        for champion in total:
            if(max_score == total[champion]):
                champions.append(self.players[champion])
            else:
                return champions




