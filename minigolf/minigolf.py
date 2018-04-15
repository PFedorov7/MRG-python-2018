import collections

class Player:
    def __init__(self, player):
        self._player = player
        self._score = 1
        self._attempt = 0
        self._success = 0

    @property
    def name(self):
    	return self._player

class Match:
    hole = 1
    nice_hit = 0
    def _default_hole(self):
        Match.hole = 1
    def _default_nice_hit(self):
        Match.nice_hit = 0
    def _inc_hole(self):
        Match.hole += 1
    def _set_nice_hit(self):
        Match.nice_hit = 1

    def __init__(self, numbers, players):
        self._numbers = numbers
        self._players = players
        self._generator = Match.generate_players(numbers, players)
        self._table = Match.default_table(numbers, players)
        self._default_hole()
        self._default_nice_hit()

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

    def _make_table(self, next_player):
        my_list = list(self._table[0])
        player_index = my_list.index(next_player.name)
        my_list1 = list(self._table[Match.hole])
        my_list1[player_index] = next_player._score
        my_tuple = tuple(my_list1)
        self._table[Match.hole] = my_tuple

    def get_table(self):
        return self._table

    @property
    def finished(self):
        return Match.hole > self._numbers

    def _next_hole(self):
        self._generator = HitsMatch.generate_players(self._numbers, self._players)
        for player in self._players:
            player._success = 0
            player._attempt = 0
        self._inc_hole()
        self._default_nice_hit()

    def get_winners(self):
        if (HolesMatch.hole > self._numbers):  
            total = collections.defaultdict(int)
            for line in self._table[1:]:
                for index, player in enumerate(line):
                    total[index] += player
            last_list = sorted(total.items(), key=lambda x: x[1])
            return self._check_winner(last_list, total)
        else:
            raise RuntimeError('The match is over')

class HitsMatch(Match):
    def hit(self, success = False):
        next_player = next(self._generator)

        while(next_player._success):
            next_player = next(self._generator)

        if (HitsMatch.hole <= self._numbers):
            if(success):
                next_player._success = 1
                next_player._score = next_player._attempt + 1
                self._make_table(next_player)
            else:
                next_player._score = 0
                next_player._attempt += 1
                if (next_player._attempt == 9):
                    next_player._score = 10
                    next_player._success = 1
                    self._make_table(next_player)
            hits = 0
            for player in self._players:
                hits += player._success
            if(hits == self._numbers):
                self._next_hole()
        else:
            raise RuntimeError('The match is over')

    def _check_winner(self, last_list, total):
        max_score = last_list[0][1]
        champions = []
        for champion in total:
            if(max_score >= total[champion]):
                champions.append(self._players[champion])
        return champions


class HolesMatch(Match):
    def hit(self, success = False):
        next_player = next(self._generator)

        if (HolesMatch.hole <= self._numbers):
            if(success):
                next_player._score = 1
                self._make_table(next_player)
                self._set_nice_hit()
            else:
                next_player._score = 0
                next_player._attempt += 1
                if (HolesMatch.nice_hit):
                    self._make_table(next_player)
                    if (next_player.name == self._players[-1].name):
                        self._next_hole()
                if (next_player._attempt == 10):
                    self._make_table(next_player)
                    if (next_player.name == self._players[-1].name):
                        self._next_hole()
        else:
            raise RuntimeError('The match is over')

    def _check_winner(self, last_list, total):
        max_score = last_list[-1][1]
        champions = []
        for champion in total:
            if(max_score == total[champion]):
                champions.append(self._players[champion])
            else:
                return champions




