# Django ELO Rating

## Installation

```bash
python3 -m pip install --user --upgrade django_elo_rating
```

## Configuation

In your `settings.py` add the following lines

```python
ELO_START_VALUE = 1000
ELO_FACTOR_K = 30
```

## Usage

```python
from django_elo_rating import EloRated


class Player(EloRated):
    pass


player_1 = Player()
player_2 = Player()

print(player_1.elo_rating)
# 1000 or whatever you set as ELO_START_VALUE
print(player_2.elo_rating)
# 1000 or whatever you set as ELO_START_VALUE

probability_player_1_wins = player_1.probability(player_2)
print(probability_player_1_wins)
# 0.5

# If player_1 wins a game against player_2 
# update player_1's elo rating like this
player_1.elo_rating = player_1.updated_elo(player_2, 1)
# and player_2's like this 
player_2.elo_rating = player_2.updated_elo(player_1, 0)


# If they played a draw
player_1.elo_rating = player_1.updated_elo(player_2, 0.5)
player_2.elo_rating = player_2.updated_elo(player_1, 0.5)
```
