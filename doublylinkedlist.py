# doublylinkedlist.py by nonetypes
# Last revised on 02/04/2021

class Node:
    """Node obect to make up the links within a DoublyLinkedList.

    Contains an item and the next and previous nodes in the chain.
    """
    def __init__(self, item=None):
        self.item = item
        self.prev_node = None
        self.next_node = None

    def __repr__(self):
        return str(self.item)


class DoublyLinkedList:
    """Linear data structure -- list like object.
    Contains a head node and a tail node.
    Each node contains an item and the previous and next node in the list.

    head(item, None, next_node) -> next_node(item, head, tail) -> tail(item, prev_node, None)

    Arguments are optional.
    Multiple argumets can be given to create multiple nodes in the list.
    """
    def __init__(self, *items):
        # Only create nodes if the items are not already nodes.
        items = [item if isinstance(item, Node) else Node(item) for item in items]
        # Assign each node's next_node and prev_node attributes.
        # 1 less than the len of items to avoid index out of range error.
        for i in range(len(items)-1):
            items[i].next_node = items[i+1]
            items[i+1].prev_node = items[i]
        # Both a head and tail are assigned. If there is only one item in the list,
        # the head and tail will be the same.
        self.head = items[0] if items else None
        self.tail = items[-1] if items else None

    def __repr__(self):
        return str(self.py_list())

    def __len__(self):
        """Return the number of items in the list.
        """
        link = self.head
        list_length = 0
        while link is not None:
            list_length += 1
            link = link.next_node
        return list_length

    def __getitem__(self, index):
        """
        Return an item from an index:

            linked = DoublyLinkedList('a', 'b', 'c')
            linked[1]                # returns 'b'
        Slices not supported.
        """
        if not isinstance(index, int):
            raise TypeError('list indices must be integers')
        # Negative index support.
        if index < 0:
            index = len(self) + index
        i = 0
        link = self.head
        while link is not None:
            if index == i:
                return link
            link = link.next_node
            i += 1
        if index >= i or index < 0:
            raise IndexError('list index out of range')

    def __setitem__(self, index, new_item):
        """
        Item assignment.

            linked = DoublyLinkedList(1, 5, 3)
            linked[1] = 2                # Changes 5 to 2
        """
        if not isinstance(index, int):
            raise TypeError('list indices must be integers')
        # Negative index support.
        if index < 0:
            index = len(self) + index
        i = 0
        link = self.head
        while link is not None:
            if i == index:
                link = new_item
            link = link.next_node
            i += 1
        if index >= i or index < 0:
            raise IndexError('list index out of range')

    def __add__(self, other_item):
        """Concatenation support.
        """
        # To keep the original linkedlist intact:
        new_linked = DoublyLinkedList()
        for node in self:
            new_linked.append(node.item)

        if isinstance(other_item, DoublyLinkedList):
            if new_linked.head is not None:
                new_linked.tail.next_node = other_item.head
                other_item.head.prev_node = new_linked.tail
                new_linked.tail = other_item.tail
            else:
                new_linked.head = other_item.head
                new_linked.tail = other_item.tail
        # Reasoning for having it work this way: it quickly allows en mass appends.
        elif isinstance(other_item, list):
            for item in other_item:
                new_linked.append(item)
        else:
            new_linked.append(other_item)
        return new_linked

    def __iter__(self):
        """Iteration support.
        """
        link = self.head
        while link is not None:
            yield link
            link = link.next_node

    def append_left(self, item):
        """Append an item to the beginning of the list.
        """
        item = item if isinstance(item, Node) else Node(item)
        # Assign the given item's (new node) next_node to the old head.
        item.next_node = self.head
        # In case a Node is passed which has a prev_node.
        item.prev_node = None
        if self.head is not None:
            # The old head's prev_node becomes the new node
            self.head.prev_node = item
        # If there wasn't a tail, the tail also becomes the new node.
        if self.tail is None:
            self.tail = item
        # Finally, the new node becomes the new head.
        self.head = item

    def append_right(self, item):
        """Append an item to the end of the list.
        """
        item = item if isinstance(item, Node) else Node(item)
        item.prev_node = self.tail
        item.next_node = None
        if self.tail is not None:
            self.tail.next_node = item
        if self.head is None:
            self.head = item
        self.tail = item

    def append(self, item):
        """Append an item to the end of the list.
        """
        self.append_right(item)

    def insert(self, index, item):
        """Insert the given item at the given index.
        """
        if not isinstance(index, int):
            raise TypeError('list indices must be integers')
        item = item if isinstance(item, Node) else Node(item)
        # Negative index support.
        if index < 0:
            index = len(self) + index
        # To simplify inserting into an empty list.
        if index == 0:
            self.append_left(item)
        else:
            inserted = False
            i = 0
            link = self.head
            while link is not None:
                if i == index:
                    item.prev_node = link.prev_node
                    item.next_node = link
                    link.prev_node.next_node = item
                    link.prev_node = item
                    inserted = True
                link = link.next_node
                i += 1
            # Inserting at the end of the list.
            if i == index:
                self.append_right(item)
                inserted = True
            # Assume index out of range if nothing was inserted.
            if not inserted:
                raise IndexError('list index out of range')

    def pop_left(self):
        """Remove the left most item in the list and return it.
        """
        if self.head is None:
            raise IndexError('pop from empty list')
        popped_item = self.head.item
        # i.e. if there is only one item in the list:
        if self.head is self.tail:
            self.head, self.tail = None, None
        else:
            self.head = self.head.next_node
            self.head.prev_node = None
        return popped_item

    def pop_right(self):
        """Remove the right most item in the list and return it.
        """
        if self.head is None:
            raise IndexError('pop from empty list')
        popped_item = self.tail.item
        # i.e. if there is only one item in the list:
        if self.head is self.tail:
            self.head, self.tail = None, None
        else:
            self.tail = self.tail.prev_node
            self.tail.next_node = None
        return popped_item

    def pop(self, index=None):
        """Remove an item at the given index from the list and return it.

        Remove the last item if index is omitted.
        """
        if index is None:
            return self.pop_right()
        else:
            if not isinstance(index, int):
                raise TypeError('list indices must be integers')
            elif self.head is None:
                raise IndexError('pop from empty list')
            # Negative index support.
            if index < 0:
                index = len(self) + index
            link = self.head
            i = 0
            while link is not None:
                if i == index:
                    popped_item = link.item
                    if link.prev_node is None:
                        return self.pop_left()
                    elif link.next_node is None:
                        return self.pop_right()
                    else:
                        # Overwrite the current link from the prev_node's
                        # next_node and the from the next_node's prev_node.
                        link.prev_node.next_node = link.next_node
                        link.next_node.prev_node = link.prev_node
                    return popped_item
                link = link.next_node
                i += 1
            if index >= i or index < 0:
                raise IndexError('list index out of range')

    def contains(self, item):
        """Return True if the given item is within the list. False otherwise.
        """
        link = self.head
        while link is not None:
            if link.item == item:
                return True
            link = link.next_node
        return False

    def py_list(self):
        """Return a python list of all items from head to tail.
        """
        py_list = []
        link = self.head
        while link is not None:
            py_list.append(link.item)
            link = link.next_node
        return py_list

    def print_nodes(self):
        """Print each node's previous and next nodes.
        """
        link = self.head
        while link is not None:
            print(f'{link}: {(link.prev_node, link.next_node)}')
            link = link.next_node


if __name__ == "__main__":
    linked = DoublyLinkedList()
    linked.append(2)
    linked.append_left(1)
    linked.append_right(3)
    print(linked[1])
    print(linked.contains(2))
    linked[1] = 'two'
    print(linked.contains('two'))
    print(linked)
    linked.print_nodes()
    print(f'"{linked.pop(1)}" was popped.')
    print(linked)
    linked.insert(1, 2)
    print(linked)
    linked.print_nodes()
    print(linked.pop_left())
    print(linked.pop_right())
    print(linked)
    new_linked = linked + DoublyLinkedList('eggs', 'spam')
    print(new_linked)
    for x in new_linked:
        print(f'{x}.prev_node is {x.prev_node} and {x}.next_node is {x.next_node}')
    print(linked)
    linked += [3, 4, 5]
    print(linked)
    print(type(linked), linked.head, linked.tail)
    linked.print_nodes()
