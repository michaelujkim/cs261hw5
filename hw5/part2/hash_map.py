# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================
#Name: Michael Kim
#class: CS261-400
#Date: Jun 1 2020

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self._buckets = []
        capacity=self.capacity
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.size=0
        #basically just creates new list with same capacity

    def get_helper(self,key,node):
        """helper function for the get function. accepts the key and the node in the linked list
        returns the value if present, or returns false if reaches end of list and doesnt find key"""
        if node==None:
            #if reaches the end of list, returns false
            return False
        elif node.key==key:
            #if the current node key and the entered key is the same, returns the nodes value
            return node.value
        else:
            #recursively iterates through to the next node in hte linked list
            return self.get_helper(key,node.next)

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        hash= self._hash_function(key)
        #creates hash
        remain=hash%self.capacity
        #finds the modulo remainder for the index in the hash table
        thebucket=self._buckets[remain]
        #names the entered bucket with correct hash modulo output
        return self.get_helper(key,thebucket.head)
    #returns the get helper to search individual linked lists.

    def listmaker(self,node,list):
        '''recursive helper function to take node and add to end of linked list
        or if it reaches end of list, does nothing'''
        if node==None:
            return
        else:
            list.append(node)
            return self.listmaker(node.next,list)

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """

        linklist=[]

        #creates a flexible iterable list to fill with values and store
        for x in self._buckets:
            #iterates through the hash table and adds values to the created list
            if x.head!=None:
                self.listmaker(x.head,linklist)
                #calls the above function to fill list
        self._buckets = []
        #empties the buckets
        self.capacity=capacity
        #sets capacity to new capacity
        for i in range(capacity):
            self._buckets.append(LinkedList())
        #fills the buckets with linked lists
        self.size = 0
        #sets size to zero
        for x in linklist:
            #iterates through the created "store" list and fills the empty hash table again
            value=x.value
            #setting variables for the put() function
            key=x.key
            hash = self._hash_function(key)
            remain = hash % self.capacity
            #re calculating each hash
            if self._buckets[remain].head == None:
                #stolen from the put code
                self._buckets[remain].add_front(key, value)
                self.size += 1

            else:
                #recursively calls the put helper
                self.put_helper(key, value, self._buckets[remain].head, remain=remain)


    def put_helper(self, key, value, node,remain):
        '''helper for put function. intakes the key and value pair, the current node and the hash modulo output'''
        if node==None:
            #if reaches the end of list and the key is not found, add the key value pair to linked list
            self._buckets[remain].add_front(key,value)
            self.size += 1
            #and increases size


        elif node.key==key:
            node.value = value

        #if the key is found, updates the value to new inputted value


        else:
            #recursively calls the put helper with the key value pair and the next value
            return self.put_helper(key,value,node.next,remain=remain)
    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        hash=self._hash_function(key)
        #calculates hash
        remain=hash%self.capacity
        #calculates the hash modulo output
        if self._buckets[remain].head ==None:
            #if that index in the hash table is empty, add the key value pair
            self._buckets[remain].add_front(key,value)
            self.size+=1
            #increases size
        else:
            #or recursively looks as the index in the hash table with the helper function and
            #carries out actions there
            return self.put_helper(key,value,self._buckets[remain].head, remain=remain)


    def remove_helper(self,key,node,remain):
        '''helper function for remove. intakes the key to be deleted, the current node in the linked list
        and the hash modulo output'''
        if node==None:
            #if it reaches the end of the list and doesnt find key, does nothing
            return
        elif node.key==key:
            #if it find the key, removes value using linked list functions

            self._buckets[remain].remove(key)
        else:
            return self.remove_helper(key,node.next,remain)
        #recursively calls the next node
    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        hash = self._hash_function(key)
        #calculates hash
        remain = hash % self.capacity
        #calculates the modulo output
        thebucket = self._buckets[remain]
        #names the bucket in question
        return self.remove_helper(key, thebucket.head,remain=remain)
        #recursively calls the remove hlper to find the key in the linked list in question
    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        count=0
        #counter to see if the key is in the table
        for i in self._buckets:
            #iterates through table and
            if i.contains(key)==None:
                #if the key is not in the linked list does nothing
                count+=0
            else:
                #if it is, increases the count
                count+=1
        if count >0:
            #if the count is non-zero, ther key is in the table and returns true, false otherwise
            return True
        else:
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table

        """
        counter=0
        #counter variable for the number of empty buckets
        for i in self._buckets:
            #iterates through the hash table and increments the counter if an empty bucket is found
            if i.head==None:
                counter+=1
        return counter
    #returns counter variable
    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        links=0
        #the counter variable for the number of links in the hash table
        buckets=0
        for i in self._buckets:
            #iterates through the hashtable and
            if i !=[]:
                #if the bucket is not empty, add the size of the list to the links counter
                links+=i.size
            buckets+=1
            #adds to the bucket counter regardles if empty or not
        return float(links/buckets)
    #returns the appropriate ratio as a float

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out



