from pathlib import Path

COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}


def calc_energy():
    pass


def doing_it_by_hand():
    """
    #############
    #...........#
    ###C#B#A#D###
      #B#C#D#A#
      #########
      D2+A7+A9+D3+D5+C7+B2+C5+B3+B5+A3+A3
      2000+7+9+3000+5000+700+20+500+30+3+3+50 = 11322 -> too high
      2000+7+9+3000+5000+700+20+500+30+3+3    = 11272-> too low
      11300 -> too low
      11311 -> incorrect
      11320 -> correct

    D2+A7+A9+D3+D5+C7+B2+C5+B3+B5+A3+A3
    #############
    #AA.........#
    ###.#B#C#D###
      #.#B#C#D#
      #########
    """
    return 11320


data = Path(__file__).with_name("input_ex.txt").read_text()

assert calc_energy() == 12521


data = Path(__file__).with_name("input.txt").read_text()
