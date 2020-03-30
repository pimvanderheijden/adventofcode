import pprint

input1 = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,6,27,2,27,13,31,1,10,31,35,1,10,35,39,2,39,6,43,1,43,5,47,2,10,47,51,1,5,51,55,1,55,13,59,1,59,9,63,2,9,63,67,1,6,67,71,1,71,13,75,1,75,10,79,1,5,79,83,1,10,83,87,1,5,87,91,1,91,9,95,2,13,95,99,1,5,99,103,2,103,9,107,1,5,107,111,2,111,9,115,1,115,6,119,2,13,119,123,1,123,5,127,1,127,9,131,1,131,10,135,1,13,135,139,2,9,139,143,1,5,143,147,1,13,147,151,1,151,2,155,1,10,155,0,99,2,14,0,0'
pp = pprint.PrettyPrinter(indent=4).pprint

def map(arr, fn):
    new_arr = []
    for item in arr: new_arr.append(fn(item))
    return new_arr

def intcode(input):
    def op1(store, line):
        new_store = store
        new_store[line[3]] = new_store[line[1]] + new_store[line[2]]
        return new_store

    def op2(store, line):
        new_store = store
        new_store[line[3]] = new_store[line[1]] * new_store[line[2]]
        return new_store

    operations = { 1: op1, 2: op2 }

    def get_fresh_line(store, offset):
        return [store[offset], store[offset + 1], store[offset + 2], store[offset + 3]]

    def run(store, offset):
        if offset == len(store): return store
        if store[offset] == 99: return store

        try:
            operation = operations[store[offset]]
        except:
            raise Exception('No operation for:', store[offset], 'and offset', offset)

        new_store = operation(store, get_fresh_line(store, offset))
        return run(new_store, offset + 4)

    output = run(map(input.split(','), int), 0)
    return ','.join(x for x in map(output, str))

def pprint_output(str):
    mem = str.split(',')
    for i in range(len(mem) - 1):
        if i % 4 == 0:
            pp([mem[i], mem[1 + i], mem[2 + i], mem[3 + i]])

# Once you have a working computer,
# the first step is to restore
# the gravity assist program (your puzzle input)
# to the "1202 program alarm" state it had
# just before the last computer caught fire.
# To do this, before running the program,
# replace position 1 with the value 12
# and replace position 2 with the value 2.
# What value is left at position 0 after the program halts?

numbers = map(input1.split(','), int)
numbers[1] = 12
numbers[2] = 2
mutated_input = ','.join(x for x in map(numbers, str))

pprint_output(intcode(mutated_input))
