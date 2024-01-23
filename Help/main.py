from ReadAminoAcidJsonFileExceptForTrp import *
import FitnessFunction as ff
import random

def get_Aminoacids_information():
    with open("AminoAcids/M.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    M_Amino = ReadJsonFile(data)
    with open("AminoAcids/F.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    F_Amino = ReadJsonFile(data)
    with open("AminoAcids/K.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    K_Amino = ReadJsonFile(data)
    with open("AminoAcids/C.json", 'r') as file:
        json_data = file.read()
    data = json.loads(json_data)
    C_Amino = ReadJsonFile(data)
    ResNames = ["Met", "Phe", "Lys", "Cys"]
    return M_Amino,F_Amino,K_Amino,C_Amino,ResNames

def RandomInput(FitnessFunctionObj):
    return ([random.choice([0,1]) for _ in range(FitnessFunctionObj.HowManyCombinationsCanWeHave)],
            [random.randint(0,360) for _ in range(6*len(FitnessFunctionObj.SequenceOfAminoObjects))])

def RandomInputForSulfur(FitnessFunctionObj):
    return [random.choice([0,1]) for _ in range(FitnessFunctionObj.HowManyCombinationsCanWeHaveForSulfur)]
    
def get_fitness(energy):
    return abs(energy)
    
def sample1_indiv_fitness(FitnessFunctionObj):
    HowTheyCombined = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1]
    HowRotationAndDeltaOccured = [127, 242, 177, 268, 174, 260, 319, 353, 288, 348, 344, 231, 220,
                                  311, 64, 187, 221, 216, 209, 130, 101, 120, 128, 260]

    indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(HowTheyCombined,
     HowRotationAndDeltaOccured, SulfurCombinations=[0, 1]))
    print("Sample fitness: "+str(indiv_fitness))
    
def sample2_indiv_fitness(FitnessFunctionObj):
    HowTheyCombined = [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0]
    HowRotationAndDeltaOccured = [65, 70, 300, 200, 10, 20, 110, 230, 300, 20, 20, 600, 290, 120,
                                  260, 100, 290, 600, 100, 220, 190, 700, 400, 120]
    indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(HowTheyCombined,
     HowRotationAndDeltaOccured, SulfurCombinations=[0, 1]))
    print("Sample fitness: "+str(indiv_fitness)) 
    
def sample3_indiv_fitness(FitnessFunctionObj):

    HowTheyCombined = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1]
    HowRotationAndDeltaOccured = [415.000001, 136.00000002, 420.0008827, 308.000001, 366.999, 264.9997718,
                                  179, 350, 292.000000000006, 464, 247, 330, 204, 366, 264, 180, 427, 464,
                                  203, 368, 263, 155, 414, 196.99995088]
    indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(HowTheyCombined,
     HowRotationAndDeltaOccured, SulfurCombinations=[0, 1]))   
    print("Sample fitness {:.17f}".format(indiv_fitness)) 

def tempinput_indiv_fitness(FitnessFunctionObj):
    HowTheyCombined, HowRotationAndDeltaOccured = FitnessFunctionObj.TempInput()
    indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(HowTheyCombined,
     HowRotationAndDeltaOccured, SulfurCombinations=[0, 1]))
    print("Sample fitness: "+str(indiv_fitness))

def rand_indiv_fitness(FitnessFunctionObj):
    HowTheyCombined, HowRotationAndDeltaOccured = RandomInput(FitnessFunctionObj)
    indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(HowTheyCombined,
     HowRotationAndDeltaOccured, SulfurCombinations=[0, 1]))
    print("Sample fitness: "+str(indiv_fitness))

def generate_population(FitnessFunctionObj, population_size):
    popu = []
    for _ in range(population_size):
        HowTheyCombined, HowRotationAndDeltaOccured = RandomInput(FitnessFunctionObj)
        chromosome = [HowTheyCombined, HowRotationAndDeltaOccured]
        popu.append(chromosome)
    return popu

def generate_population_with_fixed_Combination(FitnessFunctionObj, population_size, fixed_Combination):
    popu = []
    for _ in range(population_size):    
        _ , HowRotationAndDeltaOccured  = RandomInput(FitnessFunctionObj)
        chromosome = [fixed_Combination, HowRotationAndDeltaOccured]
        popu.append(chromosome)
    return popu

def generate_population_with_fixed_RotationAndDelta(FitnessFunctionObj, population_size, fixed_RotationAndDelta):
    popu = []
    for _ in range(population_size):
        HowTheyCombined , _ = RandomInput(FitnessFunctionObj)
        chromosome = [HowTheyCombined, fixed_RotationAndDelta]
        popu.append(chromosome)
    return popu

def generate_population_with_fixed_Combination_and_RotationAndDelta(
        FitnessFunctionObj, population_size, fixed_RotationAndDelta, fixed_Combination):
    popu = []
    for _ in range(population_size):
        SulfurCombinations = RandomInputForSulfur(FitnessFunctionObj)
        chromosome = [fixed_Combination, fixed_RotationAndDelta,SulfurCombinations]
        popu.append(chromosome)
    return popu

def get_populationfitness_dic(popu):
    population_dic = []
    for indiv in popu:
        HowTheyCombined = indiv[0]
        HowRotationAndDeltaOccured = indiv[1]
        indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(indiv[0],indiv[1],SulfurCombinations=[0, 1]))
        population_dic.append((indiv,indiv_fitness))
    return population_dic

def get_populationfitness_dic_with_SulfurCombinations(popu):
    population_dic = []
    for indiv in popu:
        HowTheyCombined = indiv[0]
        HowRotationAndDeltaOccured = indiv[1]
        SulfurCombinations = indiv[2]
        indiv_fitness = get_fitness(FitnessFunctionObj.caculateEnergy(indiv[0],indiv[1],indiv[2]))
        population_dic.append((indiv,indiv_fitness))
    return population_dic

def fit_population(population_dic,n):
    # it selects nth fittest
    sorted_population_dic = sorted(
        population_dic,
        key=lambda x: x[1]
    )
    nfit_population = []
    for i in range(n):
        nfit_population.append(sorted_population_dic[i][0])
    return nfit_population

def pair_random(parent_pool):
    parent_pairs = []
    while len(parent_pool) != 0:
        idx0 = random.randrange(0, len(parent_pool))
        parent_0 = parent_pool[idx0]
        parent_pool.remove(parent_0)
        idx1 = random.randrange(0, len(parent_pool))
        parent_1 = parent_pool[idx1]
        parent_pool.remove(parent_1)
        parent_pairs.append((parent_0, parent_1))
        # print("-----------------------------------")
    return parent_pairs
    
def send_noise(fitness):
    noise = 0
    if fitness >   40000000:
       noise = random.randint(0,45) 
    elif fitness > 20000000:
       noise = random.randint(0,41) 
    elif fitness > 10000000:
       noise = random.randint(0,37) 
    elif fitness > 5000000:
       noise = random.randint(0,34) 
    elif fitness > 1000000:
       noise = random.randint(0,30)
    elif fitness > 500000:
       noise = random.randint(0,25)  
    elif fitness > 100000:
       noise = random.randint(0,20)
    elif fitness > 70000:
       noise = random.randint(0,15) 
    elif fitness > 40000:
       noise = random.randint(0,13)
    elif fitness > 20000:
       noise = random.randint(0,11)
    elif fitness > 10000:
       noise = random.randint(0,10)
    elif fitness > 4000:
       noise = random.randint(0,8)
    elif fitness > 1000:
       noise = random.randint(0,6)
    elif fitness > 400:
       noise = random.randint(0,4)
    elif fitness > 100:
       noise = random.randint(0,2)
    elif fitness > 20:
       noise = random.randint(0,1)
    elif fitness > 2:
       noise = round(random.uniform(-0.1,0.1),2)
    else:
       noise = round(random.uniform(-0.01,0.01),3)
    return noise
      
def recombination(parents_pair,fixed_Combination, Pc):
    off_springs_RotationAndDelta = []
    off_springs = []
    for parents in parents_pair:
        if random.uniform(0, 1) < Pc:
            cross_over_point1 = len(parents[0][1]) / 2
            off_spring0_RotationAndDelta = []
            off_spring1_RotationAndDelta = []
            
            for i in range(len(parents[0][1])):
                if i < cross_over_point1:
                    off_spring0_RotationAndDelta.append(parents[0][1][i])
                    off_spring1_RotationAndDelta.append(parents[1][1][i])
                else:
                    off_spring0_RotationAndDelta.append(parents[1][1][i])
                    off_spring1_RotationAndDelta.append(parents[0][1][i])
            off_springs_RotationAndDelta.append(off_spring0_RotationAndDelta)
            off_springs_RotationAndDelta.append(off_spring1_RotationAndDelta)
        else:
            off_springs_RotationAndDelta.append(parents[0][1])
            off_springs_RotationAndDelta.append(parents[1][1])
    
    for ofs_rd in off_springs_RotationAndDelta:
        off_springs.append([fixed_Combination,ofs_rd])
    return off_springs

def mutation(offsprs, Pm, fitness):
    for offspring in offsprs:
        for i in range(len(offspring[1])):
            if random.uniform(0, 1) < Pm:
                offspring[1][i] += send_noise(fitness)
    return offsprs

def recombination1(parents_pair,fixed_RotationAndDelta, Pc):
    off_springs_Combination = []
    off_springs = []
    for parents in parents_pair:
        if random.uniform(0, 1) < Pc:
            cross_over_point1 = len(parents[0][0]) / 2
            off_spring0_Combination = []
            off_spring1_Combination = []
            
            for i in range(len(parents[0][0])):
                if i < cross_over_point1:
                    off_spring0_Combination.append(parents[0][0][i])
                    off_spring1_Combination.append(parents[1][0][i])
                else:
                    off_spring0_Combination.append(parents[1][0][i])
                    off_spring1_Combination.append(parents[0][0][i])
            off_springs_Combination.append(off_spring0_Combination)
            off_springs_Combination.append(off_spring1_Combination)
        else:
            off_springs_Combination.append(parents[0][0])
            off_springs_Combination.append(parents[1][0])
    
    for ofs_c in off_springs_Combination: 
        off_springs.append([ofs_c,fixed_RotationAndDelta])
    return off_springs

def mutation1(offsprs, Pm):
    for offspring in offsprs:
        for i in range(len(offspring[0])):
            if random.uniform(0, 1) < Pm:
               if offspring[0][i] == 1:
                  offspring[0][i] = 0
               elif offspring[0][i] == 0:
                  offspring[0][i] = 1
               else:
                  print("it shouldnt be here")
    return offsprs

def recombination2(parents_pair,fixed_RotationAndDelta,fixed_Combination, Pc):
    off_springs_SulfurCombination = []
    off_springs = []
    for parents in parents_pair:
        if random.uniform(0, 1) < Pc:
            cross_over_point1 = len(parents[0][2]) / 2
            off_spring0_SulfurCombination = []
            off_spring1_SulfurCombination = []
            
            for i in range(len(parents[0][2])):
                if i < cross_over_point1:
                    off_spring0_SulfurCombination.append(parents[0][2][i])
                    off_spring1_SulfurCombination.append(parents[1][2][i])
                else:
                    off_spring0_SulfurCombination.append(parents[1][2][i])
                    off_spring1_SulfurCombination.append(parents[0][2][i])
            off_springs_SulfurCombination.append(off_spring0_SulfurCombination)
            off_springs_SulfurCombination.append(off_spring1_SulfurCombination)
        else:
            off_springs_SulfurCombination.append(parents[0][2])
            off_springs_SulfurCombination.append(parents[1][2])
    
    for ofs_sc in off_springs_SulfurCombination: 
        off_springs.append([fixed_Combination,fixed_RotationAndDelta,ofs_sc])
    return off_springs

def mutation2(offsprs, Pm):
    for offspring in offsprs:
        for i in range(len(offspring[2])):
            if random.uniform(0, 1) < Pm:
               if offspring[2][i] == 1:
                  offspring[2][i] = 0
               elif offspring[2][i] == 0:
                  offspring[2][i] = 1
               else:
                  print("it shouldnt be here")
    return offsprs
    

def train_RotationAndDelta(generation,found,mio,llambda,Pc,Pm,max_number_of_generation,fixed_Combination):
    population = generate_population_with_fixed_Combination(FitnessFunctionObj, 100,fixed_Combination)
    population_dic = get_populationfitness_dic(population)
    population = fit_population(population_dic,llambda)
    fitnesses1 = []
    best_answer = population[0]
    while generation <= max_number_of_generation and not found:
          best_indiv = population[0]
          HowTheyCombined = best_indiv[0]
          HowRotationAndDeltaOccured = best_indiv[1]
          energy = FitnessFunctionObj.caculateEnergy(best_indiv[0],best_indiv[1], SulfurCombinations=[0, 1])
          fitness = get_fitness(energy)
          fitnesses1.append(fitness)
          print("generation: " + str(generation))
          print("best individual: " + str(best_indiv[0]))
          print(best_indiv[1]) 
          print("best individual fitness: " + str(fitness))        
          print("================================================================================="
                "================================================================")
          generation +=1
          parent_pool = random.sample(population, mio)
          parents_pair = pair_random(parent_pool)
          offsprs = recombination(parents_pair,fixed_Combination, Pc)
          offsprs = mutation(offsprs, Pm, fitness)
          population_dic = get_populationfitness_dic(population + offsprs)
          population = fit_population(population_dic,llambda)
          if fitness < 1 :
             found = True
    return best_indiv[1]

def train_combination(generation,found,mio,llambda,Pc,Pm,max_number_of_generation,fixed_RotationAndDelta):
    population = generate_population_with_fixed_RotationAndDelta(FitnessFunctionObj, 100,fixed_RotationAndDelta)
    population_dic = get_populationfitness_dic(population)
    population = fit_population(population_dic,llambda)
    population[0][0] = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1]
    fitnesses2 = []
    while generation <= max_number_of_generation and not found:
          best_indiv = population[0]
          HowTheyCombined = best_indiv[0]
          HowRotationAndDeltaOccured = best_indiv[1]
          energy = FitnessFunctionObj.caculateEnergy(best_indiv[0],best_indiv[1], SulfurCombinations=[0, 1])
          fitness = get_fitness(energy)
          fitnesses2.append(fitness)
          print("generation: " + str(generation))
          print("best individual: " + str(best_indiv[0]))
          print(best_indiv[1]) 
          print("best individual fitness: " + str(fitness))        
          print("============================================================================"
                "=====================================================================")
          generation +=1
          parent_pool = random.sample(population, mio)
          parents_pair = pair_random(parent_pool)
          offspr = recombination1(parents_pair,fixed_RotationAndDelta, Pc)
          offspr = mutation1(offspr, Pm)
          population_dic = get_populationfitness_dic(population + offspr)
          population = fit_population(population_dic,llambda)
    return best_indiv[0]

def train_sulfurcomb(generation,found,mio,llambda,Pc,Pm,max_number_of_generation,
                     fixed_Combination,fixed_RotationAndDelta):
    population = generate_population_with_fixed_Combination_and_RotationAndDelta(FitnessFunctionObj, 100,
     fixed_RotationAndDelta, fixed_Combination)
    population_dic_SulfurCombinations = get_populationfitness_dic(population)
    population = fit_population(population_dic_SulfurCombinations,llambda)
    fitnesses3 = []
    while generation <= max_number_of_generation and not found:
          best_indiv = population[0]
          HowTheyCombined = best_indiv[0]
          HowRotationAndDeltaOccured = best_indiv[1]
          SulfurCombination = best_indiv[2]
          energy = FitnessFunctionObj.caculateEnergy(best_indiv[0],best_indiv[1], best_indiv[2])
          fitness = get_fitness(energy)
          fitnesses3.append(fitness)
          print("generation: " + str(generation))
          print("best individual: " + str(best_indiv[0]))
          print(best_indiv[1])
          print(best_indiv[2])
          print("best individual fitness: " + str(fitness))        
          print("==========================================================================="
                "======================================================================")
          generation +=1
          parent_pool = random.sample(population, mio)
          parents_pair = pair_random(parent_pool)
          offspr = recombination2(parents_pair,fixed_RotationAndDelta,fixed_Combination, Pc)
          offspr = mutation2(offspr, Pm)
          population_dic_SulfurCombinations = get_populationfitness_dic(population + offspr)
          population = fit_population(population_dic_SulfurCombinations,llambda)
    return best_indiv[2]

  
if __name__=="__main__":
    M_Amino,F_Amino,K_Amino,C_Amino,ResNames = get_Aminoacids_information()
    FitnessFunctionObj = ff.FitnessFunction([M_Amino, F_Amino, K_Amino, C_Amino], ResNames)    
       
       
    fixed_RotationAndDelta = RandomInput(FitnessFunctionObj)[1]
    HowTheyCombined = train_combination(generation= 1,found= False,mio= 20,llambda= 20,Pc= 0.8,Pm= 0.05,
      max_number_of_generation=30,fixed_RotationAndDelta=fixed_RotationAndDelta)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    
    
    fixed_Combination = HowTheyCombined
    HowRotationAndDeltaOccured = train_RotationAndDelta(generation= 1,found= False,mio= 20,llambda= 20,
      Pc= 0.8,Pm= 0.07,max_number_of_generation=3000,fixed_Combination=fixed_Combination)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    
    
    fixed_RotationAndDelta = HowRotationAndDeltaOccured
    SulfurCombinations = train_sulfurcomb(generation= 1,found= False,mio= 20,llambda= 20,Pc= 0.08,
      Pm= 0.05,max_number_of_generation=30, fixed_Combination=fixed_Combination,
                                          fixed_RotationAndDelta=fixed_RotationAndDelta)
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
   
   
    #rand_indiv_fitness(FitnessFunctionObj)
    #tempinput_indiv_fitness(FitnessFunctionObj)
    #sample1_indiv_fitness(FitnessFunctionObj)  
