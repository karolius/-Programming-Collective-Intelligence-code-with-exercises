from random import random, randint, uniform, choice
from copy import deepcopy
from math import log
import time
import math
from itertools import combinations


class fwrapper:
    """
    A wrapper for the functions that will be used on function nodes. Its memeber
    variables are the name of the function, the function itself, and the number
    of paremeters it takes.
    """
    def __init__(self, function, childcount, name):
        self.function = function
        self.childcount = childcount
        self.name = name


class node:
    """
    The class for function nodes (nodes with children). This is initialized with
    an fwrapper. When evaluated is called, it evaluates the child nodes and then
    applies the function to their results.
    """
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print (' '*indent)+self.name
        for c in self.children:
            c.display(indent+1)


class paramnode:
    """
    The class for nodes that only return one of the parameters passed to the
    program. Its evaluate method returns the parameter specified by idx.
    """
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print '%sp%d' % (' '*indent, self.idx)


class constnode:
    """
    Nodes that return a constatn value. The evaluate method simply returns
    the value with which it was initialized.
    """
    def __init__(self, v):
        self.v = v

    def evaluate(self, inp):
        return self.v

    def display(self, indent=0):
        print '%s%d' % (' '*indent, self.v)


def randposexc(x=[]):
    """

    :param x:
    :return:
    """
    if not isinstance(x, list):
        x = [x]
    if 3 == len(x):
        for i in xrange(0, 3):
            if i not in x:
                return i
            else:
                x.remove(i)
    while True:
        c = randint(0, 3)
        if c not in x:
            break
    return c


def chose(l):
    # Decode info from stance() and return function to use
    if l[0] == 0:
        return l[1]
    elif l[0] > 0:
        return l[2]
    elif l[0] == -1:
        return l[3]
    else:
        return l[4]


def stance(l):
    # Return stance
    x = (l[0] - l[2]) ** 2 + (l[1] - l[3]) ** 2
    # Attack
    if x == 1:
        return 1
    # Defense A and B
    elif x == 2:
        return -1
    elif x == 4:
        return -2
    # Rand move
    else:
        return 0


def attack(l):
    # If opponent is near, then attack if its possible
    if l[2] == l[0]:
        if l[3] > l[1]:
            if 3 != l[4]:
                return 3
            else:
                return randposexc(x=[3])
        else:
            if 2 != l[4]:
                return 2
            else:
                return randposexc(x=[2])
    else:
        if l[2] > l[0]:
            if 1 != l[4]:
                return 1
            else:
                return randposexc(x=[1])
        else:
            if 0 != l[4]:
                return 0
            else:
                return randposexc(x=[0])


def adefense(l):
    if l[2] > l[0]:
        if l[3] > l[1]:
            return randposexc(x=[l[4], 1, 3])
        else:
            return randposexc(x=[l[4], 1, 2])
    else:
        if l[3] > l[1]:
            return randposexc(x=[0, l[4], 3])
        else:
            return randposexc(x=[0, l[4], 2])


def bdefense(l):
    if l[2] == l[0]:
        if l[3] > l[1]:
            return randposexc(x=[l[4], 3])
        else:
            return randposexc(x=[l[4], 2])
    else:
        if l[2] > l[0]:
            return randposexc(x=[1, l[4]])
        else:
            return randposexc(x=[0, l[4]])


# Changed all to lambda for practise + some functions added
addw = fwrapper(lambda l: l[0] + l[1], 2, 'add')
subw = fwrapper(lambda l: l[0] - l[1], 2, 'subtract')
mulw = fwrapper(lambda l: l[0] * l[1], 2, 'multiply')
ifw = fwrapper(lambda l: l[1] if l[0] > 0 else l[2], 3, 'if')
gtw = fwrapper(lambda l: 1 if l[0] > l[1] else 0, 2, 'isgreater')
parw = fwrapper(lambda l: 1 if l[1] != 0 and l[0] % l[1] else 0, 3, 'parity')
sqw = fwrapper(lambda l: l[0] ** 2, 1, 'square')
euclw = fwrapper(lambda l: ((l[0]-l[1])**2)+(l[2]-l[3])**2, 4, 'euclidean')
decw = fwrapper(chose, 5, 'chose')
stnw = fwrapper(stance, 4, 'stance')
rndmw = fwrapper(randposexc, 1, 'rand move')
attw = fwrapper(attack, 5, 'attack')
adefw = fwrapper(adefense, 5, 'A defense')
bdefw = fwrapper(bdefense, 5, 'B defense')
flist = [addw, mulw, ifw, gtw, subw, decw, stnw, rndmw, attw, adefw, bdefw,  # parw , sqw, euclw
        ]


def gridwarterminator():
    # His name's Mkbewe
    """
    Another one player "KutangPan" can run to closest (avoid colision with player 2)
    corner and stuck there with move changing. When someone come- attack him.
    """
    return node(decw, [node(stnw, [paramnode(0), paramnode(1), paramnode(2), paramnode(3)]),
                       node(rndmw, [paramnode(4)]),
                       node(attw, [paramnode(0), paramnode(1), paramnode(2), paramnode(3), paramnode(4)]),
                       node(adefw, [paramnode(0), paramnode(1), paramnode(2), paramnode(3), paramnode(4)]),
                       node(bdefw, [paramnode(0), paramnode(1), paramnode(2), paramnode(3), paramnode(4)]), ])


def exampletree():
    return node(ifw, [node(gtw, [paramnode(0), constnode(3)]),
                      node(addw, [paramnode(1), constnode(5)]),
                      node(subw, [paramnode(1), constnode(2)]), ])


def exampletree():
    return node(ifw, [node(gtw, [paramnode(0), constnode(3)]),
                      node(addw, [paramnode(1), constnode(5)]),
                      node(subw, [paramnode(1), constnode(2)]), ])


def makerandomtree(pc, maxdepth=4, fpr=0.5, ppr=0.6, chcount=None):
    """
    :param pc:
    :param maxdepth:
    :param fpr:
    :param ppr:
    :param chcount: default None to deal with book usage and specified
    for replacement mutation
    :return:
    """
    if maxdepth > 0 and random() < fpr:  # Better check first less computational intensive condition
        if chcount is None:
            f = choice(flist)
            chcount = f.childcount
            children = [makerandomtree(pc, maxdepth - 1, fpr, ppr)
                        for _ in xrange(chcount)]
        else:
            f = choice([f for f in flist if f.childcount == chcount])
            children = None
        return node(f, children)
    elif random() < ppr:
        return paramnode(randint(0, pc-1))
    else:
        return constnode(randint(0, 10))


def hiddenfunction(x, y):
    return x**2 + 2*y + 3*x + 5


def hiddensin(x, y):
    return y*math.sin(x)


def buildhiddenset(fun=hiddenfunction):
    rows = []
    for i in xrange(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hiddenfunction(x, y)])
    return rows


def scorefunction(tree, s):
    dif = 0
    for data in s:
        v = tree.evaluate([data[0], data[1]])
        dif += abs(v - data[2])
    return dif


def mutate(t, pc, probchange=0.1):
    if random() < probchange:
        return makerandomtree(pc)
    else:
        result = deepcopy(t)
        if isinstance(t, node):
            result.children = [mutate(c, pc, probchange) for c in t.children]
        return result


def repmutate(t, pc, probchange=0.1):
    """
    Travesing down, chooses a random node on the tree and changes just it.
    :param t:
    :param pc:
    :param probchange:
    :return:
    """
    if random() < probchange:
        if isinstance(t, node):
            tchildlist = t.children
            newnode = makerandomtree(pc, maxdepth=1, fpr=1, chcount=len(tchildlist))
            newnode.children = tchildlist
            return newnode
        elif isinstance(t, paramnode):
            return makerandomtree(pc, maxdepth=0, ppr=1)
        else:
            return makerandomtree(pc, maxdepth=0, ppr=0)
    else:
        result = deepcopy(t)
        if isinstance(t, node):
            result.children = [repmutate(c, pc, probchange) for c in t.children]
        return result


def crossover(t1, t2, probswap=0.7, top=True):
    if not top and random() < probswap:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, node) and isinstance(t2, node):
            result.children = [crossover(c, choice(t2.children), probswap, False)
                               for c in t1.children]
        return result


def getbranchlist(tlist, brlist=None):
    if brlist is None:
        brlist = []
    for t in tlist:
        if isinstance(t, node):
            brlist.append(t)
            getbranchlist(t.children, brlist)
    return brlist


def randcrossover(t1, t2, probswap=0.7, top=True, brlist=None):
    """
    Different crossover function that crosses any two random branches
    :param t1:
    :param t2:
    :param probswap:
    :param top:
    :param brlist: branch list for randome chose from t2
    :return:
    """
    if brlist is None:
        if isinstance(t2, node):
            brlist = getbranchlist([t2])
        else:
            return t1
    if not top and random() < probswap:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, node):
            result.children = [randcrossover(c, choice(brlist), probswap, False, brlist=brlist)
                               for c in t1.children]
        return result


def evolve(pc, popsize, rankfunction, maxgen=500, mutationrate=0.1, breedingrate=0.4, pexp=0.7,
           pnew=0.05, pmut=0.75, mutswap=0.03, prcross=0.9, crossswap=0.1, maxnoimpr=None, individs=None):
    """
    This function creates an initial random population. It then loops up to maxgen times,
    each time calling rankfunction to rank the programs from best to worst. The best
    program is automatically passed through to the next generation unaltered, which is
    sometimes referred to as elitism. The rest of the next generation is constructed by
    randomly choosing programs that are near the top of the ranking, and then breeding
    and mutating them. This process repeats until either a program has a perfect score of
    0 or maxgen is reached.
    :param pc: number of input variables for trees
    :param popsize: size of the initial population
    :param rankfunction:
    :param maxgen:
    :param mutationrate: Pr of a mutation
    :param breedingrate: Pr of a crossover
    :param pexp: lowering its value, you allow weaker solutions into the final result
                it should be in range of 0 < p < 1 due to log assumption
     turning the process from "survival of the fittest" to "survival of the fittest
     and luckiest."
    :param pnew: Pr when building the new population that a completely new, random
                 program is introduced
    :param pmut: Pr of replacement mutation rather than branch replacement
    :param mutswap: If actual score / mean of initial scores is < thatn this param,
                then probability of using replace mutation : mutation swaps.
    :param prcross: Pr of random crossover rather than normal
    :param mutswap: If actual score / mean of initial scores is < thatn this param,
                then probability of using random crossover : crossover swaps.
    :param maxnoimpr: stops the process and returns the best result if the best score
                hasn't improved within X generations
    :param individs: list of individuals to be added to random populatinn
    :return:
    """
    # Compute constants once
    xmin = pexp**(popsize-2)
    den = log(pexp)
    def selectindex():
        """
        xmin prevents functionf from risisng error by restricting X (it still return
        pseudo random number)
        :return: random number, tending towards lower numbers. The lower pexp is, more
        lower numbers you will get
        """
        return int(log(uniform(xmin, 1.0)) / den)

    # Create a random initial population
    mswap = False
    cswap = False
    iniscore = 0
    noimpr = 0
    prevscore = 0
    population = [makerandomtree(pc) for _ in range(popsize)]
    if individs is not None:
        for ind in individs:
            population.append(ind)
    for i in xrange(maxgen):
        scores = rankfunction(population)
        s00 = scores[0][0]
        if maxnoimpr is not None:
            if s00 == prevscore:
                noimpr += 1
                if noimpr == maxnoimpr:
                    break
            else:
                noimpr = 0
        prevscore = s00
        if 0 < i < 4:
            iniscore += s00
            if i == 3:
                mswap = True
                cswap = True
                denasnom = 3.0/iniscore
        print s00
        if s00 == 0:
            break
        if mswap and s00 * denasnom < mutswap:
            pmut = 1 - pmut
            mswap = False
            print "MUTSWAP"
        if cswap and s00 * denasnom < crossswap:
            prcross = 1 - prcross
            cswap = False
            print "CROSSSWAP"
        # The two best always make it
        newpop = [scores[0][1], scores[1][1]]
        # Build the next generation
        while len(newpop) < popsize:
            if random() > pnew:
                if random() < pmut:
                    mutfun = mutate
                else:
                    mutfun = repmutate
                if random() < prcross:
                    crossfun = randcrossover
                else:
                    crossfun = crossover
                newpop.append(mutfun(crossfun(scores[selectindex()][1],
                                              scores[selectindex()][1],
                                              probswap=breedingrate), pc,
                                     probchange=mutationrate))
            else:
                # Add a random node to mix things up
                newpop.append(makerandomtree(pc))
        population = newpop

    scores[0][1].display()
    return scores[0][1]


def getrankfunction(dataset):
    def rankfunction(population):
        scores = [(scorefunction(t, dataset), t) for t in population]
        scores.sort()
        return scores
    return rankfunction


def gridgame(p):
    """
    :param p:
    :return:
     0 - player 1 is the winner
     1 - player 2 is the winner
     -1 - player 1 is the winner
    """
    max = (3, 3)  # Board size
    # Remember the last move for each player
    lastmove = [-1, -1]

    # Remember the player's locations and put the second player a
    # sufficient didstance from the first
    location = [[randint(0, max[0]), randint(0, max[1])]]
    location.append([(location[0][0] + 2) % 4, (location[0][1] + 2) % 4])

    # Maximum of 50 moves before a tie
    for _ in xrange(50):
        for i in xrange(2):  # for each player
            locs = location[i][:] + location[1-i][:]
            locs.append(lastmove[i])
            move = p[i].evaluate(locs) % 4

            # You lose if you move the same direction twice in a row
            if lastmove[i] == move:
                return 1-i
            lastmove[i] = move

            # Checkig which side was choosen and board limits
            if move == 0:
                location[i][0] -= 1
                if location[i][0] < 0:
                    location[i][0] = 0
            if move == 1:
                location[i][0] += 1
                if location[i][0] > max[0]:
                    location[i][0] = max[0]
            if move == 2:
                location[i][1] -= 1
                if location[i][1] < 0:
                    location[i][1] = 0
            if move == 3:
                location[i][1] += 1
                if location[i][1] > max[1]:
                    location[i][1] = max[1]

            # If you have captured the other player, you win
            if location[i] == location[1-i]:
                return i
    return -1


def tttoegame(p):
    """
    :param p:
    :return:
     0 - player 1 is the winner
     1 - player 2 is the winner
     -1 - player 1 is the winner
    """
    # Remember the player's locations and put the second player a
    # sufficient didstance from the first
    pickedpoints = ([0]*5, [0]*5)
    points = [n for n in xrange(1, 10)]  # Board size
    for o in xrange(9):
        for i in xrange(2):  # for each player
            pnt = p[i].evaluate(points) % 9
            # You lose if you choose the same point twice
            if points[pnt] == -1 or points[pnt] == -2:
                return 1-i
            points[pnt] = -(i+1)  # f(0)=-1, f(1)=-2
            pickedpoints[i][o/2] = pnt
            if o > 3:
                for comb in combinations(pickedpoints[i], 3):
                    if sum(comb) == 15 and 0 not in comb:
                        return i
    return -1


def tournament(pl, progtoevolve=gridgame):
    # Count losses
    losses = [0 for _ in pl]

    # Every player plays every other player
    for i in xrange(len(pl)):
        for j in xrange(len(pl)):
            if i == j:
                continue
            # Who is the winner!?
            winner = progtoevolve([pl[i], pl[j]])

            # Two points for a loss, one point for a tie
            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            elif winner == -1:
                losses[i] += 1
                losses[j] += 1
    # Sort and return the results
    z = zip(losses, pl)
    z.sort()
    return z


class humanplayer:
    def evaluate(self, board):
        # Get my location and the location of other player
        me = tuple(board[:2])
        others = [tuple(board[x: x+2]) for x in xrange(2, len(board)-1, 2)]

        # Display the board
        for i in xrange(4):
            for j in xrange(4):
                if (i, j) == me:
                    print '0',
                elif (i, j) in others:
                    print 'X',
                else:
                    print '.',
            print
        # Show moves, for reference
        print 'Your last move was %d' % board[len(board)-1]
        print ' 0'
        print '2 3'
        print ' 1'
        print 'Enter move: ',

        # Return whatever the user enters
        move = int(raw_input())
        return move


class ttthumanplayer:
    def evaluate(self, board):
        # Split picks for: my, others and rest
        me = []
        others = []
        rest = []
        gridboard = [4, 9, 2, 3, 5, 7, 8, 1, 6]
        for i, el in enumerate(board):
            if el == -2:
                me.append(i+1)
            elif el == -1:
                others.append(i+1)
            else:
                rest.append(el)

        # Display the board with grid numbers to pick, and mark already choosen
        for i, grid in enumerate(gridboard):
            if i % 3 == 0:
                print
            if grid in me:
                print 'O',
            elif grid in others:
                print 'X',
            else:
                print grid,

        print '\nEnter grid number: ',
        while True:
            grid = int(raw_input())
            if grid in rest:
                break
            print 'Your can mark only numbers from grid:'
        return grid-1


def exampletree2():
    # if x%2 == 1: return x**(1.0/y) else return y**x
    return node(euclw, [node(parw, [paramnode(0), constnode(2)]),
                        node(addw, [paramnode(0), paramnode(1)]),
                        node(subw, [paramnode(1), paramnode(0)]),
                        node(sqw, [paramnode(1)]), ]) 


def printsummary(g):
    if g == 0:
        print "You lose!"
    elif g == 1:
        print "You WIN!"
    else:
        print "Tie!"


def paramtournament(pl, programgtoevolve):
    return tournament(pl, progtoevolve=programgtoevolve)


if __name__ == '__main__':
    '''
    # Building and Evaluating Trees
    exampletree = exampletree()
    exampletree2 = exampletree2()

    print exampletree.evaluate([2, 3])
    print exampletree.evaluate([5, 3])
    print exampletree.evaluate([4, 5])

    print exampletree2.evaluate([8, 3])
    print exampletree2.evaluate([9, 2])
    print exampletree2.evaluate([4, 2])


    # Displaying the Program
    exampletree = exampletree()
    exampletree2 = exampletree2()
    exampletree.display()
    print '\n'
    exampletree2.display()


    # Creating the Initial Population
    for _ in xrange(4):
        exampletree = makerandomtree(2)
        print exampletree.evaluate([2, 3])
        print exampletree.evaluate([5, 3])
        exampletree.display()
        print '\n'


    random1 = makerandomtree(2)
    random2 = makerandomtree(2)

    hiddenset = buildhiddenset()
    print scorefunction(random1, hiddenset)
    print scorefunction(random2, hiddenset)

    # Function found after 5,7 mln iterations
    prev = 999999999999
    i = 0
    random1 = makerandomtree(2)
    start = time.time()
    while True:
        random1 = makerandomtree(2)
        sc = scorefunction(random1, hiddenset)
        if sc < prev:
            prev = sc
            print 'Iter: {:d} \nWith score: {:d} for function:\n'.format(i, sc)
            print 'Czas: ', time.time() - start
            random1.display()
            if sc == 0:
                print 'Motyla noga, udalo sie!'
                print 'Czas: ', time.time()-start
                break
        i += 1


    # Building the Environment (exercises task implemented)
    rf = getrankfunction(buildhiddenset())
    evolve(2, 500, rf, mutationrate=0.25, breedingrate=0.12, pexp=0.7,
           pnew=0.15, pmut=0.8, mutswap=0.12, prcross=0.9, crossswap=0.12, maxnoimpr=7)


    # Gridgame
    p1 = makerandomtree(5)
    p2 = makerandomtree(5)

    print gridgame([p1, p2])


    # A Round-Robin Tournament and Playing Against Real People
    winner = evolve(5, 100, tournament, maxgen=50)
    winner.display()
    gridgame([winner, humanplayer()])


    # Replacement muation
    exampletree = exampletree()
    print '\n'
    exampletree.display()
    nt = repmutate(exampletree, 2, probchange=0.6)
    print '\n'
    nt.display()

    # Building the Environment
    rf = getrankfunction(buildhiddenset(fun=hiddensin))
    evolve(2, 500, rf, mutationrate=0.25, breedingrate=0.12, pexp=0.7,
           pnew=0.15, pmut=0.8, mutswap=0.12, prcross=0.9, crossswap=0.12, maxnoimpr=7)


    # Playing Agaist Terminator
    pcp = gridwarterminator()
    pcp.display()
    printsummary(gridgame([pcp, humanplayer()]))

    # A Round-Robin Tournament and Playing Against Hand Designed Tree Program
    # (You can add him, but its too good for initial functons, so he need a friend to compete)
    winner = evolve(5, 100, tournament, maxgen=50)
    winner.display()
    printsummary(gridgame([winner, gridwarterminator()]))


    # Tic Tac Toe - A Round-Robin Tournament and Playing Against Real People
    tictactoe = lambda pl: tournament(pl, progtoevolve=tttoegame)
    winner = evolve(9, 150, tictactoe, maxgen=40, mutationrate=0.1, breedingrate=0.4, pexp=0.7,
                    pnew=0.05, pmut=0.75, mutswap=0.03, prcross=0.9, crossswap=0.1)
    winner.display()
    printsummary(tttoegame([winner, ttthumanplayer()]))
    '''