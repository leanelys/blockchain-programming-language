
# Blockchain Programming Language

A programming language made using [PLY](https://www.dabeaz.com/ply/index.html) with a [Flask](https://flask.palletsprojects.com/en/stable/) frontend for my Programming Language course. It's intended to be used for the creation of blocks in a blockchain. Complete with error checking for semantic, syntactical, and lexical errors.

## Documentation
Create a block in memory: 

``block myBlock = (param1:str, param2:int, param3:str)``

---
Add the created block to the chain: 

``add myBlock = (param1:"Hello", param2: 25, param3:"World")``

---
Mine the block (change its hash):

``mine myBlock``

---
Export the blockchain belonging to the block as a JSON file:

``export myBlock``

---
View the blockchain:

``print myBlock``
