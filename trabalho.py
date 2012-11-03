# -*- encoding: utf-8 -*-

import os
import time

REGISTER_LENGTH = 64
DOCUMENT_LENGTH = 10
NAME_LENGTH = 15
ADDRESS_LENGTH = 20
SEPARATOR_LENGTH = 1

INDEX_ID_LENGTH = 10
INDEX_LENGTH = 22
DATA_FILEPATH = u'data.txt'
INDEXES_FILEPATH = u'indexes.txt'
TEMP_FILEPATH = u'temp.txt'

data_file = open(DATA_FILEPATH, 'Ur')

def is_substring(original_string, test_string):
    iterable_original = iter(original_string)
    iterable_test = iter(test_string)
    if len(test_string) > len(original_string):
        return False
    for i in range(len(test_string)):
        if iterable_test.next() != iterable_original.next():
            return False
    return True

def exhaustive_search(query_string, query_field):
    result = ''
    if query_field == 'document':
        data_file.seek(0, 0)
        document = data_file.read(DOCUMENT_LENGTH)
        while document and not result:
            if document == query_string:
                data_file.seek(-(DOCUMENT_LENGTH), 1)
                result = data_file.read(REGISTER_LENGTH)
            data_file.seek(REGISTER_LENGTH - DOCUMENT_LENGTH, 1)
            document = data_file.read(DOCUMENT_LENGTH)

    elif query_field == 'name':
        data_file.seek(DOCUMENT_LENGTH + SEPARATOR_LENGTH, 0)
        name = data_file.read(NAME_LENGTH)
        while name and not result:
            if is_substring(name, query_string):
                data_file.seek(-(DOCUMENT_LENGTH + SEPARATOR_LENGTH + NAME_LENGTH), 1)
                result = data_file.read(REGISTER_LENGTH)
            data_file.seek(REGISTER_LENGTH - NAME_LENGTH, 1)
            name = data_file.read(NAME_LENGTH)

    elif query_field == 'address':
        data_file.seek(DOCUMENT_LENGTH + SEPARATOR_LENGTH + NAME_LENGTH + SEPARATOR_LENGTH, 0)
        address = data_file.read(ADDRESS_LENGTH)
        while address and not result:
            if is_substring(address, query_string):
                data_file.seek(-(DOCUMENT_LENGTH + SEPARATOR_LENGTH + NAME_LENGTH + SEPARATOR_LENGTH + ADDRESS_LENGTH), 1)
                result = data_file.read(REGISTER_LENGTH)
            data_file.seek(REGISTER_LENGTH - ADDRESS_LENGTH, 1)
            address = data_file.read(ADDRESS_LENGTH)
    else:
        print('Parâmetro Inválido!')
        return False

    if not result:
        print('Não encontrado!')
    else:
        print('Encontrado!')
        print(result)

def binary_search(search, source = INDEXES_FILEPATH, index_length = INDEX_LENGTH):
    index_file = open(INDEXES_FILEPATH, 'r')
    index_file.seek(0, 0)
    index = index_file.read(index_length)

    if int(search) < int(index[:10]):
        return -1

    size = get_size(INDEXES_FILEPATH)
    indexes_ammount = (size/index_length)

    right_path = indexes_ammount
    left_path = 0
    center = 0
    previous_center = -1
    while 1:
        center = (left_path + right_path) / 2
        if center == previous_center:
            return -1
        index_file.seek(center * index_length, 0)
        index = index_file.read(index_length)
        print(index)
        print('Left: ' + str(left_path) + \
              ' Right: ' + str(right_path) + \
              ' Center: ' + str(center))
        if right_path < left_path:
            return -1
        if int(search) == int(index[:10]):
            print('Encontrado: ' + index)
            return 1
        elif int(search) < int(index[:10]):
            right_path = center
        else:
            left_path = center

        previous_center = center


def generate_indexes():
    data_file.seek(0, 0)
    reg = data_file.read(DOCUMENT_LENGTH)
    try:
        os.remove(INDEXES_FILEPATH)
    except:
        pass
    index_counter = 0
    os.system('touch ' + INDEXES_FILEPATH)
    while reg != '':
        index_file = open(INDEXES_FILEPATH, 'r')
        size = get_size(INDEXES_FILEPATH)
        indexes_ammount = (size/INDEX_LENGTH)
        right = indexes_ammount
        left = 0
        center = (left + right) / 2
        while (center != left):
            index_file.seek(center * INDEX_LENGTH, 0)
            index = index_file.read(INDEX_LENGTH)
            if int(reg) > int(index[:10]):
                left = center
            else:
                right = center
            center = (left + right) / 2

        index_file.seek(center * INDEX_LENGTH, 0)
        index = index_file.read(INDEX_LENGTH)
        if left != right and int(reg) > int(index[:10]):
            center = right

        insert_position = center

        #Creates a temporary file that will receive the content of the new file.
        os.system('touch ' + TEMP_FILEPATH)
        temp_file = open(TEMP_FILEPATH, 'a')
        index_file.close()
        index_file = open(INDEXES_FILEPATH, 'r')
        index_file.seek(0, 0)
        before = index_file.read(INDEX_LENGTH * (insert_position))
        after = index_file.read()

        #Adds the indexes before the new index, followed by the new index and, then,
        #by the rest of the indexes.
        temp_file.write(before)
        temp_file.write(generate_index_text(reg, index_counter))
        temp_file.write(after)
        temp_file.close()

        #Removes the original indexes.txt file.
        os.remove(INDEXES_FILEPATH)
        os.rename('temp.txt', 'indexes.txt')

        index_counter += 1
        data_file.seek(REGISTER_LENGTH - DOCUMENT_LENGTH, 1)
        reg = data_file.read(DOCUMENT_LENGTH)

def generate_index_text(reg, index_counter):
    fixed_counter = str(index_counter) + \
                    ((INDEX_ID_LENGTH - len(str(index_counter))) * ' ')
    return (reg + '|' + fixed_counter + '|')

def get_size(filepath):
    return os.path.getsize(filepath)

if __name__ == '__main__':
    start_time = time.clock()
    #binary_search(1936325214)
    #binary_search(1936325215)
    generate_indexes()
    elapsed_time = time.clock() - start_time
    size = get_size(INDEXES_FILEPATH)
    print('Tempo para realizar a indexação: ' + str(elapsed_time))
