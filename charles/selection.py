from random import uniform, choice, sample, Random
from operator import attrgetter
from .charles import Individual


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        
        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += total_fitness - individual.fitness
            if position > spin:
                return individual


    else:
        raise Exception("No optimization specified (min or max).")




def tournament_sel(population, tournament_size=9):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(tournament_size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
    





def double_tournament(population, tournament_size=10, queens_tournament_size=6, deaths_tournament_size=2, switch=False):
    rng = Random()

    if switch and deaths_tournament_size >= queens_tournament_size:
        queens_winners = []

        for i in range(deaths_tournament_size):
            queens_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            queens_winners.append(max([population[i] for i in queens_candidates], key=lambda x: x.get_queens()))

        death_candidates = [rng.randint(0, len(queens_winners) - 1) for i in range(queens_tournament_size)]
        winner = min([queens_winners[i] for i in death_candidates], key=lambda x: x.get_deaths())

        return winner

    elif not switch and queens_tournament_size >= deaths_tournament_size:
        death_winners = []

        for i in range(queens_tournament_size):
            death_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            death_winners.append(min([population[i] for i in death_candidates], key=lambda x: x.get_deaths()))

        queens_candidates = [rng.randint(0, len(death_winners) - 1) for i in range(deaths_tournament_size)]
        winner = max([death_winners[i] for i in queens_candidates], key=lambda x: x.get_queens())
        return winner

    else:
        if switch and deaths_tournament_size < queens_tournament_size:
            raise ValueError("Switch is True so queens size can't be bigger than deaths size")
        else:
            raise ValueError("Deaths size can't be bigger than queens size")



def ranking(population):


    if population.optim == "max":

        #[10,3,7,1]

        # Sum acumulated rank nrs
        total_rank_sum = sum([rank for rank in range(1, population.size+1)]) # 10
      
        # make a sorted list of fitness - because it is maximization it is not inverted so the best is the last as it should
        fitness_rank = sorted([individual for individual in population], key = lambda ind : ind.fitness, reverse = False) #[1,3,7,10]

        # Get a 'position' on the wheel
        spin = uniform(0, total_rank_sum)
        position = 0

        # Find individual in the position of the spin
        for individual in population:
            position += fitness_rank.index(individual)+1 # sum the individual's rank, given by the fitness rank list
            if position > spin:
                return individual


    elif population.optim == "min":

        #[10,3,7,1]

        # Sum acumulated rank nrs
        total_rank_sum = sum([rank for rank in range(1, population.size+1)]) # 10

        # make a sorted list of fitness - because it is minimization it is inverted so the best is the last
        fitness_rank = sorted([individual for individual in population], key = lambda ind : ind.fitness, reverse = True) #[10,7,3,1]

        # Get a 'position' on the wheel
        spin = uniform(0, total_rank_sum)
        position = 0

        # Find individual in the position of the spin
        for individual in population:
            position += fitness_rank.index(individual)+1 #  sum the individual's rank, given by the fitness rank list
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")

