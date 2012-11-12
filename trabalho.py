# -*- encoding: utf-8 -*-

from random import choice, randint, uniform
import os
from time import time, sleep

REGISTERS_AMMOUNT = 2000000
REGISTER_LENGTH = 64
DOCUMENT_LENGTH = 10
NAME_LENGTH = 15
ADDRESS_LENGTH = 20
SEPARATOR_LENGTH = 1
INDEX_ID_LENGTH = 10
INDEX_LENGTH = 22
DATA_SOURCE_FILEPATH = u'/usr/share/dict/words'
DATA_FILEPATH = u'data.txt'
INDEXES_FILENAME = u'indexes'
INDEXES_FILE_EXTENSION = u'.txt'
INDEXES_FILEPATH = INDEXES_FILENAME + INDEXES_FILE_EXTENSION
TEMP_FILEPATH = u'temp.txt'
GENDERS = ['M', 'F']
LINKED_LIST = None

class Register:
    """
        Class that represents a register.
    """
    pass


class LinkedListNode:
    """
        Represents a linked list node.
    """
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node
        self.content = ContentLinkedList()

class ContentLinkedListNode:
    """
        Represents a content linked list node.
    """
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class ContentLinkedList:
    """
        Class that represents a content linked list.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        """
            Adds a node to the end of the content linked list.
        """
        new_node = ContentLinkedListNode(data, None)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next_node = new_node

    def search(self, data):
        """
            Searches for a node with a certain string and returns it.
        """
        node = self.head
        while node is not None:
            if node.data.strip() == data.strip():
                return node
            node = node.next_node

    def print_all(self):
        """
            Prints all the nodes in a content list.
        """
        print("Nodes: " + self.stringify_nodes())

    def stringify_nodes(self):
        """
            Returns a string with all the nodes in the linked list.
        """
        content_string = ''
        first = True
        node = self.head
        while node is not None:
            if first:
                content_string += str(node.data)
                first = False
            else:
                content_string += str(', ' + str(node.data))
            node = node.next_node
        return content_string


class LinkedList:
    """
        Represents a linked list.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_in_place(self, value, content):
        """
            Inserts a certain value with its content in the appropriated
            place in the linked list.
        """
        if not self.head:
            self.append(value, content)
        elif self.head.data > value:
            self.prepend(value, content)
        else:
            node = self.head
            next_node = node.next_node
            found = False
            while not found or node:
                if value == node.data:
                    self.add_to_existent(node, content)
                    return True
                elif not next_node:
                    self.append(value, content)
                    return True
                elif value > node.data and value < next_node.data:
                    self.inset(node, value, content)
                    return True
                node = node.next_node
                next_node = node.next_node

    def add_to_existent(self, node, value):
        """
            Adds a value to the content of an existing linked list node.
        """
        node.content.append(value)

    def inset(self, node, data, content):
        """
            Adds a node in the middle of the linked list.
        """
        new_node = LinkedListNode(data, node.next_node)
        new_node.content.append(content)
        node.next_node = new_node
        if self.tail == node:
            self.tail = new_node

    def append(self, data, content):
        """
            Adds a node to the end of the linked list.
        """
        if self.tail is None:
            new_node = LinkedListNode(data, None)
            new_node.content.append(content)
            self.head = self.tail = new_node
        else:
            self.inset(self.tail, data, content)

    def prepend(self, data, content):
        """
            Adds a node in the beginning of the linked list.
        """
        new_node = LinkedListNode(data, self.head)
        new_node.content.append(content)
        self.head = new_node

    def search(self, data):
        """
            Searches for a certain data and prints the result.
        """
        node = self.head
        while node is not None:
            if node.data.strip() == data.strip():
                print('Results: ' + node.content.stringify_nodes())
                inner_node = node.content.head
                while inner_node is not None:
                    binary_search(inner_node.data, verbose=False)
                    inner_node = inner_node.next_node
            node = node.next_node

    def print_all(self):
        """
            Prints all the content of the linked list.
        """
        count = 0
        node = self.head
        while node is not None:
            print(str(node.data) + ' | Nodes: ' + \
                node.content.stringify_nodes())
            node = node.next_node
            count +=1


def generate_linked_list():
    """
        Generates a linked list based on the 'name' field
        on the registers.

        This is a timed function.
    """
    print
    initial_time = time()
    initial_partial_time = initial_time
    data_file = open(DATA_FILEPATH, 'Ur')
    data_file.seek(0, 0)
    content = data_file.read(DOCUMENT_LENGTH)
    data_file.seek(SEPARATOR_LENGTH, 1)
    reg = data_file.read(NAME_LENGTH)
    LINKED_LIST = LinkedList()
    index_counter = 0
    while index_counter < 1000:
        LINKED_LIST.insert_in_place(reg, content)
        index_counter += 1
        if index_counter % 1000 == 0:
            present_partial_time = time()
            elapsed_time = present_partial_time - initial_partial_time
            initial_partial_time = present_partial_time
            print('Time elapsed to index from %s to %s: %s' % \
                  (str(index_counter - 1000), str(index_counter), \
                   str(elapsed_time)))
 
        data_file.seek(REGISTER_LENGTH - NAME_LENGTH - SEPARATOR_LENGTH - \
                       DOCUMENT_LENGTH, 1)
        content = data_file.read(DOCUMENT_LENGTH)
        data_file.seek(SEPARATOR_LENGTH, 1)
        reg = data_file.read(NAME_LENGTH)

    LINKED_LIST.print_all()
    LINKED_LIST.search('Zambezian')
    final_time = time()
    data_file.close()

    print('Time to index %s registers: %s' % \
        (str(REGISTERS_AMMOUNT), str(final_time - initial_time)))


def create_register(source1, source2):
    """
        Creates a random register. Uses 2 source words to create it.
    """
    register = Register()
    register.document = randint(1000000000, 9999999999)
    register.name = (source1.strip().title())[:15]
    register.address = (u'Rua %s, %i' % \
            ((source2.strip().title())[:10],
            randint(0, 9999)))
    register.sex = choice(GENDERS)
    register.age = randint(0, 99)
    register.salary = round(uniform(700.00, 99999.00), 2)
    return register

def generate_register_text(register):
    """
        Returns the register string.
    """
    fixed_name = register.name + ((15 - len(register.name)) * ' ')
    fixed_address = register.address + ((20 - len(register.address)) * ' ')
    fixed_age = str(register.age) + ((2 - len(str(register.age))) * ' ')
    fixed_salary = str(register.salary) +\
                   ((10 - len(str(register.salary))) * ' ')
    return (u'%i|%s|%s|%s|%s|%s|' % (register.document, fixed_name,
                                fixed_address, register.sex,
                                fixed_age, fixed_salary))

def generate_registers():
    """
        Generates a certain ammount of registers,
        being the ammount stored in REGISTERS_AMMOUNT.

        This is a timed function.
    """
    print
    initial_time = time()
    f = open(DATA_SOURCE_FILEPATH, 'r')
    lines = f.readlines()
    lines_length = len(lines)
    try:
        os.remove(DATA_FILEPATH) 
    except:
        pass
    os.system('touch ' + DATA_FILEPATH)
    f = open(DATA_FILEPATH, 'a')

    for i in range(REGISTERS_AMMOUNT):
        r = create_register(lines[randint(0, lines_length - 1)],
                            lines[randint(0, lines_length - 1)])
        s = generate_register_text(r)
        f.write(s)

    final_time = time()
    f.close()

    print('Number of generated registers: ' + \
        str(get_size(DATA_FILEPATH)/REGISTER_LENGTH))

    print('Time to create %s registers: %s' % \
        (str(REGISTERS_AMMOUNT), str(final_time - initial_time)))


def generate_indexes():
    """
        Generate the indexes from the DATA_FILEPATH into the INDEXES_FILEPATH.

        This is a timed function.
    """
    print
    initial_time = time()
    initial_partial_time = time()
    data_file = open(DATA_FILEPATH, 'Ur')
    data_file.seek(0, 0)
    reg = data_file.read(DOCUMENT_LENGTH)
    try:
        os.remove(INDEXES_FILEPATH)
    except:
        pass
    ammount_registers = get_size(DATA_FILEPATH)/REGISTER_LENGTH
    ammount_index_files = ammount_registers / 100

    os.system('N=' + str(ammount_index_files) +\
              '; i=0; while [ $i != $N ]; do touch ' + \
              INDEXES_FILENAME + '$i' + INDEXES_FILE_EXTENSION +\
              '; i=$((i + 1)); done')
    index_counter = 0
    while reg != '':
        index_file_number = get_index_file(reg, ammount_index_files)
        index_file = open(INDEXES_FILENAME + str(index_file_number) + \
                          INDEXES_FILE_EXTENSION, 'r')
        size = get_size(INDEXES_FILENAME + str(index_file_number) +\
                        INDEXES_FILE_EXTENSION)
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
        temp_file = open(TEMP_FILEPATH, 'w')
        index_file.close()
        index_file = open(INDEXES_FILENAME + str(index_file_number) +\
                          INDEXES_FILE_EXTENSION, 'r')
        index_file.seek(0, 0)
        before = index_file.read(INDEX_LENGTH * (insert_position))
        after = index_file.read()

        #Adds the indexes before the new index, followed by the new index and, 
        #then, by the rest of the indexes.
        temp_file.write(before)
        temp_file.write(generate_index_text(reg, index_counter))
        temp_file.write(after)
        temp_file.close()

        #Removes the original indexes.txt file.
        os.remove(INDEXES_FILENAME + str(index_file_number) +\
                  INDEXES_FILE_EXTENSION)
        os.rename(TEMP_FILEPATH, INDEXES_FILENAME + str(index_file_number) +\
                  INDEXES_FILE_EXTENSION)

        index_counter += 1
        if index_counter % 10000 == 0:
            present_partial_time = time()
            elapsed_time = present_partial_time - initial_partial_time
            initial_partial_time = present_partial_time
            print('Time elapsed to index from %s to %s: %s' % \
                  (str(index_counter - 10000), str(index_counter),\
                   str(elapsed_time)))
            
        data_file.seek(REGISTER_LENGTH - DOCUMENT_LENGTH, 1)
        reg = data_file.read(DOCUMENT_LENGTH)
        
    f = open(INDEXES_FILEPATH, "w")
    for i in range(ammount_index_files):
        fh = open(INDEXES_FILENAME + str(i) + INDEXES_FILE_EXTENSION, 'r')
        f.write(fh.read())
        fh.close()
        os.remove(INDEXES_FILENAME + str(i) + INDEXES_FILE_EXTENSION)
    f.close()
    final_time = time()

    print('Number of generated indexes: ' + \
        str(get_size(INDEXES_FILEPATH)/INDEX_LENGTH))
    print('Time to execute the indexing of %s registers: %s' % \
        (str(ammount_registers), str(final_time - initial_time)))
    return 1


def generate_index_text(reg, index_counter):
    """
        Returns the index string of a register.
    """
    fixed_counter = str(index_counter) + \
                    ((INDEX_ID_LENGTH - len(str(index_counter))) * ' ')
    return (reg + '|' + fixed_counter + '|')

def is_substring(original_string, test_string):
    """
        Verifies if a string is a substring of another.
    """
    iterable_original = iter(original_string)
    iterable_test = iter(test_string)
    if len(test_string) > len(original_string):
        return False
    for i in range(len(test_string)):
        if iterable_test.next() != iterable_original.next():
            return False
    return True

def exhaustive_search(query_string, query_field):
    """
        Executes an exhaustive search using 'query_string'
        as the search key and 'query_field' to select in
        which field the exhaustive search will be done.

        This is a timed function.
    """
    print
    data_file = open(DATA_FILEPATH, 'Ur')
    data_file.seek(0, 0)
    initial_time = time()
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
                data_file.seek(-(DOCUMENT_LENGTH + SEPARATOR_LENGTH +\
                               NAME_LENGTH), 1)
                result = data_file.read(REGISTER_LENGTH)
            data_file.seek(REGISTER_LENGTH - NAME_LENGTH, 1)
            name = data_file.read(NAME_LENGTH)

    elif query_field == 'address':
        data_file.seek(DOCUMENT_LENGTH + SEPARATOR_LENGTH + NAME_LENGTH +\
                       SEPARATOR_LENGTH, 0)
        address = data_file.read(ADDRESS_LENGTH)
        while address and not result:
            if is_substring(address, query_string):
                data_file.seek(-(DOCUMENT_LENGTH + SEPARATOR_LENGTH +\
                               NAME_LENGTH + SEPARATOR_LENGTH +\
                               ADDRESS_LENGTH), 1)
                result = data_file.read(REGISTER_LENGTH)
            data_file.seek(REGISTER_LENGTH - ADDRESS_LENGTH, 1)
            address = data_file.read(ADDRESS_LENGTH)
    else:
        print('Invalid parameter')
        return False

    if not result:
        print('Not found')
    else:
        print('Found\nRegister: ' + result)
        final_time = time()
        print('Time to execute the exhaustive search on %s for the %s "%s": %s'\
              % (DATA_FILEPATH, query_field, query_string,\
                str(final_time - initial_time)))
    data_file.close()

def binary_search(search, source = INDEXES_FILEPATH,\
                  index_length = INDEX_LENGTH, verbose = True):
    """
        Executes a binary search using 'search' as the search key,
        'source' as the place where the search will be made
        and 'index_length' as the length of the index that will be searched.

        This is a timed function.
    """

    if verbose:
        print
    initial_time = time()
    index_file = open(INDEXES_FILEPATH, 'r')
    index_file.seek(0, 0)
    index = index_file.read(index_length)

    if int(search) < int(index[:10]):
        final_time = time()
        print('Not found')
        print('Time to execute the binary search on %s: %s' % \
            (source, str(final_time - initial_time)))
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
            final_time = time()
            print('Not found')
            print('Time to execute the binary search on %s: %s' % \
                (source, str(final_time - initial_time)))
            return -1
        index_file.seek(center * index_length, 0)
        index = index_file.read(index_length)
        if right_path < left_path:
            final_time = time()
            print('Not found')
            print('Time to execute the binary search on %s: %s' % \
                (source, str(final_time - initial_time)))
            return -1
        if int(search) == int(index[:10]):
            final_time = time()
            if not verbose:
                print get_register(int(index[11:21]))
            else:
                print('Found\nIndex: ' + index + '\nRegister: '+\
                      get_register(int(index[11:21])))
                print('Time to execute the binary search on %s: %s' % \
                    (source, str(final_time - initial_time)))
            return 1
        elif int(search) < int(index[:10]):
            right_path = center
        else:
            left_path = center

        previous_center = center


def get_index_file(reg, ammount_index_files):
    """
        Get the index file on which the new index must be stored.
    """
    return int(reg) / (10000000000 / ammount_index_files)

def get_register(access_key):
    """
        Get the register text using access_key as the argument to seek it.
    """
    data_file = open(DATA_FILEPATH, 'r')
    data_file.seek(access_key * REGISTER_LENGTH)
    register = data_file.read(REGISTER_LENGTH)
    data_file.close()
    return register

def get_size(filepath):
    """
        Gets the size of a certain file.
    """
    return os.path.getsize(filepath)

if __name__ == '__main__':
    generate_linked_list()
