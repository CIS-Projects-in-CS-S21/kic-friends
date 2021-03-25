from functools import total_ordering
from typing import List


def left_child_index(i):
    return 2 * i + 1


def right_child_index(i):
    return 2 * i + 2


def parent_index(i):
    return (i - 1) // 2


@total_ordering
class Node:

    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __eq__(self, other):
        return other.weight == self.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def change_weight(self, new_weight):
        self.weight = new_weight


class HeapQueue:

    def __init__(self):
        self.elements: 'List[Node]' = list()

    def __len__(self):
        return self.size()

    def size(self):
        return len(self.elements)

    def insert(self, item, weight):
        # if the item is already in the queue, return
        if self.search(item) != -1:
            return
        # add the item to the left most slot, and push it up until the min heap property is satisfied
        self.elements.append(Node(weight, item))
        index = len(self.elements) - 1
        parent = parent_index(index)
        while index != 0 and self.elements[parent] > self.elements[index]:
            temp = self.elements[parent]
            self.elements[parent] = self.elements[index]
            self.elements[index] = temp
            index = parent
            parent = parent_index(index)

    def remove_top(self):
        if len(self.elements) == 0:
            return None
        if len(self.elements) == 1:
            elem = self.elements.pop()
            return elem.weight, elem.value
        # remove the top of the heap, take the last element in the heap and move it to the top, then heapify
        to_return = self.elements[0]
        self.elements[0] = self.elements.pop()
        self.heapify(0)
        return to_return.weight, to_return.value

    def heapify(self, root_index):
        # recursively construct the heap by swapping parents and children as needed
        left = left_child_index(root_index)
        right = right_child_index(root_index)
        min_val = root_index
        if left < len(self.elements) and self.elements[left] < self.elements[min_val]:
            min_val = left
        if right < len(self.elements) and self.elements[right] < self.elements[min_val]:
            min_val = right
        if min_val != root_index:
            temp = self.elements[root_index]
            self.elements[root_index] = self.elements[min_val]
            self.elements[min_val] = temp
            self.heapify(min_val)

    def search(self, value):
        for index, element in enumerate(self.elements):
            if value == element.value:
                return index
        return -1

    def decrease_weight(self, value, new_weight):
        idx = self.search(value)
        if idx == -1:
            raise AttributeError()
        self.elements[idx].change_weight(new_weight)
        parent = parent_index(idx)
        while idx != 0 and self.elements[parent] > self.elements[idx]:
            temp = self.elements[parent]
            self.elements[parent] = self.elements[idx]
            self.elements[idx] = temp
            idx = parent
            parent = parent_index(idx)
