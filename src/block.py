import hashlib

class Block:
    # Block constructor
    def __init__(self, data):
       self.data = data                  # Data for Block
       self.prev_hash = None             # Hash of previous Block in the BlockChain
       self.index = None                 # Index of Block in the BlockChain
       self.nonce = 0                    # Nonce for mining starts at 0
       self.hashcode = self.get_hash()   # Calculate the hash based on the data
    
    # Gets the hash of the Block object's data
    def get_hash(self):
        data_to_hash = (str(self.data) + str(self.nonce))                # Put data and nonce into single string
        return hashlib.sha256(data_to_hash.encode('utf-8')).hexdigest()  # Return hash using SHA256

    # Mine the block based on the difficulty given
    def mine(self, difficulty: int):
        target = "0" * difficulty                              # Number of 0's required to mine successfully
        while not self.hashcode[0:int(difficulty)] == target:  # While the first characters in the hash arent the target...
            self.nonce += 1                                    # Up the nonce by 1 so the next hash is different
            self.hashcode = self.get_hash()                    # Recalculate hash with the updated nonce
    
    # Print the Block's information
    def print(self):
        block = self.get_as_dict()
        for k in block:
            print(f"{k} : {block[k]}")
    
    # Return the Block's data as a dictionary
    def get_as_dict(self):
        block = {
            "Index" : self.index,
            "Hash" : self.hashcode,
            "Previous Hash" : self.prev_hash,
            "Nonce" : self.nonce,
            "Data" : self.data
        }
        return block