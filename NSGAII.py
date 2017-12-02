# NSGA II
import generate_field
import random
import copy

req = generate_field.req
custo = generate_field.custo
popul = 25
costmin = generate_field.costmin
costmax = generate_field.costmax
weightmin = generate_field.weightmin
weightmax = generate_field.weightmax
valuemin = generate_field.valuemin
valuemax = generate_field.valuemax
mutation_rate = 0.2
generation_num = 20
fout = open("out.csv", "w")
preset = "preset\n" \
         "requirement,customer,cost min,cost max,weight min,weight max," \
         "value min,value max\n"
preset += str(req) + ","
preset += str(custo) + ","
preset += str(costmin) + ","
preset += str(costmax) + ","
preset += str(weightmin) + ","
preset += str(weightmax) + ","
preset += str(valuemin) + ","
preset += str(valuemax) + "\n\n"

fout.write(preset)

nsga_preset = "NSGA-II preset\npopulation,mutation rate,generation number\n"
nsga_preset += str(popul) + "," + str(mutation_rate) + "," + str(generation_num) + "\n\n"
fout.write(nsga_preset)


field = generate_field.generate_field(req, custo)
for i in range(req):
    field.set_value("cost", random.randint(costmin, costmax), i)
    for j in range(custo):
        field.set_value("value", random.randint(valuemin, valuemax), i, j)
for j in range(custo):
    field.set_value("weight", random.randint(weightmin, weightmax), j)
field.eval_score()
fout.write("cost\n")
for c in field.cost:
    fout.write(str(c) + ",")
fout.write("\n\n")
fout.write("weight\n")
for w in field.weight:
    fout.write(str(w) + ",")
fout.write("\n\n")
fout.write("value\n")
for field_value in field.value:
    for fv in field_value:
        fout.write(str(fv) + ",")
    fout.write("\n")
fout.write("\n")
fout.write("score\n")
for s in field.score:
    fout.write(str(s) + ",")
fout.write("\n\n")


def print_solution_set(sol_set):
    for sol in sol_set:
        s = ""
        for tf in sol:
            if tf:
                s = s + "T,"
            else:
                s = s + "F,"
        sol_value = calc_val(sol)
        s = s + str(sol_value[0]) + ","
        s = s + str(sol_value[1]) + "\n"
        fout.write(s)


def calc_val(arr):
    cost_a = 0
    score_a = 0
    for i in range(req):
        if arr[i]:
            cost_a += field.cost[i]
            score_a += field.score[i]
    return cost_a, score_a


def dominate(a, b):
    cost_a = 0
    score_a = 0
    cost_b = 0
    score_b = 0
    for i in range(req):
        if a[i]:
            cost_a += field.cost[i]
            score_a += field.score[i]
        if b[i]:
            cost_b += field.cost[i]
            score_b += field.score[i]
    if cost_a > cost_b and score_a < score_b:
        return True
    return False


def fast_nondomi_sort(P):
    # nP : number of elements that i_th element of P dominates
    # SP : list of elements that i_th element is dominated
    # returning list of index lists
    SP = [[] for set in range(len(P))]
    nP = [0 for n in range(len(P))]
    F = [[]]
    for i in range(len(P)):
        for j in range(len(P)):
            if dominate(P[i], P[j]):
                SP[j].append(i)
                nP[i] += 1
        if nP[i] == 0:
            F[0].append(i)
    i = 0
    while len(F[i]) != 0:
        F.append([])
        for j in F[i]:
            for k in SP[j]:
                nP[k] -= 1
                if nP[k] == 0:
                    F[i+1].append(k)

        i += 1
    ### 수정중
    F.pop()
    return F


def make_child_pop(parent_set, child_set):
    for i in range(popul):
        r1 = random.randint(0, req-1)
        r2 = random.randint(0, req-2)
        if r2 >= r1:
            r2 += 1
        # r1, r2 crossover
        r3 = random.randint(0, req-1)
        try:
            c1 = parent_set[r1][:r3] + parent_set[r2][r3:]
            c2 = parent_set[r2][:r3] + parent_set[r1][r3:]
        except IndexError:
            print(parent_set, r3, r1, r2)

        # r4 : mutation
        r4 = random.randint(0, 99)
        r5 = random.randint(0, 99)
        if r4 < 100 * mutation_rate:
            r6 = random.randint(0, req-1)
            c1[r6] = not c1[r6]
        if r5 < 100 * mutation_rate:
            r6 = random.randint(0,req-1)
            c2[r6] = not c2[r6]
        child_set.append(c1)
        child_set.append(c2)
    child_set = child_set + copy.copy(parent_set)


# generate initial population
P_set = []
for i in range(popul):
    P_set.append([])
    for j in range(req):
        randvalue = random.randint(0,1)
        if randvalue == 0:
            P_set[i].append(False)
        else:
            P_set[i].append(True)
fout.write("Initial set\n")
print_solution_set(P_set)

for i in range(generation_num):
    print(str(i) + " generation passed successfully")
    # generate child generation
    C_set = []
    make_child_pop(P_set, C_set)
    F = fast_nondomi_sort(C_set)
    new_P_set = []
    j = 0
    while len(new_P_set) < popul:
        if len(new_P_set) + len(F[j]) < popul:
            for idx in F[j]:
                new_P_set.append(C_set[idx])
        else:
            random.shuffle(F[j])
            for k in range(popul - len(new_P_set)):
                new_P_set.append(C_set[F[j][k]])
        j+=1
    P_set = new_P_set
fout.write("\nresult\n")
print_solution_set(P_set)
fout.close()
