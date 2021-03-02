# linkedlist.py by nonetypes
# Last revised on 02/17/2021

class Node:
    """Node obect to make up the links within a LinkedList.

    Contains an item and the next node in the chain.
    """
    def __init__(self, item=None):
        self.item = item
        self.next_node = None

    def __repr__(self):
        return str(self.item)


class LinkedList:
    """Linear data structure -- list like object.
    Contains a head node which contains an item and the next node,
    containing the next item and so forth.

    head(item, next_node) -> next_node(item, next_node) -> next_node(item, None)

    Arguments are optional.
    Multiple argumets can be given to create multiple nodes in the list.
    """
    def __init__(self, *items):
        # Only create nodes if the items are not already nodes.
        items = [item if isinstance(item, Node) else Node(item) for item in items]
        # Assign each node's next_node attribute.
        for i in range(len(items)-1):
            items[i].next_node = items[i+1]
        self.head = items[0] if items else None

    def __repr__(self):
        return str(self.py_list())

    def __len__(self):
        """Return the length of the list.
        """
        link = self.head
        list_length = 0
        while link is not None:
            list_length += 1
            link = link.next_node
            # Cricle handling.
            if link == self.head:
                break
        return list_length

    def __getitem__(self, index):
        """
        Return an item from an index:

            linked = LinkedList('a', 'b', 'c')
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
            # Circle handling.
            if link == self.head:
                break
        if index >= i or index < 0:
            raise IndexError('list index out of range')

    def __setitem__(self, index, new_item):
        """
        Item assignment.

            linked = LinkedList(1, 5, 3)
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
                link.item = new_item
            link = link.next_node
            i += 1
            # Circle handling.
            if link == self.head:
                break
        if index >= i or index < 0:
            raise IndexError('list index out of range')

    def __iter__(self):
        link = self.head
        while link is not None:
            yield link
            link = link.next_node
            # Circle handling.
            if link == self.head:
                break

    def append_left(self, item):
        """Append an item to the beginning of the list.
        """
        item = item if isinstance(item, Node) else Node(item)
        # Create a new head. The old head becomes the new head's next_node.
        item.next_node = self.head
        self.head = item

    def append_right(self, item):
        """Append an item to the end of the list.
        """
        item = item if isinstance(item, Node) else Node(item)
        if self.head is None:
            self.head = item
        else:
            # Start with the head.
            # Work through each node until the next_node is None (the tail),
            # and assign the given item (new node) to its next_node.
            link = self.head
            while link.next_node is not None:
                link = link.next_node
            link.next_node = item

    def append(self, item):
        """Append an item to the end of the list.
        """
        # For ease of use. Functions like built-in [].append()
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
        if index == 0:
            self.append_left(item)
        else:
            inserted = False
            # Start at 1 rather than 0 for i because the link preceding the
            # given index is what must be altered.
            i = 1
            link = self.head
            while link is not None:
                if i == index:
                    item.next_node = link.next_node
                    link.next_node = item
                    inserted = True
                link = link.next_node
                i += 1
            # Assume index out of range if nothing was inserted.
            if not inserted:
                raise IndexError('list index out of range')

    def pop_left(self):
        """Remove the left most item in the list and return it.
        """
        if self.head is None:
            raise IndexError('pop from empty list')
        else:
            # Reassign the head to the head's next_node effectively deleting it
            popped_item = self.head.item
            self.head = self.head.next_node
            return popped_item

    def pop_right(self):
        """Remove the right most item in the list and return it.
        """
        if self.head is None:
            raise IndexError('pop from empty list')
        if self.head.next_node is None:
            popped_item = self.head.item
            self.head = None
        else:
            link = self.head
            while link.next_node is not None:
                # Detect if the node after the next is the tail because the
                # preceding node is what must be altered in order to delete it.
                if link.next_node.next_node is None:
                    popped_item = link.next_node.item
                    link.next_node = None
                else:
                    link = link.next_node
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
            if index == 0:
                return self.pop_left()
            else:
                # Start at 1 rather than 0 for i because the link preceding the
                # given index is what must be altered.
                i = 1
                link = self.head
                while link is not None:
                    if i == index:
                        if link.next_node is not None:
                            popped_item = link.next_node.item
                            link.next_node = link.next_node.next_node
                            return popped_item
                    link = link.next_node
                    i += 1
                # Assume index out of range if function got this far.
                raise IndexError('list index out of range')

    def contains(self, item):
        """Return True if the given item is within the list and False otherwise.
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
            # Circle handling.
            if link == self.head:
                break
        return py_list

    def classify(self):
        """Returns one of three strings: 'terminating', 'circle', or 'lollipop'.

        Determines if the list is 'terminating', i.e. it eventually points to None,
        is a 'circle', i.e. it eventually points back to the head node,
        or is a 'lollipop', i.e. it eventually points to an earlier node that is not the head.
        """
        # Hare will traverse list twice as fast as tortoise.
        tort = self.head
        hare = self.head
        while tort is not None and hare is not None:
            hare = hare.next_node
            if hare is self.head:
                return 'circle'
            elif hare is tort:
                return 'lollipop'
            elif hare is not None:
                hare = hare.next_node
            # Check if hare is head or tort at each step for efficiency.
            if hare is self.head:
                return 'circle'
            elif hare is tort:
                return 'lollipop'
            tort = tort.next_node
            if tort is self.head:
                return 'circle'
            elif tort is hare:
                return 'lollipop'
        # Loop is escaped if the tort or hare is None, confirming a terminating list.
        return 'terminating'

    def has_cycle(self):
        """Determine if the list contains a cycle, i.e. if a node points to an earlier
        node in the list, returning True if it does and False otherwise.
        """
        node_list = []
        link = self.head
        while link is not None:
            if link in node_list:
                return True
            else:
                node_list.append(link)
            link = link.next_node
        return False


if __name__ == "__main__":
    linked = LinkedList(1, 2, 3)
    linked.append_left(0)
    linked.append_right(4)
    print(linked.contains(2))
    linked[2] = 'two'
    print(linked.contains(2))
    print(linked)
    print(f'"{linked.pop(-3)}" was popped.')
    print(linked)
    linked.pop_left()
    linked.pop_right()
    print(linked)
    linked.insert(1, 2)
    print(linked)
    # Confirm that list is terminating.
    print(linked.has_cycle(), linked.classify())
    # Circle test.
    linked.append(linked.head)
    print(linked.has_cycle(), linked.classify())
    # Lollipop test.
    linked = LinkedList(1, 2, 3, 4, 5, 6)
    # The sixth (last) node will point to the second node.
    linked[5].next_node = linked[1]
    print(linked[5], linked[5].next_node)
    print(linked.has_cycle(), linked.classify())
