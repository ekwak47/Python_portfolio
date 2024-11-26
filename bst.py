# Name: Eric Kwak
# OSU Email: kwake@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: BST/AVL Tree implementation
# Due Date: 5/22/23
# Description: BST implementation methods
import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """
    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None
        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.
        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True
    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree
        """
        if self._root is None:  # if the root is None, inserts the value to the root
            self._root = BSTNode(value)
        else:  # uses recursion to insert a value
            self._insert(value, self._root)  # function which starts at the root and moves as directed

    def _insert(self, value: object, curr_node):
        """helper function to add a value to the BST"""
        if value < curr_node.value:  # if value is less than the current node
            if curr_node.left is None:  # if the left child is unoccupied, the value becomes the left child
                curr_node.left = BSTNode(value)
            else:  # calls the method and inserts the value back into the function
                self._insert(value, curr_node.left)

        else:  # if value is greater than or equal to the current node
            if curr_node.right is None:  # occupies the right child value to the current node
                curr_node.right = BSTNode(value)
            else:  # the value goes back into the _insert function
                self._insert(value, curr_node.right)

    def remove(self, value: object) -> bool:
        """
        Method which removes a value from the tree
        """

        if not self.contains(value):  # uses the contain method to check if value exists
            return False

        def _search_del(root, key):
            """
            Separate add-on function which searches and deletes selected node while calling itself recursively
            """
            if root is None:
                return False

            if root.value < key:
                root.right = _search_del(root.right, key)

            elif root.value > key:
                root.left = _search_del(root.left, key)

            else:

                if root.left and root.right is not None:  # both left and right children

                    if root.right.left:  # if there is a leftmost node in right subtree
                        leftmost = root.right.left
                        leftmost_parent = root.right

                        while leftmost.left:  # searches for the leftmost node
                            leftmost = leftmost.left
                            leftmost_parent = leftmost_parent.left

                        leftmost_parent.left = leftmost.right  # replaces node

                        leftmost.left, leftmost.right = root.left, root.right  # swaps nodes

                        root = leftmost   # replace the target node with the leftmost node

                    else:

                        root.right.left = root.left  # if the right subtree does not have a left,
                        # it replaces the target node with the right child
                        root = root.right

                elif root.left:  # only a left child
                    root = root.left
                elif root.right:  # only a right child
                    root = root.right

                else:  # target node has no left or right children
                    root = None
            return root

        self._root = _search_del(self._root, value)  # updates the tree after
        return True  # returns True if a value is deleted

    def contains(self, value: object) -> bool:
        """
        Method which returns true if the value is in the tree, otherwise, it returns False
        """
        node = BSTNode(value)
        node = self._root  # will iterate through the tree, sets node to the root node
        while node is not None:  # iterates through the tree
            if value == node.value:  # if node is found, returns True
                return True
            elif value > node.value:  # continues moving to the right or left depending on if the node is larger or less
                node = node.right
            else:
                node = node.left

        return False

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal of the tree, then returns a queue which contains the values of the nodes
        """
        q = Queue()  # initializes an empty Queue to insert values

        def in_order(node):  # helper function which traverses through the tree and returns a Queue of the values
            """Returns a queue of the values in the tree in order"""
            if node is None:  # returns an empty Queue if the tree is empty
                return
            else:  # traverses the tree and adds each value
                in_order(node.left)
                q.enqueue(node.value)
                in_order(node.right)
            return q
        in_order(self._root)
        return q

    def find_min(self) -> object:
        """
        Returns the lowest value in the tree
        """
        if self._root is None:  # returns None if node value is empty
            return None
        curr_node = self._root  # sets the node at the root node
        while curr_node.left is not None:  # traverses to each value left of the tree value
            curr_node = curr_node.left
        return curr_node.value

    def find_max(self) -> object:
        """
        returns the highest value in the tree
        """
        if self._root is None:  # returns None if node value is empty
            return None
        curr_node = self._root  # sets the node at the root node
        while curr_node.right is not None:  # traverses to each value right of the tree value
            curr_node = curr_node.right
        return curr_node.value

    def is_empty(self) -> bool:
        """
        Method which returns True if the tree is empty, otherwise returns false if there exists elements
        """
        if self._root is None:  # if the root node has no value, there is no tree
            return True  # returns True if empty
        else:
            return False  # if a value occupies the root node, returns False

    def make_empty(self) -> None:
        """
        Method removes all values from the tree
        """
        self._root = None  # Sets the root node to None and clears all the other values
        return


# ------------------- BASIC TESTING -----------------------------------------
if __name__ == '__main__':
    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)
    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')
    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)
    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))
    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))
    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())
    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())
    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())
    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())
    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())
    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
