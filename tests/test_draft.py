import pytest
from mock import patch

from draft import Draft, Trainer, Pokemon, PokeType

@pytest.fixture
def pokemon():
    poke =  Pokemon(3)
    poke.import_pokedata()
    return poke

def test_pokemon_import_pokedata_when_3_expect_Venusaur():
    pokemon = Pokemon(3)

    result = pokemon.import_pokedata()

    assert result == [3, 'Venusaur', 80,82,83,100,100,80, ('Grass', 'Poison')]

def test_pokemon_import_pokedata_when_Venusaur_expect_Venusaur():
    pokemon = Pokemon(name='Venusaur')

    result = pokemon.import_pokedata()

    assert result == [3, 'Venusaur', 80,82,83,100,100,80, ('Grass', 'Poison')]

def test_pokemon_cry_when_Venusaur_expect_Venusaur(pokemon):

    result = pokemon.cry()

    assert result == 'Venusaur!'

def test_pokemon_get_base_speed_when_Venusaur_expect_80(pokemon):

    result = pokemon.get_base_speed()

    assert result == 80

def test_get_base_stats_when_Venusaur_expect_80x82x83x100x100x80(pokemon):

    result = pokemon.get_base_stats()

    assert result == [80,82,83,100,100,80]

def test_get_types_when_Venusaur_expect_GrassxPoison(pokemon):

    result = pokemon.get_types()

    assert result == ('Grass', 'Poison')

def test_get_counters_when_Venusaur_expect_BugxFlyingxFirexIce(pokemon):

    result = pokemon.get_counters()

    assert result == [('Flying',2.0),('Bug',4.0),('Fire',2.0),('Psychic',2.0),('Ice',2.0)]

def test_resistant_to_when_Venusaur_expect_FightingxWaterxGrassxElectric():
    poketype = PokeType('Grass', 'Poison')

    result = poketype.resistant_to()

    assert result == [('Fighting',0.5),('Water',0.5),('Grass',0.25),('Electric',0.5)]

def test_trainer_draft_pokemon_when_Venusaur_expect_team_Venusaur():
    trainer = Trainer()
    
    result = trainer.draft_pokemon(3)
    print result

    assert isinstance(result, list)
    # assert result == ['Pokemon']

def test_trainer_get_power_estimate_when_team_Venusaur_expect_summed_Venusaur():
    trainer = Trainer()
    trainer.draft_pokemon(3)
    trainer.draft_pokemon(3)
    trainer.draft_pokemon(3)
    trainer.draft_pokemon(3)
    trainer.draft_pokemon(3)
    trainer.draft_pokemon(3)

    result =  trainer.get_power_estimate()

    assert result == 525

def test_draft_begin_draft_when_default_expect_random_order_snaked():
    draft = Draft()

    result = draft.begin_draft()

    assert result != ['Red', 'Blue', 'Yellow', 'Green']