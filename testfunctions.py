import pandas as pd
from charles.charles import Population
from charles.selection import tournament_sel, double_tournament

import itertools


############################################# function for running any experiment ###############################################

def run_experiment(n, runs, pop_size, crossover_prob, mutation_prob, selection, mutation, crossover, gens, t_size = None,queens_t_size=None,deaths_t_size=None, switch = None):

    df = pd.DataFrame()

    for run in range(runs):
        print('run', run+1)

        df_temp = None
        df_temp = pd.DataFrame()

        best_indvs_fit = []
        best_indvs_queens = []
        best_indvs_deaths = []
        best_indvs_rep = []

        pop = None
    
        pop = Population(size = pop_size, optim="min", sol_size=n*n, valid_set=[0, 1], replacement=True)

        pop.evolve(gens=gens, xo_prob=crossover_prob, mut_prob=mutation_prob, select=selection,
                 mutate=mutation, crossover=crossover,
                 elitism=True, tournament_size=t_size, queens_tournament_size=queens_t_size, deaths_tournament_size=deaths_t_size, switch=switch)
        
        best_indvs_fit = [i.fitness for i in pop.bestindvs]
        best_indvs_queens = [i.queens for i in pop.bestindvs]
        best_indvs_deaths = [i.deaths for i in pop.bestindvs]
        best_indvs_rep = [i.representation for i in pop.bestindvs]


        df_temp['run'] = [run+1]*gens
        df_temp['gens'] = range(1,gens+1)
        df_temp['crossover'] = crossover.__name__
        df_temp['xo_prob'] = crossover_prob
        df_temp['mutate'] = mutation.__name__
        df_temp['mut_prob'] = mutation_prob
        df_temp['select'] = selection.__name__
        df_temp['tournament_size'] = t_size
        df_temp['deaths_tournament_size'] = deaths_t_size
        df_temp['queens_tournament_size'] = queens_t_size
        df_temp['best_fitness'] = best_indvs_fit
        df_temp['queens']= best_indvs_queens
        df_temp['deaths'] = best_indvs_deaths
        df_temp['best_representation'] = best_indvs_rep

        df = pd.concat([df, df_temp])

    return df



############################################# function for running single tournament experiments ###############################################
def tournmanent_experiment(sizes, n, runs, pop_size, crossover_prob, mutation_prob, mutation, crossover, gens):

    df_final = []

    df_final_med = []

    for size in sizes:

        print('\nTesting tournament size', size)
        #print(size)

        data = run_experiment(n = n, runs = runs, pop_size = pop_size, crossover_prob=crossover_prob, mutation_prob=mutation_prob, mutation = mutation, crossover=crossover, gens=gens, t_size=size, selection=tournament_sel)

        df_final.append({'tournament_size': size, 'data': data})
    
        df_med = data.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).agg({'queens': ['min', 'mean', 'max','std'],'deaths': ['min', 'mean', 'max','std'], 'best_fitness': ['min', 'mean', 'max','std']})
        df_med[('queens', 'lower_bound')] = df_med[('queens', 'mean')] - (df_med[('queens', 'std')])/2
        df_med[('queens', 'upper_bound')] = df_med[('queens', 'mean')] + (df_med[('queens', 'std')])/2
        df_med[('deaths', 'lower_bound')] = df_med[('deaths', 'mean')] - (df_med[('deaths', 'std')])/2
        df_med[('deaths', 'upper_bound')] = df_med[('deaths', 'mean')] + (df_med[('deaths', 'std')])/2
        df_med[('best_fitness', 'lower_bound')] = df_med[('best_fitness', 'mean')] - (df_med[('best_fitness', 'std')])/2
        df_med[('best_fitness', 'upper_bound')] = df_med[('best_fitness', 'mean')] + (df_med[('best_fitness', 'std')])/2


        df_final_med.append({'size':size, 'df': df_med})

    return df_final, df_final_med


################################## double tournament exp #


def double_tournament_experiment(pars,n, runs, pop_size, crossover_prob, mutation_prob, mutation, crossover, gens):

    df_final = []

    df_final_med = []

    keys=pars.keys()

    combinations=itertools.product(*pars.values())
    
    ds=[dict(zip(keys,cc)) for cc in combinations]
    print(ds)
    i = 0

    for dictionary in ds: 

        print(dictionary)

        if dictionary["switch"] == True and dictionary["deaths_t_size"] < dictionary["queens_t_size"]:
            print("continue")
            continue
        elif dictionary["switch"] == False and dictionary["deaths_t_size"] > dictionary["queens_t_size"]:
            print("continue")
            continue 

        

        data = run_experiment(n = n, runs = runs, gens = gens, pop_size = pop_size, crossover_prob = crossover_prob,
                                                mutation_prob = mutation_prob, 
                                                selection = double_tournament, 
                                                t_size = dictionary['t_size'],
                                                queens_t_size=dictionary['queens_t_size'],
                                                deaths_t_size=dictionary['deaths_t_size'],
                                                switch=dictionary['switch'],
                                                mutation = mutation,
                                                crossover = crossover)
        
        df_final.append({'parameters': dictionary, 'data': data})

        
        df_med = data.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).agg({'queens': ['min', 'mean', 'max','std'],'deaths': ['min', 'mean', 'max','std'], 'best_fitness': ['min', 'mean', 'max','std']})
        df_med[('queens', 'lower_bound')] = df_med[('queens', 'mean')] - (df_med[('queens', 'std')])/2
        df_med[('queens', 'upper_bound')] = df_med[('queens', 'mean')] + (df_med[('queens', 'std')])/2
        df_med[('deaths', 'lower_bound')] = df_med[('deaths', 'mean')] - (df_med[('deaths', 'std')])/2
        df_med[('deaths', 'upper_bound')] = df_med[('deaths', 'mean')] + (df_med[('deaths', 'std')])/2
        df_med[('best_fitness', 'lower_bound')] = df_med[('best_fitness', 'mean')] - (df_med[('best_fitness', 'std')])/2
        df_med[('best_fitness', 'upper_bound')] = df_med[('best_fitness', 'mean')] + (df_med[('best_fitness', 'std')])/2


        df_final_med.append({'parameters':dictionary, 'df': df_med})


    return df_final, df_final_med

##################################################################### grid search ########################################################

def grid_search(pars, n):
    df_final = []

    df_final_med = []

    keys=pars.keys()
    combinations=itertools.product(*pars.values())
    ds=[dict(zip(keys,cc)) for cc in combinations]

    i = 0

    for dictionary in ds: 
        print(dictionary)

        data = run_experiment(n = n,runs=30, pop_size = 200, crossover_prob = dictionary["xo_prob"],
                                                mutation_prob = dictionary['mut_prob'], 
                                                selection = dictionary['selection'], 
                                                mutation = dictionary['mutation'],
                                                crossover = dictionary['crossover'], gens=30)



        df_final.append({'parameters': dictionary, 'data': data})

        df_med = data.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).agg({'queens': ['min', 'mean', 'max','std'],'deaths': ['min', 'mean', 'max','std'], 'best_fitness': ['min', 'mean', 'max','std']})
        df_med[('queens', 'lower_bound')] = df_med[('queens', 'mean')] - (df_med[('queens', 'std')])/2
        df_med[('queens', 'upper_bound')] = df_med[('queens', 'mean')] + (df_med[('queens', 'std')])/2
        df_med[('deaths', 'lower_bound')] = df_med[('deaths', 'mean')] - (df_med[('deaths', 'std')])/2
        df_med[('deaths', 'upper_bound')] = df_med[('deaths', 'mean')] + (df_med[('deaths', 'std')])/2
        df_med[('best_fitness', 'lower_bound')] = df_med[('best_fitness', 'mean')] - (df_med[('best_fitness', 'std')])/2
        df_med[('best_fitness', 'upper_bound')] = df_med[('best_fitness', 'mean')] + (df_med[('best_fitness', 'std')])/2


        df_final_med.append({'parameters':dictionary, 'df': df_med})


    return df_final, df_final_med