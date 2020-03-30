import pprint

input1 = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,6,27,2,27,13,31,1,10,31,35,1,10,35,39,2,39,6,43,1,43,5,47,2,10,47,51,1,5,51,55,1,55,13,59,1,59,9,63,2,9,63,67,1,6,67,71,1,71,13,75,1,75,10,79,1,5,79,83,1,10,83,87,1,5,87,91,1,91,9,95,2,13,95,99,1,5,99,103,2,103,9,107,1,5,107,111,2,111,9,115,1,115,6,119,2,13,119,123,1,123,5,127,1,127,9,131,1,131,10,135,1,13,135,139,2,9,139,143,1,5,143,147,1,13,147,151,1,151,2,155,1,10,155,0,99,2,14,0,0'
pp = pprint.PrettyPrinter(indent=4).pprint

def intcode(input):
    global offset
    store = input.split(',')
    store_length = len(store)
    output = []
    offset = 0

    def op1(line):
        store[int(line[3])] = str(int(line[1]) + int(line[2]))

    def op2(line):
        store[int(line[3])] = str(int(line[1]) * int(line[2]))

    operations = { '1': op1, '2': op2 }

    def run():
        global offset

        if offset == store_length: return

        val = store[offset]

        if val == '99':
            offset += 1
            return run()

        try:
            op = operations[val]
        except:
            raise Exception('No operation for:', val, 'and offset', offset)

        def get_fresh_line(): return [store[offset], store[offset + 1], store[offset + 2], store[offset + 3]]

        op(get_fresh_line())
        output.extend(get_fresh_line())

        offset += 4
        run()

    run()
    out = ','.join(str(x) for x in output)
    return out

def pprint_output(output):
    mem = output.split(',')
    for i in range(len(mem) - 1):
        if (i + 1) % 4 == 0: pp([mem[i], mem[1 + i], mem[2 + i], mem[3 + i]])

pprint_output(intcode(input1))
