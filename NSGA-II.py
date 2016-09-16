import random
import math
import functools

class Genotype:
    def __init__(self, gene = 0):
        self.gene = gene

class Fenotype:
    def __init__(self, genotype = Genotype()):
        g = genotype.gene #entre el tamaño de intervalo + la cota minima / 2 a la n
        _g = integerToString(int(g),int(g))
        n = len(_g[0])
        g = g / math.pow( 2,n)
        self.objectives = [ g*10 + 2 , math.sin(g* 10 + 2)]

class Individual:
    def __init__(self, name = "" , genotype = Genotype()):
        self.n = 0
        self.s = set([])
        self.rank = 0 #Variable de rank. que se aplicará en el fast non dominated sort
        self.name = name
        self.crowdingDistance = 0
        self.genotype = genotype
        self.fenotype = Fenotype(genotype)
    def __lt__(self, other):
        return crowdedComparisonOperator(self, other) == False
    def __gt__(self, other):
        return crowdedComparisonOperator(self, other) == True
    def __eq__(self, other):
        return crowdedComparisonOperator(self, other) == True
    def __le__(self, other):
        return crowdedComparisonOperator(self, other) == False
    def __ge__(self, other):
        return crowdedComparisonOperator(self, other) == True
    def __ne__(self, other):
        return crowdedComparisonOperator(self, other) == False
    def __key(self):
        return (self.genotype.gene)
    def __eq__(x, y):
        return x.__key() == y.__key()
    def __hash__(self):
        return hash(self.__key())

def dominates(individualA, individualB):
    '''
        Dominates
            Regresa si A domina a B. Si a es mejor en al menos uno y no es peor en ninguno.
    '''
    a = False
    for i in range(0, len(individualA.fenotype.objectives)):
        if isWorse(individualA.fenotype.objectives[i], individualB.fenotype.objectives[i]):
            return False
        if isBetter(individualA.fenotype.objectives[i], individualB.fenotype.objectives[i]):
            a = True
    return a

def isBetter(a, b):
    '''
        ¿Is Better?
            Regresa si a es mejor que b.
    '''
    if(a>b):
        return True
    else:
        return False

def isWorse(a, b):
    '''
        ¿Is Worse?
            Regresa si a es peor que b.
    '''
    if(a<b):
        return True
    else:
        return False

def fastNonDominatedSort(population):
    '''
       Fast NonDominated Sort
            Recibe a la población y regresa una lista con las fronteras de la población.
            Asigna a los individuos:
                n
                s
                rank
    '''
    f = []
    f.append(set([]))
    for individualA in population:
        #print(individualA.name)
        for individualB in population:
            #print("\t",individualB.name)
            if dominates(individualA, individualB):
                individualA.s = individualA.s | set([individualB])
            elif dominates(individualB, individualA):
                individualA.n = individualA.n + 1
        if individualA.n == 0: #if np == 0:
            f[0] = f[0] | set([individualA])
    i = 0
    while( len(f[i]) != 0 ):
        h = set([])
        for p in f[i]:
            for q in p.s: #for q in sp:
                q.n = q.n - 1
                if q.n == 0:
                    h = h | set([q])
                    q.rank = i + 1 #Agrega el atributo de rank en el individuo...
        i = i + 1
        f.append(h) #f[i] = h
    return f

def crowdingDistanceAssigment(frontera): #LISTO
    '''
        Crowding Distance Assigment
    '''
    frontera = list(frontera)
    length = len(frontera)
    for individual in frontera:
        individual.crowdingDistance = 0
    for objective in Individual().fenotype.objectives:
        objectiveindex = Individual().fenotype.objectives.index(objective)
        frontera.sort(key=lambda x: x.fenotype.objectives[objectiveindex])
        frontera = sorted(frontera, key=lambda x: x.fenotype.objectives[objectiveindex])
        if(len(frontera)>0):
            frontera[0].crowdingDistance = float("inf")
            frontera[length - 1].crowdingDistance = float("inf")
            for i in range(2, length - 1):
                frontera[i].crowdingDistance = frontera[i].crowdingDistance + (frontera[i + 1].fenotype.objectives[objectiveindex] - frontera[i - 1].fenotype.objectives[objectiveindex])
    return frontera

def crowdedComparisonOperator(individualA, individualB): #LISTO
    '''
        Crowded Comparison Operator
    '''
    rank_i = individualA.rank
    rank_j = individualB.rank
    distance_i = individualA.crowdingDistance
    distance_j = individualB.crowdingDistance
    if rank_i<rank_j or ((rank_i == rank_j) and (distance_i > distance_j)):
        return True
    return False

def crossover(str1, str2):
    '''
        Crossover
            Recibe dos cadenas de genes codificados y regresa dos hijos producidos a partir de esas cadenas. Depende de CROSSOVER_RATE y utiliza CHROMO_LEN.
    '''
    # crosses over two chromosomes at a random location
    CROSSOVER_RATE = .8
    if (random.random() < CROSSOVER_RATE):
        cr = random.randint(0, len(str1) - 1)
        tmp1 = str2[0:cr] + str1[cr:]
        tmp2 = str1[0:cr] + str2[cr:]
    else:
        tmp1 = str1
        tmp2 = str2
    return [tmp1, tmp2]

def mutate(str1):
    '''
        Mutate
            Recibe la cadena del gen codificado y regresa mutación coorrespondiente. Depende de la constante MUTATION_RATE y utiliza CHROMO_LEN.
    '''
    MUTATION_RATE = 0.1
    tmp1 = ""
    for i in range(len(str1)):
        if (random.random() < MUTATION_RATE):
            if (str1[i] == '1'):
                tmp1 += "0"
            else:
                tmp1 += "1"
        else:
            tmp1 += str1[i]
    return tmp1

def integerToString(numero,numero2):
    '''
        Binary to String
            Recibe dos numeros decimales y regresa las cadenas de la codificacion binaria.
    '''
    cadenas = []
    cadenas.append(bin(numero))
    cadenas.append(bin(numero2))
    #Limpiar las cadenas
    cadenas[0] = cadenas[0].replace("0b","")
    cadenas[1] = cadenas[1].replace("0b","")
    if (len(cadenas[0]) > len(cadenas[1])):
        cadenas[1] = ("0"*(len(cadenas[0])-len(cadenas[1]))) + cadenas[1]
    else:
        cadenas[0] = ("0"*(len(cadenas[1])-len(cadenas[0]))) + cadenas[0]
    return cadenas[0], cadenas[1]

def stringToInteger(cadena):
    '''
        Binary to Integer
            Recibe una cadena en binario y regresa el valor decodificado a decimal.
    '''
    decimal = 0
    for i,v in enumerate(cadena):
        if(v == '1'):
            decimal = decimal + math.pow(2,len(cadena)-1-i)
    return decimal

def makeNewPopulation(population):#
    '''
        Make New Population.
            Utiliza selección, crossover y mutación para crear una nueva poblacion
    '''
    newPopulation = []
    while len(newPopulation) < len(population):
        # Hacer seleccion
        individualA = random.choice(population)
        individualB = random.choice(population)
        # Hacer el encoding
        cadenas = integerToString(int(individualA.genotype.gene), int(individualB.genotype.gene))
        cadenaA = cadenas[0]
        cadenaB = cadenas[1]
        # Hacer crossover
        genes = crossover(cadenaA,cadenaB)
        geneA = genes[0]
        geneB = genes[1]
        # Hacer mutación
        geneA = mutate(geneA)
        geneB = mutate(geneB)        
        # Crear hijos
        genA = stringToInteger(geneA)
        genB = stringToInteger(geneB)
        individualA = Individual("hijo", Genotype(genA) )
        individualB = Individual("hijo", Genotype(genB) )
        #Agregar hijos a new population
        newPopulation.append(individualA)
        newPopulation.append(individualB)
    return newPopulation

def sort(population):
    '''
        Sort
            Recibe un conjunto con una poblacion y devuelve una lista con la población ordenada en base a crowdedComparisonOperator
    '''
    listaOrdenada = []
    conjuntoComparacion = []
    
    for cadaElemento in population:
        conjuntoComparacion.append(cadaElemento)
    
    for i in range(0,len(population)):
        mayor = Individual()
        indice = 0
        for idx,val in enumerate(conjuntoComparacion):
            if (crowdedComparisonOperator(val,mayor)==True):
                mayor = val
                indice = idx
        
        listaOrdenada.append(mayor)
        conjuntoComparacion.pop(indice)
    return listaOrdenada


poblacioninicial = []
for i in range(0, 100):
    poblacioninicial.append(Individual("poblacion inicial", Genotype(random.random()*100)))
parents = set(poblacioninicial)
children = set()

for contador in range(0, 200):
    _p = set()
    n = 100
    i = 0
    t = 0
    parents = set(parents)
    children = set(children)
    r = parents | children
    f = fastNonDominatedSort(r)
    for a in f:
        print("_______f_______")
        for b in a:
            print("  ", b.genotype.gene, "\t", b.fenotype.objectives[0] ,"\t", b.fenotype.objectives[1])
    while(len(_p) < n ):
        if(i == len(f)):
            break
        f[i] = crowdingDistanceAssigment(f[i])
        _p = _p | set(f[i])
        i = i + 1
    _p = sort(_p)
    _p = list(_p)[0:len(parents)]
    children = makeNewPopulation(_p)
    t = t + 1
    parents = _p
