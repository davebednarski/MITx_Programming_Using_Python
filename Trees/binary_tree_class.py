# decision trees and tree search

# first version is just a binary tree


class BinaryTree(object):
    def __init__(self, value):
        self.value = value
        self.leftBranch = None
        self.rightBranch = None
        self.parent = None

    def set_left_branch(self, node):
        self.leftBranch = node

    def set_right_branch(self, node):
        self.rightBranch = node

    def set_parent(self, parent):
        self.parent = parent

    def get_value(self):
        return self.value

    def get_left_branch(self):
        return self.leftBranch

    def get_right_branch(self):
        return self.rightBranch

    def get_parent(self):
        return self.parent

    def __str__(self):
        return self.value


def dfs_binary(root, fcn):
    queue = [root]
    while len(queue) > 0:
        print('at node ' + str(queue[0].get_value()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            if temp.get_right_branch():
                queue.insert(0, temp.get_right_branch())
            if temp.get_left_branch():
                queue.insert(0, temp.get_left_branch())
    return False


def bfs_binary(root, fcn):
    queue = [root]
    while len(queue) > 0:
        print('at node ' + str(queue[0].get_value()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            if temp.get_left_branch():
                queue.append(temp.get_left_branch())
            if temp.get_right_branch():
                queue.append(temp.get_right_branch())
    return False


def dfs_binary_ordered(root, fcn, ltFcn):
    queue = [root]
    while len(queue) > 0:
        if fcn(queue[0]):
            return True
        elif ltFcn(queue[0]):
            temp = queue.pop(0)
            if temp.get_left_branch():
                queue.insert(0, temp.get_left_branch())
        else:
            temp = queue.pop(0)
            if temp.get_right_branch():
                queue.insert(0, temp.get_right_branch())
    return False


n5 = BinaryTree(5)
n2 = BinaryTree(2)
n1 = BinaryTree(1)
n4 = BinaryTree(4)
n8 = BinaryTree(8)
n6 = BinaryTree(6)
n7 = BinaryTree(7)
n3 = BinaryTree(3)

n5.set_left_branch(n2)
n2.set_parent(n5)
n5.set_right_branch(n8)
n8.set_parent(n5)
n2.set_left_branch(n1)
n1.set_parent(n2)
n2.set_right_branch(n4)
n4.set_parent(n2)
n8.set_left_branch(n6)
n6.set_parent(n8)
n6.set_right_branch(n7)
n7.set_parent(n6)
n4.set_left_branch(n3)
n3.set_parent(n4)


def find6(node):
    return node.get_value() == 6


def find10(node):
    return node.get_value() == 10


def find2(node):
    return node.get_value() == 2


def lt6(node):
    return node.get_value() > 6


# test examples

print('DFS')
dfs_binary(n5, find6)

print('')
print('BFS')
bfs_binary(n5, find6)


# if we wanted to return the path that got to the goal, would need to modify

def dfs_binary_path(root, fcn):
    queue = [root]
    while len(queue) > 0:
        if fcn(queue[0]):
            return trace_path(queue[0])
        else:
            temp = queue.pop(0)
            if temp.get_right_branch():
                queue.insert(0, temp.get_right_branch())
            if temp.get_left_branch():
                queue.insert(0, temp.get_left_branch())
    return False


def trace_path(node):
    if not node.get_parent():
        return [node]
    else:
        return [node] + trace_path(node.get_parent())


print('')
print('DFS path')
pathTo6 = dfs_binary_path(n5, find6)
print([e.getValue() for e in pathTo6])


# make a decision tree
# for efficiency should really generate on the fly, but here will build
# and then search


def build_d_tree(sofar, todo):
    if len(todo) == 0:
        return BinaryTree(sofar)
    else:
        withelt = build_d_tree(sofar + [todo[0]], todo[1:])
        withoutelt = build_d_tree(sofar, todo[1:])
        here = BinaryTree(sofar)
        here.set_left_branch(withelt)
        here.set_right_branch(withoutelt)
        return here


def dfs_d_tree(root, valueFcn, constraintFcn):
    queue = [root]
    best = None
    visited = 0
    while len(queue) > 0:
        visited += 1
        if constraintFcn(queue[0].get_value()):
            if best == None:
                best = queue[0]
                print(best.get_value())
            elif valueFcn(queue[0].get_value()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.get_value())
            temp = queue.pop(0)
            if temp.get_right_branch():
                queue.insert(0, temp.get_right_branch())
            if temp.get_left_branch():
                queue.insert(0, temp.get_left_branch())
        else:
            queue.pop(0)
    print('visited', visited)
    return best


def bfs_d_tree(root, valueFcn, constraintFcn):
    queue = [root]
    best = None
    visited = 0
    while len(queue) > 0:
        visited += 1
        if constraintFcn(queue[0].get_value()):
            if best == None:
                best = queue[0]
                print(best.get_value())
            elif valueFcn(queue[0].get_value()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.get_value())
            temp = queue.pop(0)
            if temp.get_left_branch():
                queue.append(temp.get_left_branch())
            if temp.get_right_branch():
                queue.append(temp.get_right_branch())
        else:
            queue.pop(0)
    print('visited', visited)
    return best


a = [6, 3]
b = [7, 2]
c = [8, 4]
d = [9, 5]

treeTest = build_d_tree([], [a, b, c, d])


def sum_values(lst):
    vals = [e[0] for e in lst]
    return sum(vals)


def sum_weights(lst):
    wts = [e[1] for e in lst]
    return sum(wts)


def weights_below_10(lst):
    return sum_weights(lst) <= 10


def weights_below_6(lst):
    return sum_weights(lst) <= 6


print('')
print('DFS decision tree')
foobar = dfs_d_tree(treeTest, sum_values, weights_below_10)
print(foobar.getValue())

print('')
print('BFS decision tree')
foobarnew = bfs_d_tree(treeTest, sum_values, weights_below_10)
print(foobarnew.getValue())


def dfs_d_tree_good_enough(root, valueFcn, constraintFcn, stopFcn):
    stack = [root]
    best = None
    visited = 0
    while len(stack) > 0:
        visited += 1
        if constraintFcn(stack[0].get_value()):
            if best == None:
                best = stack[0]
                print(best.get_value())
            elif valueFcn(stack[0].get_value()) > valueFcn(best.getValue()):
                best = stack[0]
                print(best.get_value())
            if stopFcn(best.getValue()):
                print('visited', visited)
                return best
            temp = stack.pop(0)
            if temp.get_right_branch():
                stack.insert(0, temp.get_right_branch())
            if temp.get_left_branch():
                stack.insert(0, temp.get_left_branch())
        else:
            stack.pop(0)
    print('visited', visited)
    return best


def bfs_d_tree_good_enough(root, valueFcn, constraintFcn, stopFcn):
    queue = [root]
    best = None
    visited = 0
    while len(queue) > 0:
        visited += 1
        if constraintFcn(queue[0].get_value()):
            if best == None:
                best = queue[0]
                print(best.get_value())
            elif valueFcn(queue[0].get_value()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.get_value())
            if stopFcn(best.getValue()):
                print('visited', visited)
                return best
            temp = queue.pop(0)
            if temp.get_left_branch():
                queue.append(temp.get_left_branch())
            if temp.get_right_branch():
                queue.append(temp.get_right_branch())
        else:
            queue.pop(0)
    print('visited', visited)
    return best


def at_least_15(lst):
    return sum_values(lst) >= 15


print('')
print('DFS decision tree good enough')
foobar = dfs_d_tree_good_enough(treeTest, sum_values, weights_below_10,
                                at_least_15)
print(foobar.getValue())

print('')
print('BFS decision tree good enough')
foobarnew = bfs_d_tree_good_enough(treeTest, sum_values, weights_below_10,
                                   at_least_15)
print(foobarnew.getValue())


def dt_implicit(toConsider, avail):
    if toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0][1] > avail:
        result = dt_implicit(toConsider[1:], avail)
    else:
        nextItem = toConsider[0]
        withVal, withToTake = dt_implicit(toConsider[1:], avail - nextItem[1])
        withVal += nextItem[0]
        withoutVal, withoutToTake = dt_implicit(toConsider[1:], avail)
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result


stuff = [a, b, c, d]

val, taken = dt_implicit(stuff, 10)

print('')
print('implicit decision search')
print('value of stuff')
print(val)
print('actual stuff')
print(taken)


def dfs_binary_no_loop(root, fcn):
    queue = [root]
    seen = []
    while len(queue) > 0:
        print('at node ' + str(queue[0].get_value()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            seen.append(temp)
            if temp.get_right_branch():
                if not temp.get_right_branch() in seen:
                    queue.insert(0, temp.get_right_branch())
            if temp.get_left_branch():
                if not temp.get_left_branch() in seen:
                    queue.insert(0, temp.get_left_branch())
    return False


# comment out

n3.set_left_branch(n5)
n5.set_parent(n3)

# run DFSBinary(n5, find6)
