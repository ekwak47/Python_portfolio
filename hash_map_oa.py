# Name: Eric Kwak
# OSU Email: kwake@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - Hashmap
# Due Date: 6/9/23
# Description: open addressing implementation of hashmap

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1
        while not self._is_prime(capacity):
            capacity += 2
        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True
        if capacity == 1 or capacity % 2 == 0:
            return False
        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2
        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #
    def put(self, key: str, value: object) -> None:
        """
        Updates the eky/value pair in the hash map.
        """
        if self.table_load() >= 0.5:  # if the load factor is greater than .5, doubles capacity
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # sets the index value

        if self._buckets.get_at_index(index) is None:  # if the bucket has no values
            self._buckets.set_at_index(index, HashEntry(key, value))  # inserts value in empty bucket
            self._size += 1  # increases the size by one

        else:
            j = 1
            quad_key = index  # quadratic probing
            while self._buckets.get_at_index(quad_key):
                if self._buckets.get_at_index(quad_key).key == key:
                    if self._buckets.get_at_index(quad_key).is_tombstone:  # if the key is a tombstone
                        self._buckets.set_at_index(quad_key, HashEntry(key, value))  # replaces value
                        self._size += 1  # increases size
                        self._buckets.get_at_index(quad_key).is_tombstone = False  # no more tombstone
                    else:
                        self._buckets.set_at_index(quad_key, HashEntry(key, value))  # replaces element
                    return
                quad_key = (index + j ** 2) % self._capacity
                j += 1

            self._buckets.set_at_index(quad_key, HashEntry(key, value))
            self._size += 1

    def table_load(self) -> float:
        """
        returns the current hash table load factor
        """
        return self._size / self._capacity  # calculates the load factor

    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table
        """
        if new_capacity < self._size:  # if the new capacity is less than number of elements, returns
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        # uses the prime function to set the capacity to the next prime number

        new_table = HashMap(new_capacity, self._hash_function)
        # initializes a new hashmap

        if new_capacity == 2:  # helps next_prime go in consistent prime values
            new_table._capacity = 2

        for index in range(self._capacity):  # iterates through the array
            item = self._buckets.get_at_index(index)  # sets item
            if item is not None and item.is_tombstone is False:  # check to make sure not a tombstone
                new_table.put(item.key, item.value)

        self._buckets = new_table._buckets  # reassigns the values to the self variables
        self._size = new_table._size
        self._capacity = new_table._capacity

    def get(self, key: str) -> object:
        """
        Returns a value associates with the given key
        """
        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # initializes index value
        i = 0  # iteration counter for probing

        while True:
            element = self._buckets.get_at_index(index)  # sets the value
            if element:
                if element.key == key:  # if the associated key is found
                    if element.is_tombstone:  # the function returns if the value was deleted
                        return None
                    return element.value  # if the value is not a tombstone, returns the object
                else:
                    i = i + 1  # updates counter
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:  # if the key is not found, returns
                return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # initializes index value
        i = 0  # iteration counter for probing

        while True:
            element = self._buckets.get_at_index(index)
            if element:
                if element.key == key and not element.is_tombstone:  # if the given key is found, returns True
                    return True
                else:
                    i = i + 1
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:  # if the key is not in the map, returns False
                return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and value from the hash map
        """

        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # initializes index value
        i = 0  # iteration counter for probing

        while True:
            element = self._buckets.get_at_index(index)
            if element:  # if the value is either found or a tombstone
                if element.key == key:
                    if self._buckets.get_at_index(index).is_tombstone:
                        return  # if the value reaches a tombstone value, returns
                    self._buckets.get_at_index(index).is_tombstone = True
                    # if the value is not a tombstone, sets the value to a tombstone for deletion
                    self._size -= 1  # updates size
                    return
                else:
                    i = i + 1  # updates counter
                    index = (self._hash_function(key) + i * i) % self._capacity
            else:    # if the given index is not found, does nothing
                return

    def clear(self) -> None:
        """
        Clears all the contents of the Hashmap
        """
        self._buckets = DynamicArray()  # initializes the buckets as a dynamicarray
        for _ in range(self._capacity):  # iterates through the whole capacity
            self._buckets.append(None)  # sets all the buckets to None
        self._size = 0  # empty

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a dynamicarray where each index contains a tuple of a key/value pair stored in hashmap
        """
        keys_values = DynamicArray()

        for index in range(self._capacity):  # iterates through the array
            item = self._buckets.get_at_index(index)  # sets item
            if item is not None and item.is_tombstone is False:  # check to make sure not a tombstone
                keys_values.append((item.key, item.value))

        return keys_values

    def __iter__(self):
        """
        Enables the hash map to iterate across itself
        """
        self.index = 0  # initializes a variable to track the iterator
        return self

    def __next__(self):
        """
        Returns the next item in the hash map
        """
        while self.index < self._buckets.length():  # while loop for the index is less than the length
            if self._buckets[self.index] is not None:
                self.index += 1  # updates index
                return self._buckets[self.index - 1]  # returns value
            self.index += 1  # updates iterators counter by one
        else:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
m.get_capacity())
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(),
m.get_capacity())
    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))
    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)
        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to "
                  f"resize_table().\n"
    f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')
        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(),
round(m.table_load(), 2))
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))
    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    m.resize_table(2)
    print(m.get_keys_and_values())
    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)