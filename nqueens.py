from charles.charles import Population, Individual
from copy import deepcopy
from charles.selection import tournament_sel, double_tournament, ranking
from charles.mutation import binary_mutation, swap_mutation, inversion_mutation
from charles.crossover import single_point_co, k_point_co, cycle_crossover, pmx
from random import random
from operator import attrgetter
from testfunctions import run_experiment, tournmanent_experiment, double_tournament_experiment, grid_search

import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.patches as mpatches




def get_fitness_regression(self):

    fitness = 5*self.deaths - 2.5*self.queens

    if self.deaths == self.queens:
        fitness *= self.n
    return fitness

def get_fitness_tuple(self):

     return (self.queens, self.deaths)


# monkey patching
Individual.get_fitness = get_fitness_regression



# # ################################################# first single tournament experiment #################################################

# tournament_exp = tournmanent_experiment([2,4,6,8,10],
#                                             n = 10, runs=100, pop_size=200, gens=30,
#                                             crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


# tournament_exp_avg = tournament_exp[1]
# tournament_exp_full = tournament_exp [0]


# ## making plot and getting the best infividuals

# fig, ax = plt.subplots(figsize=(9,5))

# track_dic_tourn1 = {}
# sizes_tourn1 = []
# bf_tourn1 = []
# f = open("results_final.txt", "a")
# f.write("tournament results\n\n")
# for i in range(len(tournament_exp_avg)):

#     sizes_tourn1.append(tournament_exp_avg[i]['size'])
#     bf_tourn1.append(min(tournament_exp_avg[i]['df'][('best_fitness','mean')]))

    
#     ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','mean')], label=tournament_exp_avg[i]['size'])
#     ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
#     ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
#     ax.legend(title='Tournament Size')
#     ax.fill_between(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
#     ax.set_xlabel('Generation',size = 14)
#     ax.set_ylabel('Best Fitness Found', size = 14)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)

# track_dic_tourn1['sizes'] = sizes_tourn1
# track_dic_tourn1['best_fitness_avg'] = bf_tourn1
# f.write(str(track_dic_tourn1)+'\n\n')
# track_dic_tourn1_df = pd.DataFrame(track_dic_tourn1)
# track_dic_tourn1_df.sort_values(by='best_fitness_avg', inplace=True)
# f.write(tabulate(track_dic_tourn1_df,tablefmt="github", headers='keys'))
# f.write('\n\n\n')
# plt.savefig('tournament_size2-10_2.png')
# f.close()

# # #plt.show()

# ################################################# second single tournament experiment #################################################

# tournament_exp_2 = tournmanent_experiment([7,8,9,10,11],
#                                               n = 10, runs=100, pop_size=200, gens=30,
#                                             crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


# tournament_exp_avg_2 = tournament_exp_2[1]

# fig, ax = plt.subplots(figsize=(9,5))

# track_dic_tourn2 = {}
# sizes_tourn2 = []
# bf_tourn2 = []
# f = open("results_final.txt", "a")
# f.write("tournament results part 2\n\n")
# for i in range(len(tournament_exp_avg)):

#     sizes_tourn2.append(tournament_exp_avg_2[i]['size'])
#     bf_tourn2.append(min(tournament_exp_avg_2[i]['df'][('best_fitness','mean')]))

    
#     ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','mean')], label=tournament_exp_avg_2[i]['size'])
#     ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
#     ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
#     ax.legend(title='Tournament Size')
#     ax.fill_between(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','lower_bound')], tournament_exp_avg_2[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
#     ax.set_xlabel('Generation',size = 14)
#     ax.set_ylabel('Best Fitness Found', size = 14)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)

# track_dic_tourn2['sizes'] = sizes_tourn2
# track_dic_tourn2['best_fitness_avg'] = bf_tourn2
# f.write(str(track_dic_tourn2)+'\n\n')
# track_dic_tourn2_df = pd.DataFrame(track_dic_tourn2).sort_values(by='best_fitness_avg')
# track_dic_tourn2_df.sort_values(by='best_fitness_avg', inplace=True)
# f.write(tabulate(track_dic_tourn2_df,tablefmt="github", headers='keys'))
# f.write('\n\n\n')
# plt.savefig('tournament_size7-11_2.png')
# f.close()




# # ######################################## making double tournament experiment ###########################################################

# double_tournament_parameters = {"t_size": [2,4,6],
#            "queens_t_size": [2, 4, 6] ,
#            "deaths_t_size": [2, 4, 6],
#            "switch":[True, False]
#            }

# double_tournament_exp = double_tournament_experiment(double_tournament_parameters,
#                                               n = 10, runs=30, pop_size=200, gens=30,
#                                             crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


# double_tournament_exp_avg = double_tournament_exp[1]

# track_dic_dtourn1 = {}
# t_sizes_dtourn1 = []
# queens_t_sizes_dtourn1 = []
# deaths_t_sizes_dtourn1 = []
# switch_dtourn1 = []
# bf_dtourn1 = []


# fig, ax = plt.subplots(figsize=(9,5))

# for i in range(len(double_tournament_exp_avg)):

#     t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['t_size'])
#     queens_t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['queens_t_size'])
#     deaths_t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['deaths_t_size'])
#     bf_dtourn1.append(min(double_tournament_exp_avg[i]['df'][('best_fitness','mean')]))
#     switch_dtourn1.append(double_tournament_exp_avg[i]['parameters']['switch'])

#     color = 'blue'

#     if double_tournament_exp_avg[i]['parameters']['switch'] == False:
#         color = 'red'
    
#     ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','mean')], color = color)
#     ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], color=color, alpha=0.1)
#     ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], color=color, alpha=0.1)
#     ax.fill_between(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], double_tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2, color = color)
#     ax.set_xlabel('Generation',size = 14)
#     ax.set_ylabel('Best Fitness Found', size = 14)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     red_patch = mpatches.Patch(color='red', label='False', linewidth=.1)
#     blue_patch = mpatches.Patch(color='blue', label='True',linewidth=.1)
#     ax.legend(handles=[red_patch, blue_patch], title = 'Switch')


# track_dic_dtourn1['t_size'] = t_sizes_dtourn1
# track_dic_dtourn1['queens_t_size'] = queens_t_sizes_dtourn1
# track_dic_dtourn1['deaths_t_size'] = deaths_t_sizes_dtourn1
# track_dic_dtourn1['switch'] = switch_dtourn1
# track_dic_dtourn1['best_fitness_avg'] = bf_dtourn1


# f = open("results_final.txt", "a")
# f.write("double tournament switch testing results\n\n")
# f.write(str(track_dic_dtourn1)+'\n\n')
# track_dic_dtourn1_df = pd.DataFrame(track_dic_dtourn1).sort_values(by='best_fitness_avg')
# track_dic_dtourn1_df.sort_values(by='best_fitness_avg', inplace=True)
# f.write(tabulate(track_dic_dtourn1_df,tablefmt="github", headers='keys'))
# f.write('\n\n\n')

# plt.savefig('doubletournament_switch_2.png')
# #plt.show()







# # ########################################### making double tournament experiment 2 #######################################################
# double_tournament_parameters_2 = {"t_size": [2,4,6,8,10],
#            "queens_t_size": [2,4,6,8,10] ,
#            "deaths_t_size": [2,4,6,8,10],
#            "switch":[False]
#            }

# double_tournament_exp_2 = double_tournament_experiment(double_tournament_parameters_2,
#                                               n = 10, runs=30, pop_size=200, gens=30,
#                                             crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)

# double_tournament_exp_avg_2 = double_tournament_exp_2[1]


# track_dic_dtourn2 = {}

# t_sizes_dtourn2 = []
# queens_t_sizes_dtourn2 = []
# deaths_t_sizes_dtourn2 = []
# bf_dtourn2 = []
# switch_dtourn2 = []

# for i in range(len(double_tournament_exp_avg_2)):

#     t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['t_size'])
#     queens_t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['queens_t_size'])
#     deaths_t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['deaths_t_size'])
#     bf_dtourn2.append(min(double_tournament_exp_avg_2[i]['df'][('best_fitness','mean')]))
#     switch_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['switch'])


# track_dic_dtourn2['t_size'] = t_sizes_dtourn2
# track_dic_dtourn2['queens_t_size'] = queens_t_sizes_dtourn2
# track_dic_dtourn2['deaths_t_size'] = deaths_t_sizes_dtourn2
# track_dic_dtourn2['switch'] = switch_dtourn2
# track_dic_dtourn2['best_fitness_avg'] = bf_dtourn2


# f = open("results_final.txt", "a")
# f.write("double tournament grid testing results\n\n")
# f.write(str(track_dic_dtourn2)+'\n\n')
# track_dic_dtourn2_df = pd.DataFrame(track_dic_dtourn2).sort_values(by='best_fitness_avg')
# track_dic_dtourn2_df.sort_values(by='best_fitness_avg', inplace=True)
# f.write(tabulate(track_dic_dtourn2_df,tablefmt="github", headers='keys'))
# f.write('\n\n\n')

# f.close()


########################################### final search for the best algorithm! #######################################################

grid_parameters = {'mutation': [binary_mutation, swap_mutation, inversion_mutation],
                   'mut_prob': [0.2,0.4,0.6,0.8,0.9],
                   'crossover': [single_point_co, k_point_co, cycle_crossover, pmx],
                   'xo_prob': [0.2,0.4,0.6,0.8,0.9],
                   'selection': [ranking, tournament_sel, double_tournament]
                }

# grid_parameters = {'mutation': [binary_mutation],
#                    'mut_prob': [0.2,0.4,0.6],
#                    'crossover': [single_point_co],
#                    'xo_prob': [0.2,0.4],
#                    'selection': [ranking]
#                 } #these were for testing purposes

grid_search_exp_final = grid_search(grid_parameters, 10)[0] #done for 10x10 chessboard
grid_search_exp_avg = grid_search(grid_parameters, 10)[1]


# lets start a list where we have the first 5 solutions; we want to plot only the best solutions.
best_list = grid_search_exp_avg[:5]

# function to sort the list of dictionaries by the best fitness of each dataframe inside the dictionary
def get_min_fitness(dictionary):
    df = dictionary['df']
    min_fitness = df[('best_fitness','mean')].min()
    return min_fitness

# Sort the list of dictionaries based on the minimum fitness value of the dataframes inside it
best_list_sorted = sorted(best_list, key=get_min_fitness)

# print([get_min_fitness(best_list_sorted[i]) for i in range(len(best_list_sorted))])

# run in every dict in the list 
for i in range(5, len(grid_search_exp_avg)):

    # see if the current dictionary has better final fitness than the worst in our list (the last element)
    if get_min_fitness(grid_search_exp_avg[i]) < get_min_fitness(best_list_sorted[-1]):

        best_list_sorted[-1] = grid_search_exp_avg[i]

    best_list_sorted.sort(key=get_min_fitness)

# print([get_min_fitness(best_list_sorted[i]) for i in range(len(best_list_sorted))])

track_dic_grid = {}

mutation_grid = []
mut_prob_grid = []
crossover_grid = []
co_prob_grid = []
selection_grid = []
bf_grid = []

fig, ax = plt.subplots(figsize=(12,7))

for i in range(len(best_list_sorted)):

    mutation_grid.append(best_list_sorted[i]['parameters']['mutation'].__name__)
    mut_prob_grid.append(best_list_sorted[i]['parameters']['mut_prob'])
    crossover_grid.append(best_list_sorted[i]['parameters']['crossover'].__name__)
    co_prob_grid.append(best_list_sorted[i]['parameters']['xo_prob'])
    selection_grid.append(best_list_sorted[i]['parameters']['selection'].__name__)
    bf_grid.append(min(best_list_sorted[i]['df'][('best_fitness','mean')]))

    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','mean')], 
            label = f"{best_list_sorted[i]['parameters']['mutation'].__name__},prob={best_list_sorted[i]['parameters']['mut_prob']};{best_list_sorted[i]['parameters']['crossover'].__name__},prob={best_list_sorted[i]['parameters']['xo_prob']};{best_list_sorted[i]['parameters']['selection'].__name__}")
    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.fill_between(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','lower_bound')], best_list_sorted[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()


track_dic_grid['mutation'] = mutation_grid
track_dic_grid['mut_prob'] = mut_prob_grid
track_dic_grid['crossover'] = crossover_grid
track_dic_grid['xo_prob'] = co_prob_grid
track_dic_grid['selection'] = selection_grid
track_dic_grid['best_fitness_avg'] = bf_grid


f = open("results_final_grid.txt", "a")
f.write("Final grid search testing results\n\n")
f.write(str(track_dic_grid)+'\n\n')
track_dic_grid_df = pd.DataFrame(track_dic_grid).sort_values(by='best_fitness_avg')
track_dic_grid_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_grid_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()

plt.savefig('final_grid.png')
plt.show()