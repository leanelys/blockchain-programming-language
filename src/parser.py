import globals
import block as b
import ply.yacc as yacc
from lexer import tokens

# ====================================================================================================
def p_Start(p):
    'Start : statements'
    pass

# ====================================================================================================
def p_statements(p):
    '''statements : statement
                  | statements statement'''
    pass

# ====================================================================================================
def p_statement(p):
    '''statement : block_definition
                 | block_operation'''
    pass

# ====================================================================================================
def p_block_definition(p):
    'block_definition : BLOCK ID ASSIGN LPAREN attributes RPAREN'
    block_name = p[2]
    attributes = []                             # List of tuples (name, type)
    for name, typ in p[5]:                      # "typ" sounds dumb but "type" is a reserved keyword lol
        attributes.append((name, typ.upper()))  # Type is made uppercase to make checks easier later
    globals.block_definitions[block_name] = attributes  # Add attributes of the block to global block_definitons
    print(f"Created block \"{block_name}\" with {globals.block_definitions[block_name]}")

# ====================================================================================================
def p_block_operation(p):
    '''block_operation : ADD ID ASSIGN LPAREN new_atts RPAREN
                       | PRINT ID
                       | MINE ID
                       | EXPORT ID
                       | VIEW ID'''
    # add : Verifies Block's data types and adds Block to the BlockChain
    if p[1] == "add":
        block_name = p[2]
        provided = p[5]  # [(param_name, value), ...]

        # Avoid using "add" on Block that doesn't exist
        if block_name not in globals.block_definitions:
            print(f"[Semantic Error] Undefined block '{block_name}'")
            return  # Early exit

        # Dictionary pairing the variables with their expected variable types
        expected_fields = {}
        for name, typ in globals.block_definitions[block_name]:
            expected_fields[name] = typ

        # Stores all the provided variable names
        provided_names = []
        for k, _ in provided:
            provided_names.append(k)

        # Stores any potential missing variables
        missing = []
        for n in expected_fields.keys():
            if n not in provided_names:
                missing.append(n)

        # If there's something in "missing", exit early
        if len(missing) > 0:
            print(f"[Semantic Error] Missing required fields for '{block_name}': {missing}")
            return

        data_dict = {}
        for field, value in provided:
            if field not in expected_fields:
                print(f"[Semantic Error] Unknown attribute '{field}' for block '{block_name}'")
                data_dict[field] = value
                continue

            expected_type = expected_fields[field]  # e.g. 'STR' or 'INT'

            # Validate according to expected_type
            if expected_type == "STR":
                if not isinstance(value, str):
                    print(f"[Semantic Error] '{field}' should be a string, got {type(value).__name__}")
                    return
            elif expected_type == "INT":
                if not isinstance(value, int):
                    print(f"[Semantic Error] '{field}' should be an integer, got {type(value).__name__}")
                    return
            elif expected_type == "FLOAT":
                if not isinstance(value, (int, float)):
                    print(f"[Semantic Error] '{field}' should be a number, got {type(value).__name__}")
                    return
            elif expected_type == "LONG":
                if not isinstance(value, int):
                    print(f"[Semantic Error] '{field}' should be a long/integer, got {type(value).__name__}")
                    return
            elif expected_type in ("LIST", "TUPLE", "DICT"):
                expected_py = {"LIST": list, "TUPLE": tuple, "DICT": dict}[expected_type]
                if not isinstance(value, expected_py):
                    print(f"[Semantic Error] '{field}' should be {expected_py.__name__}, got {type(value).__name__}")
                    return
            else:
                # Unknown type
                print(f"[Semantic Error] Unknown expected type '{expected_type}' for field '{field}'")
                return

            data_dict[field] = value

        new_block = b.Block(data_dict)
        globals.blockchain.add(new_block)
        print(f"{block_name} added to blockchain")

    # print : BlockChain is printed to the screen (in dictionary form for readability)
    elif p[1] == "print":
        globals.blockchain.print()

    # mine : Every Block in the BlockChain gets mined
    elif p[1] == "mine":
        block_name = p[2]

        # Avoid using "mine" on Block that doesn't exist
        if block_name not in globals.block_definitions:
            print(f"[Semantic Error] Undefined block '{block_name}'")
            return  # Early exit
        
        globals.blockchain.mine()
        print("Mined blockchain!")

    # export : Exports BlockChain to blockchain.json
    elif p[1] == "export":
        globals.blockchain.export()


# ====================================================================================================
def p_type(p):
    '''type : STR
            | INT
            | LONG
            | FLOAT
            | LIST
            | TUPLE
            | DICT'''
    p[0] = p[1]

# ====================================================================================================
def p_attribute(p):
   'attribute : ID TYPEASSIGN type'
   p[0] = (p[1], p[3])

# ====================================================================================================
def p_attributes(p):
    '''attributes : attribute
                  | attributes SEPARATOR attribute'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[3]]

# ====================================================================================================
def p_new_att(p):
    '''new_att : ID TYPEASSIGN STR
               | ID TYPEASSIGN NUM
               | ID TYPEASSIGN FLOATVAL
               | ID TYPEASSIGN LPAREN new_atts RPAREN
               | ID TYPEASSIGN LBRACKET elements RBRACKET
               | ID TYPEASSIGN LBRACE pairs RBRACE'''
    var_name = p[1]

    # Primitive values (string, number, float)
    if len(p) == 4:
        value = p[3]
    
    # Tuple
    elif p[3] == '(':
        inner = p[4]
        value = {k: v for (k, v) in inner}
    
    # List
    elif p[3] == '[':
        value = p[4]
    
    # Dict
    elif p[3] == '{':
        value = dict(p[4])

    p[0] = (var_name, value)

# ====================================================================================================
def p_new_atts(p):
    '''new_atts : new_att
                | new_atts SEPARATOR new_att'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
       p[0] = p[1] + [p[3]]

# ====================================================================================================
def p_elements(p):
    '''elements : element
                | elements SEPARATOR element'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

# ====================================================================================================
def p_element(p):
    '''element : STR
               | NUM
               | FLOATVAL'''
    p[0] = p[1]

# ====================================================================================================
def p_pairs(p):
    '''pairs : pair
              | pairs SEPARATOR pair'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

# ====================================================================================================
def p_pair(p):
    '''pair : STR TYPEASSIGN element'''
    p[0] = (p[1], p[3])

# ====================================================================================================
def p_error(p):
    if p:
        print(f"[Syntax Error] Line {p.lineno}: Unexpected token '{p.value}'")
    else:
        print("[Syntax Error] Unexpected end of file")

my_parser = yacc.yacc()