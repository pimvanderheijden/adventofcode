import pprint
import sys

pp = pprint.PrettyPrinter(indent=4).pprint

def map(arr, fn):
    new_arr = []
    for item in arr: new_arr.append(fn(item))
    return new_arr

def intcode(input, noun, verb):
    def get_values(store, instruction, modes):
        values = {}
        if modes[1 - 1]: values['a'] = instruction[1] if modes[1 - 1] == 1 else store[instruction[1]]
        if modes[2 - 1]: values['b'] = instruction[2] if modes[2 - 1] == 1 else store[instruction[2]]
        if modes[3 - 1]: values['c'] = instruction[3] if modes[3 - 1] == 1 else store[instruction[3]]
        return values

    def op1(store, instruction, modes):
        new_store = store
        values = get_values(store, instruction, modes)
        new_store[values['c']] = new_store[values['b']] + new_store[values['c']]
        return new_store

    def op2(store, instruction, modes):
        new_store = store
        values  = get_values(store, instruction, modes)
        new_store[values['c']] = new_store[values['b']] * new_store[values['c']]
        return new_store

    def op3(store, instruction, modes):
        new_store = store
        values  = get_values(store, instruction, modes)
        new_store[instruction[1]] = values['a']
        return new_store

    def op4(store, instruction, modes):
        new_store = store
        values  = get_values(store, instruction, modes)
        new_store[values['a']] = instruction[1]
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

        if first_len == 1:
            opcode = int(first_str[first_len - 1])
        else:
            opcode = int(first_str[first_len - 1] + first_str[first_len - 2])

        if first_len > 2:
            modes.append(int(first_str[first_len - 3]))
        if first_len > 3:
            modes.append(int(first_str[first_len - 4]))
        if first_len > 4:
            modes.append(int(first_str[first_len - 5]))

        if opcode == 99: return store

        offset = offsets[opcode]
        instruction = get_instruction(offset, store, pointer)
        new_store = operations[opcode](store, instruction, modes)
        return run(new_store, pointer + offset)

    store = map(input.split(','), int)
    if noun: store[1] = noun
    if verb: store[2] = verb
    output = run(store, 0)

    return ','.join(x for x in map(output, str))

def pprint_output(str):
    mem = str.split(',')
    for i in range(len(mem) - 1):
        if i % 4 == 0:
            pp([mem[i], mem[1 + i], mem[2 + i], mem[3 + i]])


if len(sys.argv) == 4:
    input = sys.argv[3]
    noun = int(sys.argv[1])
    verb = int(sys.argv[2])
    output = intcode(input, noun, verb)
else:
    input = sys.argv[1]
    output = intcode(input, False, False)

pprint_output(output)
print('------------------------------------------')
pp(int(output.split(',')[0]))

# value on address 0 should be 4462686
# noun 59 and verb 36 give 19690720