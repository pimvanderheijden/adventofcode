import pprint

from intcode import intcode

pp = pprint.PrettyPrinter(indent=4).pprint


def pprint_output(str):
    mem = str.split(',')
    for i in range(len(mem) - 1):
        if i % 4 == 0:
            pp([mem[i], mem[1 + i], mem[2 + i], mem[3 + i]])

reader = open("input_day_7.txt", "r")
input1 = reader.read()
reader.close()

highest = 0

# create list of all permutation
def get_perms(dimension):
    perms = []

    for i in range(pow(10, dimension)):
        perm = list(str(i).zfill(dimension))
        perms.append(map(int, perm))

    return perms

perms = get_perms(1)

for perm in perms:
    latest_input = input1

    for choice, i in enumerate(perm):
        input_curr = output if i != 0 else latest_input
        res = intcode(input_curr, False, False, choice)
        latest_input = res['output_full']
        if res['output_num'] > highest: highest = res['output_num']