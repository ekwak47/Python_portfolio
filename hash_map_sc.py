# Name: Eric Kwak
# OSU Email: kwake@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - Hashmap
# Due Date: 6/9/23
# Description: Separate Chaining implementation of hashmap
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map.
        """

        if self.table_load() >= 1:  # resizes if the load factor is greater than one
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # sets the index value

        if self._buckets.get_at_index(index) is None:  # if the value at index is None, puts the value in
            self._buckets.get_at_index(index).insert(key, value)

        elif self._buckets.get_at_index(index).contains(key):
            # if there is a matching index value, deletes that one and adds the new one
            self._buckets.get_at_index(index).remove(key)  # deletes
            self._size = self._size - 1  # reduces the size
            self._buckets.get_at_index(index).insert(key, value)  # adds new one

        else:  # adds value
            self._buckets.get_at_index(index).insert(key, value)
        self._size = self._size + 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        empty_num = 0  # initial number of buckets
        for index in range(0, self._capacity):  # goes through each index value in the entire map
            if self._buckets.get_at_index(index).length() == 0:
                empty_num = empty_num + 1  # if an empty bucket is found, adds one to the initial
        return empty_num

    def table_load(self) -> float:
        """
        returns the current hash table factor
        """
        return self._size / self._capacity  # calculates the table factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        for index in range(0, self._capacity):
            self._buckets.set_at_index(index, LinkedList())
            self._size = 0  # puts the number of elements to zero

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table
        """

        if new_capacity < 1:  # if the inputted capacity is less than one, returns
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        # uses the prime function to set the capacity to the next prime number

        new_table = HashMap(new_capacity, self._hash_function)
        # initiates a new hashmap for rehashing

        if new_capacity == 2:  # helps next_prime go in consistent prime values
            new_table._capacity = 2

        for i in range(self._capacity):  # rehashes values for the new capacity
            if self._buckets.get_at_index(i).length() > 0:

                for item in self._buckets.get_at_index(i):
                    new_table.put(item.key, item.value)

        self._buckets = new_table._buckets  # reassigns the updated values to the original variables
        self._size = new_table._size
        self._capacity = new_table._capacity

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets.get_at_index(index).length() is None:
            # returns None if the value is not found
            return None
        else:
            for item in self._buckets.get_at_index(index):  # iterates through the bucket
                if item.key == key:  # if the value is found, returns the value and true
                    return item.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        hash = self._hash_function(key)  # takes a key through the hash function
        index = hash % self._capacity  # sets the index value
        if self._buckets.get_at_index(index).contains(key):  # uses contain and returns True if found
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash mpa.
        """
        if self.contains_key(key) is False:  # if the keyed value is not in the hash, return
            return

        hash_index = self._hash_function(key) % self._capacity  # takes a key through a hash function for the index
        hash = self._buckets[hash_index]
        node = hash.contains(key)  # use the contains method written earlier to find and remove
        if node is not None:  # uses LinkedList remove method to remove the value
            hash.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamicarray of where each index contains a tuple of a key/value pair stored in the hash map
        """
        da = DynamicArray()  # initializes a new dynamicarray
        for i in range(self._capacity):  # iterates through the array
            if self._buckets.get_at_index(i).length() > 0:
                for node in self._buckets.get_at_index(i):
                    da.append((node.key, node.value))  # adds the key and the value to the array
        return da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a DynamicArray and returns a tuple containing mode, value, and occurrences
    """

    map = HashMap()  # initializes a HashMap for chaining
    for index in range(da.length()):  # iterates through the length of the dynamicarray
        if map.contains_key(da.get_at_index(index)) is False:  # if key is not found
            map.put(da.get_at_index(index), 1)
        else:
            map.put(da.get_at_index(index), map.get(da.get_at_index(index)) + 1)

    max_freq = 0  # sets the frequency count to zero
    arr = map.get_keys_and_values()
    mode = DynamicArray()  # initiates a new array for the mode

    for index in range(arr.length()):  # iterates through the array
        if max_freq < arr.get_at_index(index)[1]:  # if a higher frequency value is found, replaces the values
            max_freq = arr.get_at_index(index)[1]  # reassigns the highest frequency

    for index in range(arr.length()):  # iterates through the array
        if arr.get_at_index(index)[1] == max_freq:
            mode.append(arr.get_at_index(index)[0])

    return mode, max_freq


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
    m = HashMap(53, hash_function_1)
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
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu",
"Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )
    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")