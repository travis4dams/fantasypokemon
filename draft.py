import pandas as pd
import random

class PokeType():
    def __init__(self, type1='Normal', type2=None):
        self.type1 = type1
        self.type2 = type2
        self.adtable = pd.read_csv('type_advantages.csv', index_col=0)

    def as_defender(self):
        if self.type1 is not None and self.type2 is not None:
            return (self.adtable[self.type1] * self.adtable[self.type2])
        else:
            return self.adtable[self.type1]

    def as_attacker(self):
        if self.type1 is not None and self.type2 is not None:
            return self.adtable.loc[[self.type1, self.type2]]
        else:
            return self.adtable[self.type1]

    def defending(self, typ):
        return self.as_defender().loc[typ]

    def weak_to(self):
        idx = self.as_defender().index[self.as_defender() > 1].tolist()
        return list(zip(idx, self.as_defender().loc[idx].tolist()))

    def resistant_to(self):
        idx = self.as_defender().index[self.as_defender() < 1].tolist()
        return list(zip(idx, self.as_defender().loc[idx].tolist()))

    def get_type(self):
        return (self.type1, self.type2)


class Pokemon():
    def __init__(self, id=0, name='Missingno', hp=70, atk=70, deF=70, satk=70, sdef=70, spd=70, **kwargs):
        self.id = id
        self.name = name
        self.spd = spd
        self.hp = hp
        self.atk = atk
        self.deF = deF
        self.satk = satk
        self.sdef = sdef
        self.type = PokeType()

    def import_pokedata(self):
        draftable_pokemon = pd.read_csv('draftpokemon.csv', index_col=0)

        if self.id == 0 and self.name == 'Missingno':
            raise KeyError('The id 0 and name of Missingno are not valid.  Please input a valid id or name.')
        elif self.id == 0 and self.name != 'Missingno':
            pokemon = draftable_pokemon.loc[draftable_pokemon['name'] == self.name].to_dict('index')
            self.id =  pokemon.keys()[0]
            pokemon = pokemon[self.id]
        elif self.id != 0 and self.name == 'Missingno':
            pokemon = draftable_pokemon.loc[self.id].to_dict()
            self.name = pokemon['name']
        else:
            pokemon = draftable_pokemon.loc[self.id].to_dict()
            if self.name != pokemon['name']:
                raise KeyError('The id and name of the Pokemon do not match.  Please input only one or an agreeing pair.')

        self.spd = pokemon['spd']
        self.hp = pokemon['hp']
        self.atk = pokemon['atk']
        self.deF = pokemon['def']
        self.satk = pokemon['satk']
        self.sdef = pokemon['sdef']
        self.type = PokeType(pokemon['type1'], pokemon['type2'])

        return [self.id, self.name] + self.get_base_stats() + [self.get_types()]

    def cry(self, **kwargs):
        return '%s!' % (self.name)

    def get_base_speed(self, **kwargs):
        return self.spd

    def get_base_hp(self, *kwargs):
        return self.hp

    def get_base_attack(self, **kwargs):
        return self.atk

    def get_base_defense(self, **kwargs):
        return self.deF

    def get_base_special_attack(self, **kwargs):
        return self.satk

    def get_base_special_defense(self, **kwargs):
        return self.sdef

    def get_base_stats(self, **kwargs):
        return [self.get_base_hp(), self.get_base_attack(), self.get_base_defense(), self.get_base_special_attack(), self.get_base_special_defense(), self.get_base_speed()]

    def get_types(self, **kwargs):
        return self.type.get_type()

    def get_counters(self, **kwargs):
        return self.type.weak_to()

    def __repr__(self):
        return self.name


class Trainer():
    def __init__(self, name='Red'):
        self.name = name
        self.pokemon = []

    def draft_pokemon(self, id):
        poke = Pokemon(id)
        poke.import_pokedata()
        self.pokemon.append(poke)

        return self.pokemon

    def get_power_estimate(self):
        stats = [sum(poke.get_base_stats()) for poke in self.pokemon]

        return sum(stats)/len(stats)

    def __repr__(self):
        return self.name


class Draft():
    def __init__(self, players=['Red', 'Blue', 'Yellow', 'Green']):
        self.names = []
        self.players = []
        for player in players:
            self.names.append(player)
            self.players.append(Trainer(player))

        self.draft_pool = pd.read_csv('draftpokemon.csv', index_col=0)

    def begin_draft(self, order='random'):
        num_pokemon = self.draft_pool.shape[0]
        if order == 'random':
            first_round = self.names
            random.shuffle(first_round)
        elif isinstance(order, list):
            if len(order) != len(self.players):
                raise ValueError('Number of trainers in tournament and the order list does not match.')
            first_round = order
        else:
            raise ValueError('That is not an acceptable option.  Please specify "randmon" or pass a list with the correct order.')

        self.rounds = num_pokemon//len(self.players)
        if self.rounds < 6:
            raise ValueError('There are too many players to support with only %d pokemon.' % (num_pokemon))

        second_round = first_round[::-1]

        self.order = []
        for x in range(0, self.rounds):
            if x % 2 == 0:
                self.order += first_round
            elif x % 2 == 1:
                self.order += second_round
        self.current_drafter = 0

        return self.order

    def draft(self, pokemon):
        if pokemon not in self.draft_pool.index:
            raise IndexError('The pokemon has already been drafted (or is not eligible).  Please make a different selection.')
        self.players[self.names.index(self.order[self.current_drafter])].draft_pokemon(pokemon)

        self.current_drafter += 1

        self.draft_pool = self.draft_pool.drop(pokemon)