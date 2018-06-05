import json, csv
from collections import OrderedDict

def calculate(stats=[], types=[]):
    raw = sum(stats)
    tiers = {'Water'   :1.20,
             'Ground'  :1.15,
             'Steel'   :1.10,
             'Fire'    :1.05,
             'Ghost'   :1.05,
             'Fighting':1.05,
             'Dark'    :1.05,
             'Electric':1.00,
             'Rock'    :1.00,
             'Psychic' :1.00,
             'Dragon'  :1.00,
             'Grass'   :1.00,
             'Poison'  :0.95,
             'Normal'  :0.95,
             'Flying'  :0.90,
             'Ice'     :0.90,
             'Bug'     :0.85
             }
    mod = 1
    for typ in types:
        if typ is None:
            typ = 'Rock'
        mod *= tiers[typ]
    score = raw * mod
    return score

with open('pokedex.json', 'rb') as inF:
    pokemon = json.load(inF)

with open('types.json', 'rb') as inF:
    types = json.load(inF)

typid = {}
for typ in types:
    cname = typ['cname']
    ename = typ['ename']
    typid[cname] = ename

pokedex = OrderedDict()
for poke in pokemon:
    pid = int(poke['id'])
    newtype = []
    for typ in poke['type']:
        typ = typid[typ]
        newtype.append(typ)
    #if len(newtype) == 1 and newtype[0] == 'Fairy':
        #newtype[0] = 'Normal'
    if len(newtype) == 1:
        newtype.append(None)
    poke['type'] = newtype
    pokedex[pid] = poke

with open('basestats.csv', 'rb') as inF:
    reader = csv.reader(inF)
    headers = reader.next()
    for row in reader:
        pid = int(row[0])
        pokedex[pid]['base'] = [int(s) for s in row[2:8]]

#for pid, pokemon in pokedex.items():
    #print pokemon
    #stats = pokemon['base']
    #types = pokemon['type']
    #score = calculate(stats, types)
    #pokemon['score'] = score

#rankdex = sorted(pokedex.items(), key=lambda x:x['score'])

draftable = []
with open('pokemondraft.csv', 'rb') as inF:
    reader = csv.reader(inF)
    for row in reader:
        pid = int(row[0])
        draftable.append(pid)

for pid in pokedex:
    if pid not in draftable:
        del pokedex[pid]
    else:
        pokemon = pokedex[pid]
        stats = pokemon['base']
        types = pokemon['type']
        score = calculate(stats, types)
        pokemon['score'] = score
        pokedex[pid] = pokemon

rankdex = reversed(sorted(pokedex.items(), key=lambda x:x[1]['score']))

rankings = []
for rank in rankdex:
    pid = rank[0]
    poke = rank[1]
    rankings.append(poke['ename'])
print rankings

with open('pokemondraft.csv', 'rb') as inF:
    reader = csv.reader(inF)
    with open('draftpokemon.csv', 'wb') as ouT:
        writer = csv.writer(ouT)
        for row in reader:
            pid = int(row[0])
            pokemon = pokedex[pid]
            name = pokemon['ename']
            types = pokemon['type']
            stats = pokemon['base']
            row += types + stats + [rankings.index(name)]
            writer.writerow(row)
