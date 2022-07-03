from itertools import product

# Defining number of digits

N = 5

# Creating all numbers: additions, result and technical

ANum = tuple("a" + str(i) for i in range(N))
ANumRev = ANum[::-1]
XNum = tuple("x" + str(i) for i in range(N))[::-1]
NNum1 = tuple("n" + str(i) for i in range(N - 1))[::-1] + (0,)
NNum2 = (0,) + tuple("+ 10 * n" + str(i) for i in range(N - 1))[::-1]

# Creating tuple from the numbers and transponding them to make expressions

addons = ANumRev, NNum1, XNum
result = NNum2, ANum
addons2 = tuple(tuple(addons[r][c] for r in range(3)) for c in range(N))[::-1]
result2 = tuple(tuple(result[r][c] for r in range(2)) for c in range(N))[::-1]

# Adding expressions from both sides to each other to new arrays

addons3 = list()
result3 = list()
for i in range(N // 2):
    addons3.append(list(addons2[i] + addons2[-1-i]))
    result3.append(list(result2[i] + result2[-1-i]))

# Adding unchanged middle expressions of the N is odd

if N % 2:
    addons3.append(list(addons2[N//2]))
    result3.append(list(result2[N//2]))

# Simplifying expressions - removing 0's and digits, moving n's to the right (result) part
# joining expressions to get nice and eval-uable view

for i, val in enumerate(addons3):
    for j in reversed(range(len(val))):
        focus = val[j]
        if not focus or focus.startswith("a"):
            del val[j]
            result3[i].remove(focus)
        elif focus.startswith("n"):
            del val[j]
            result3[i].append("- " + focus)
    addons3[i] = " + ".join(val)
    result3[i] = " ".join(result3[i])

# Trying all variants of n'2, evaluating result and storing valid solutions

solutions = list()
for var in product((0, 1), repeat=N-1):
    sol = [var, {}, []]
    #creating final expressions for x's
    for i in range(len(addons3)):
        change_res3 = result3[i]
        for j in range(N):
            change_res3 = change_res3.replace("n{}".format(j), "var[{}]".format(j))
        ev = eval(change_res3)
        if ev < 0 or ev > 18:
            break
        elif ev == 10 and len(addons3[i]) == 2:
            break
        if not ev and len(addons3[i]) > 2:
            sol[1][addons3[i][:2]] = 0
            sol[1][addons3[i][-2:]] = 0
        elif ev == 18:
            sol[1][addons3[i][:2]] = 9
            sol[1][addons3[i][-2:]] = 9
        else:
            sol[1][addons3[i]] = ev
    # Creating final expressions for addons and result
    else:
        for i in range(N):
            change_add2 = list(addons2[i])
            change_res2 = list(result2[i])
            if change_add2[2] in sol[1] and not sol[1][change_add2[2]]:
                del change_add2[2]
            if not change_add2[1] or not var[int(change_add2[1][1])]:
                del change_add2[1]
            else:
                change_add2[1] = "1"
            if not change_res2[0] or not var[int(change_res2[0][-1])]:
                del change_res2[0]
            else:
                change_res2[0] = "10"
            sol[2].append(" + ".join(change_add2) + " = " + " + ".join(change_res2))
        solutions.append(sol)

# Printing all steps and valid solutions

print(ANumRev)
# print(NNum1)
print(XNum)
print("_" * N * 6)
# print(NNum2)
print(ANum)
print()
print("addons2 + result2:")
for i in range(N):
    print(addons2[i], "=", result2[i])
print()
print("addons3 + result3 simplified:")
for i in range(N // 2 + N % 2):
    print(addons3[i], "=", result3[i])
print()
for var, xx, aa in solutions:
    print("var = ", var)
    print()
    for k, v in xx.items():
        print(k, '=', v)
    print()
    for row in aa:
        print(row)
    print()
