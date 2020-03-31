import pprint
import sys

noun = int(sys.argv[1])
verb = int(sys.argv[2])
input = sys.argv[3]

pp = pprint.PrettyPrinter(indent=4).pprint

def map(arr, fn):
    new_arr = []
    for item in arr: new_arr.append(fn(item))
    return new_arr

def intcode(input, noun, verb):
    def op1(store, instruction):
        new_store = store
        new_store[instruction[3]] = new_store[instruction[1]] + new_store[instruction[2]]
        return new_store

    def op2(store, instruction):
        new_store = store
        new_store[instruction[3]] = new_store[instruction[1]] * new_store[instruction[2]]
        return new_store

    def op3(store, instruction, modes):
        new_store = store
        value = instruction[1]
        new_store[value] = value if modes[1] == 1 else store[value]
        return new_store

    def op4(store, instruction, modes):
        new_store = store
        value = instruction[1]
        new_store[value if modes[1] == 1 else store[value]] = value
        return new_store

    operations = { 1: op1, 2: op2, 3: op3, 4: op4 }
    offsets = { 1: 4, 2: 4, 3: 2, 4: 2 }

    def get_instruction(length, store, pointer):
        line = []
        for i in range(length):
            line.append(store[pointer] + i)
        return line

    def run(store, pointer):
        # should always end with 99?
        # if pointer == len(store): return store

        first = store[pointer]
        first_str = str(first)
        first_len = len(first_str)
        modes = []

        if first_len > 2:
            modes[1] = int(first_str[first_len - 1 - 2])
        if first_len > 3:
            modes[2] = int(first_str[first_len - 1 - 3])
        if first_len > 4:
            modes[3] = int(first_str[first_len - 1 - 4])

        opcode = int(first_str[first_len - 1] + first_str[first_len - 2])

        if opcode == 99: return store

        offset = offsets[opcode]
        instruction = get_instruction(offset, store, pointer)
        new_store = operations[opcode](store, instruction, modes)
        return run(new_store, pointer + offset)

    store = map(input.split(','), int)
    store[1] = noun
    store[2] = verb
    output = run(store, 0)

    return ','.join(x for x in map(output, str))

def pprint_output(str):
    mem = str.split(',')
    for i in range(len(mem) - 1):
        if i % 4 == 0:
            pp([mem[i], mem[1 + i], mem[2 + i], mem[3 + i]])

output = intcode(input, noun, verb)
pprint_output(output)
print('------------------------------------------')
pp(int(output.split(',')[0]))

# value on address 0 should be 4462686
# noun 59 and verb 36 give 19690720