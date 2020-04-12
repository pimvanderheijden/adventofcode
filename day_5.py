from intcode import intcode


reader = open("input_day_5.txt", "r")
input1 = reader.read()
reader.close()

res = intcode(input1, False, False, '0')
print(res['output_full'])
print(res['output_num'])