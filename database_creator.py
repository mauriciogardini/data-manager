# -*- encoding: utf-8 -*-

from random import choice, randint, uniform
import time
import os

f = open('/usr/share/dict/words', 'r')
lines = f.readlines()
sexes = ['M', 'F']
lines_length = len(lines)

class Register:
    pass

def create_register():
    register = Register()
    register.document = randint(1000000000, 9999999999)
    register.name = (lines[randint(0, lines_length - 1)].strip().title())[:15]
    register.address = (u'Rua %s, %i' % \
            ((lines[randint(0, lines_length - 1)].strip().title())[:10],
            randint(0, 9999)))
    register.sex = choice(sexes)
    register.age = randint(0, 99)
    register.salary = round(uniform(700.00, 99999.00), 2)
    return register

def print_register(register):
    fixed_name = register.name + ((15 - len(register.name)) * ' ')
    fixed_address = register.address + ((20 - len(register.address)) * ' ')
    fixed_age = str(register.age) + ((2 - len(str(register.age))) * ' ')
    fixed_salary = str(register.salary) + ((10 - len(str(register.salary))) * ' ')
    return (u'%i|%s|%s|%s|%s|%s|' % (register.document, fixed_name,
                                   fixed_address, register.sex,
                                   fixed_age, fixed_salary))

def generate_database(registers_ammount):
    try:
        os.remove('data.txt') 
    except:
        pass
    os.system('touch data.txt')
    f = open('data.txt', 'a')

    for i in range(registers_ammount):
        r = create_register()
        s = print_register(r)
        f.write(s)

def get_size():
    return os.path.getsize('data.txt')

if __name__ == '__main__':
    start_time = time.clock()
    generate_database(100)
    elapsed_time = time.clock() - start_time
    print('Tempo para a criação dos registros: ' + str(elapsed_time))
    print('Tamanho do arquivo gerado: ' + str(get_size()))
    print('Quantidade de registros criados: ' + str(get_size()/64))
