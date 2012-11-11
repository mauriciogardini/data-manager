import random

class BTree:
    root = None

    def __init__(self, value):
        self.root = Node(value)

    def add_node(self, value, node=None, parent=None):
        if not node:
            node = self.root
        if node.has_children():
            if value > node.value1 and value > node.value2:
                return self.add_node(value, node.right, node)
            elif value < node.value1 and value < node.value2:
                return self.add_node(value, node.left, node)
            else:
                return self.add_node(value, node.middle, node)
        else:
            if node.has_available_spaces():
                return node.add_value(value)
            else:
                self.promote_value(value, node)

    def promote_value(self, value, node):
        if not node:
            new_root = Node(value, None)
            self.root = new_root
            return new_root
        elif node.has_available_spaces():
            return node.add_value(value)
        else:
            center = node.get_center_value(value)
            left = node.get_left_value(value)
            right = node.get_right_value(value)
            center_parent = self.get_parent(center)
            if not center_parent:
                self.root = Node(center)
                self.root.left = Node(left)
                self.root.middle = Node(right)
            elif center_parent.has_available_spaces():
                center_parent.add_value(center)
                value_position = center_parent.get_value_position(center)
                if value_position == 'left':
                    center_parent.left = Node(left)
                    center_parent.middle = Node(right)
                elif value_position == 'right':
                    center_parent.middle = Node(left)
                    center_parent.middle = Node(right)
            else:
                self.promote_value(center, center_parent)



    def get_parent(self, value, node=None, parent_node=None):
        if not node and not parent_node:
            parent_node = None
            node = self.root
        if not node:
            return None
        elif node.value1 == value or node.value2 == value:
            return parent_node
        else:
            if node.has_children():
                return (self.get_parent(value, node.left, node) or\
                        self.get_parent(value, node.middle, node) or\
                        self.get_parent(value, node.right, node))
            else:
                return None

    def print_tree(self):
        if self.root:
            if self.root.value1:
                print(self.root.value1)
            if self.root.value2:
                print(self.root.value2)
            self.print_node(self.root.left, 1)
            self.print_node(self.root.middle, 1)
            self.print_node(self.root.right, 1)

    def print_node(self, node, level):
        identifier = random.randint(1, 1000)
        if node:
            self.print_node(node.left, level + 1)
            if node.value1:
                print(str(level * '-') + str(node.value1) + ' (' + str(identifier) + ')')
            self.print_node(node.middle, level + 1)
            if node.value2:
                print(str(level * '-') + str(node.value2) + ' (' + str(identifier) + ')')
            self.print_node(node.right, level + 1)

class Node:
    value1 = None
    value2 = None
    left = None
    middle = None
    right = None

    def __init__(self, value1):
        self.value1 = value1

    def get_value_position(self, value):
        if self.value1 == value:
            return 'left'
        elif self.value2 == value:
            return 'right'
        else:
            return None

    def add_value(self, value):
        if self.has_available_spaces():
            if self.value1:
                self.value2 = value
                if self.value1 > value:
                    self.switch_values()
                return self
            elif self.value2:
                self.value1 = value
                if self.value2 < value:
                    self.switch_values()
                return self
        return False

    def get_center_value(self, value):
        if value > self.value1 and value < self.value2:
            return value
        elif value < self.value1:
            return self.value1
        elif value > self.value2:
            return self.value2

    def get_left_value(self, value):
        if value < self.value1 and value < self.value2:
            return value
        elif self.value1 < value and self.value1 < self.value2:
            return self.value1
        elif self.value2 < value and self.value2 < self.value1:
            return self.value2

    def get_right_value(self, value):
        if value > self.value1 and value > self.value2:
            return value
        elif self.value1 > value and self.value1 > self.value2:
            return self.value1
        elif self.value2 > value and self.value2 > self.value1:
            return self.value2

    def switch_values(self):
        temp = self.value1
        self.value1 = self.value2
        self.value2 = temp

    def has_available_spaces(self):
        return True if (not self.value1 or not self.value2) else False

    def has_children(self):
        return True if (self.left or self.middle or self.right) else False

if __name__ == '__main__':
    tree = BTree(1)
    #for i in range(2):
    tree.add_node(2)
    tree.add_node(3)
    tree.add_node(4)
    tree.print_tree()

