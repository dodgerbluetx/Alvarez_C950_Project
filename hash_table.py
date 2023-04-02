
class HashTable:
    # default constructor
    def __init__(self, initial_capacity: int = 10) -> None:
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def print_table(self) -> None:
        for count, value in enumerate(self.table): 
            print(count, ": ", value)
            # print(count)
            # for i in value:
            #     print(i[0])
            #     print(i[1])

    # insert new item or update if key exists
    def add(self, key: str, value: str) -> bool:
        # find the hashed index value
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through list and update value if key is already there
        for i in index_list:
            #print (key_value)
            if i[0] == key:
                i[1] = value
                return True
        
        # if value was not updated already, add value to the index list
        key_value = [key, value]
        index_list.append(key_value)
        return True 

    # find a value when provided a key to search for
    def find(self, key: str) -> str:
        # find the hashed index value
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through list and return the value if matching key is found
        for i in index_list:
            if i[0] == key:
                return i[1]
        return None
 
    # Removes an item with matching key from the hash table.
    def remove(self, key: str) -> None:
        # find the hashed index value
        index = hash(key) % len(self.table)
        index_list = self.table[index]
 
        # loop through the index list and remove the key/value pair
        for i in index_list:
            if i[0] == key:
                index_list.remove([i[0],i[1]])