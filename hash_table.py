from typing import Any


class HashTable:
    """Class for defining a HashTable data structure object.

    This class is used to define a hash table data structure that will be used to store package data.

    Attributes:
        table: The list of empty lists that is used for storing package data.
    """

    def __init__(self, initial_capacity: int = 10) -> None:
        """Initializes a HashTable instance

        The time complexity of creating the empty hash table is O(n), where n is the depth or size of the table.
        The space complexity of the empty table is O(n) where n is also the depth or size of the table.

        Args:
            initial_capacity: An integer value to define the depth of the hash table, 10 by default.

        Returns:
            None
        """
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def print_table(self) -> None:
        """Prints the hash table data.

        When called, iterate through the hash table data and print the key/value pair.

        The time complexity of printing the hash table is O(n), where n is the depth or size of the table.
        The space complexity of printing the hash table is O(1).

        Args:
            None

        Returns:
            None
        """

        for count, value in enumerate(self.table): 
            print(count, ": ", value)

    def add(self, key: str, value: Any) -> bool:
        """Add new data to the hash table

        A hash value is created to determine the index to store the data. Once the location is found, determine
            if there is already a value there matching the hashed key, if so, then update the value. If not, then
            add the data to the index list.

        Time complexity for adding a value to the has table is O(1) if the index is empty, and O(n) if
            there are values present as we are checking first to see if the key exists and should be updated.
        Space complexity for updating or adding a value is O(1), as we are always only modifying or adding
            a single value.

        Args:
            key: The string to be hashed to determine the table index.
            value: The data to store in the calculated hash table index.

        Returns:
            boolean True that represents that the add was successful.
        """

        # hash the provided key to determine the table index location
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through list and update value if key already exists, return after update
        for i in index_list:
            if i[0] == key:
                i[1] = value
                return True
        
        # if no existing data was updated, add the key/value pair to the list
        key_value = [key, value]
        index_list.append(key_value)
        return True 

    def find(self, key: str) -> str:
        """Search for data in the hash table.

        A hash value is created to determine the index to search the data. Iterate through the hash table index
        to determine if a matching key exists. If a matching key is found, return the value. If not, then
        return None.

        Time complexity for finding a value to the has table is O(1) if the index is empty, and O(n) if
            there are values present as we are checking first to see if the key exists and should be updated.
        Space complexity for finding a value is O(1), as we always only return a single value.

        Args:
            key: The string to be hashed to search the table index for.

        Returns:
            The data value if found, None if no match is found.
        """

        # hash the provided key to determine the table index location
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through list and return the value if matching key is found
        for i in index_list:
            if i[0] == key:
                return i[1]
        return None

    def remove(self, key: str) -> None:
        """Remove data from the hash table.

        A hash value is created to determine the index to search the data. Iterate through the hash table index
            to determine if a matching key exists. If a matching key is found, remove it from the table index list.

        Time complexity for removing a value is O(1) when there is just one value in the index, but O(n) if there
            are multiple values that need to be checked.
        Space complexity for removing a value is O(1), as we always only remove a single value.

        Args:
            key: The string to be hashed to remove from the table index.

        Returns:
            None
        """

        # hash the provided key to determine the table index location
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through the index list and remove the key/value pair
        for i in index_list:
            if i[0] == key:
                index_list.remove([i[0],i[1]])