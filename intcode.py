import sys


def get_value(store, parameter, mode):
    if mode == '1': # immediate mode
        return parameter
    else: # position mode
        return store[parameter]

def intcode(input_str, noun, verb, choice):
    def op1(store, instruction, modes):
        new_store = store
        value1 = get_value(store, instruction[1], modes[2])
        value2 = get_value(store, instruction[2], modes[1])

        # Parameters that an instruction writes to will never be in immediate mode.
        value3 = get_value(store, instruction[3], modes[0])
        # ----> only get working situation with immediate mode
        # value3 = instruction[3]

        new_store[value3] = value1 + value2
        return new_store

    def op2(store, instruction, modes):
        new_store = store
        value1 = get_value(store, instruction[1], modes[2])
        value2 = get_value(store, instruction[2], modes[1])

        # Parameters that an instruction writes to will never be in immediate mode.
        value3 = get_value(store, instruction[3], modes[0])
        # ----> only get working situation with immediate mode
        # value3 = instruction[3]

        new_store[value3] = value1 * value2
        return new_store

    def op3(store, instruction, modes):
        new_store = store

        # Parameters that an instruction writes to will never be in immediate mode.
        # ----> only get working situation with immediate mode
        value1 = get_value(store, instruction[1], modes[2])

        new_store[value1] = choice
        return new_store

    def op4(store, instruction, modes):
        global output_num

        new_store = store

        # Parameters that an instruction writes to will never be in immediate mode.
        value1 = get_value(store, instruction[1], modes[2])

        output_num += value1

        return new_store

    def get_instruction(offset, store, pointer):
        instruction = []
        for i in range(offset):
            instruction.append(store[pointer + i])
        return instruction

    def run(store, pointer):
        # print('', )
        # print('pointer', pointer)
        # print(','.join(x for x in map(str, store))[:60])

        # Does it always end with 99?
        # If not, do this:
        # if pointer == len(store): return store

        first = store[pointer]
        first_str = str(first).zfill(5)
        modes = list(first_str)
        a = modes.pop()
        b = modes.pop()
        opcode = int(b + a)

        if opcode == 99: return store

        # print('opcode', opcode)
        offset = offsets[opcode]
        instruction = get_instruction(offset, store, pointer)
        # print('opcode', opcode)
        # print('instruction', instruction)
        # print('modes', modes)
        new_store = operations[opcode](store, instruction, modes)
        return run(new_store, pointer + offset)

    operations = { 1: op1, 2: op2, 3: op3, 4: op4 }
    offsets = { 1: 4, 2: 4, 3: 2, 4: 2 }
    store = []
    output_num = ''

    for _ in range(10000):
        store.append('0')

    def fill_store(i, digit):
        store[i] = digit

    input_str_splitted = input_str.split(',')

    for i, digit in enumerate(input_str_splitted):
        fill_store(i, digit)

    if noun: store[1] = noun
    if verb: store[2] = verb

    input_transformed = run(map(int, store), 0)[:len(input_str_splitted) -1]
    output_full = ','.join(x for x in map(str, input_transformed))

    return dict(
        output_full=output_full,
        output_num=output_num
    )