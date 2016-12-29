# decision trees and tree search

# first version is just a binary tree


class BinaryTree(object):
    def __init__(self, value):
        self.value = value
        self.leftBranch = None
        self.rightBranch = None
        self.parent = None

    def setLeftBranch(self, node):
        self.leftBranch = node

    def setRightBranch(self, node):
        self.rightBranch = node

    def setParent(self, parent):
        self.parent = parent

    def getValue(self):
        return self.value

    def getLeftBranch(self):
        return self.leftBranch

    def getRightBranch(self):
        return self.rightBranch

    def getParent(self):
        return self.parent

    def __str__(self):
        return self.value


def dfs_binary(root, fcn):
    queue = [root]
    while len(queue) > 0:
        print('at node ' + str(queue[0].getValue()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            if temp.getRightBranch():
                queue.insert(0, temp.getRightBranch())
            if temp.getLeftBranch():
                queue.insert(0, temp.getLeftBranch())
    return False


def bfs_binary(root, fcn):
    queue = [root]
    while len(queue) > 0:
        print('at node ' + str(queue[0].getValue()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            if temp.getLeftBranch():
                queue.append(temp.getLeftBranch())
            if temp.getRightBranch():
                queue.append(temp.getRightBranch())
    return False


def dfs_binary_ordered(root, fcn, ltFcn):
    queue = [root]
    while len(queue) > 0:
        if fcn(queue[0]):
            return True
        elif ltFcn(queue[0]):
            temp = queue.pop(0)
            if temp.getLeftBranch():
                queue.insert(0, temp.getLeftBranch())
        else:
            temp = queue.pop(0)
            if temp.getRightBranch():
                queue.insert(0, temp.getRightBranch())
    return False


n5 = BinaryTree(5)
n2 = BinaryTree(2)
n1 = BinaryTree(1)
n4 = BinaryTree(4)
n8 = BinaryTree(8)
n6 = BinaryTree(6)
n7 = BinaryTree(7)
n3 = BinaryTree(3)

n5.setLeftBranch(n2)
n2.setParent(n5)
n5.setRightBranch(n8)
n8.setParent(n5)
n2.setLeftBranch(n1)
n1.setParent(n2)
n2.setRightBranch(n4)
n4.setParent(n2)
n8.setLeftBranch(n6)
n6.setParent(n8)
n6.setRightBranch(n7)
n7.setParent(n6)
n4.setLeftBranch(n3)
n3.setParent(n4)


def find6(node):
    return node.getValue() == 6


def find10(node):
    return node.getValue() == 10


def find2(node):
    return node.getValue() == 2


def lt6(node):
    return node.getValue() > 6


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
            if temp.getRightBranch():
                queue.insert(0, temp.getRightBranch())
            if temp.getLeftBranch():
                queue.insert(0, temp.getLeftBranch())
    return False


def trace_path(node):
    if not node.getParent():
        return [node]
    else:
        return [node] + trace_path(node.getParent())


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
        here.setLeftBranch(withelt)
        here.setRightBranch(withoutelt)
        return here


def dfs_d_tree(root, valueFcn, constraintFcn):
    queue = [root]
    best = None
    visited = 0
    while len(queue) > 0:
        visited += 1
        if constraintFcn(queue[0].getValue()):
            if best == None:
                best = queue[0]
                print(best.getValue())
            elif valueFcn(queue[0].getValue()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.getValue())
            temp = queue.pop(0)
            if temp.getRightBranch():
                queue.insert(0, temp.getRightBranch())
            if temp.getLeftBranch():
                queue.insert(0, temp.getLeftBranch())
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
        if constraintFcn(queue[0].getValue()):
            if best == None:
                best = queue[0]
                print(best.getValue())
            elif valueFcn(queue[0].getValue()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.getValue())
            temp = queue.pop(0)
            if temp.getLeftBranch():
                queue.append(temp.getLeftBranch())
            if temp.getRightBranch():
                queue.append(temp.getRightBranch())
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
        if constraintFcn(stack[0].getValue()):
            if best == None:
                best = stack[0]
                print(best.getValue())
            elif valueFcn(stack[0].getValue()) > valueFcn(best.getValue()):
                best = stack[0]
                print(best.getValue())
            if stopFcn(best.getValue()):
                print('visited', visited)
                return best
            temp = stack.pop(0)
            if temp.getRightBranch():
                stack.insert(0, temp.getRightBranch())
            if temp.getLeftBranch():
                stack.insert(0, temp.getLeftBranch())
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
        if constraintFcn(queue[0].getValue()):
            if best == None:
                best = queue[0]
                print(best.getValue())
            elif valueFcn(queue[0].getValue()) > valueFcn(best.getValue()):
                best = queue[0]
                print(best.getValue())
            if stopFcn(best.getValue()):
                print('visited', visited)
                return best
            temp = queue.pop(0)
            if temp.getLeftBranch():
                queue.append(temp.getLeftBranch())
            if temp.getRightBranch():
                queue.append(temp.getRightBranch())
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
        print('at node ' + str(queue[0].getValue()))
        if fcn(queue[0]):
            return True
        else:
            temp = queue.pop(0)
            seen.append(temp)
            if temp.getRightBranch():
                if not temp.getRightBranch() in seen:
                    queue.insert(0, temp.getRightBranch())
            if temp.getLeftBranch():
                if not temp.getLeftBranch() in seen:
                    queue.insert(0, temp.getLeftBranch())
    return False


# comment out

n3.setLeftBranch(n5)
n5.setParent(n3)

# run DFSBinary(n5, find6)
