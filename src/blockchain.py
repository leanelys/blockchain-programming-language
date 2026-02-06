import block
import json

# ====================================================================================================
# BLOCKCHAIN CLASS
# ====================================================================================================
class BlockChain:
    # BlockChain constructor
    def __init__(self):
        self.chain = []                   # Create the chain for Blocks to go in
        self.difficulty = 4               # Difficulty for mining
        genesis = block.Block("Genesis Block")  # Hardcoding the first/genesis block in the blockchain
        genesis.prev_hash = "0"*64
        genesis.mine(self.difficulty)
        genesis.index = 0
        self.chain.append(genesis)                         

    # Adds a Block to the BlockChain
    def add(self, block: block.Block):
        block.prev_hash = self.chain[-1].get_hash()  # Use the last Block's hash to set this Block's previous hash
        block.index = len(self.chain)                # Set the Block's index now that it's in the BlockChain
        self.chain.append(block)                     # Add it to the end of the chain
    
    # Print each Block in the chain and its info
    def print(self):
        for block in self.chain:
            block.print()

    def export(self):
        blocks = {}                                 # Store all the blocks in a dictionary
        for block in self.chain:                    # Iterate through the chain
            block_name = f"Block{block.index}"      # The key for the dict will be Block{i} e.g. Block0, Block1, etc.
            curr_block = block.get_as_dict()        # Store current Block as a dictionary
            blocks[block_name] = curr_block         # Add to blocks dictionary
        with open("blockchain.json", 'w') as file:  
            json.dump(blocks, file, indent=4)       # Dumps all the dicts into blockchain.json

    # Mine all the Blocks in the BlockChain
    def mine(self):
        for block in self.chain:
            block.mine(self.difficulty)