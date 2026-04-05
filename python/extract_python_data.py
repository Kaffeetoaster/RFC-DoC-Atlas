import ast
from pathlib import Path

def convert_value(value, context):

    if isinstance(value, ast.Constant):
        return value.value
    
    elif isinstance(value, ast.Name):
        
        return context.get(value.id, value.id)
    elif isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.USub):
        # negative number
        return -convert_value(value.operand, context)
    
    elif isinstance(value, ast.List):
        return [convert_value(elt, context) for elt in value.elts]

    elif isinstance(value, ast.Tuple):
        return tuple(convert_value(elt,context) for elt in value.elts)
  
    
    elif isinstance(value, ast.Dict):
        result = {}
        for k, v in zip(value.keys, value.values):
            key = convert_value(k, context) if k is not None else None
            val = convert_value(v, context)
            result[key] = val
        return result
    
    elif isinstance(value, ast.Call):
        if isinstance(value.func, ast.Name ) and value.func.id in ("CivDict", "appenddict"):
            return convert_value(value.args[0], context)
        elif isinstance(value.func, ast.Attribute):
            # e.g., module.appenddict(...)
            print("function is an attribute:", value.func.attr)
            return None
        else:
            return None

    else:
        return None

def convert_tuple_assignment(node, context):
    
    if (
        isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
    ):
        target_names = [elt.id for elt in node.targets[0].elts if isinstance(elt, ast.Name)]

        if node.value.func.id == "tuple":
            # case tuple(Civ(i) for i in range(iNumCivs))
            # for the definition of Civs
            size = len(node.targets[0].elts)
            results = [i for i in range(size)]
            if ast.unparse(node.value) == "tuple((Civ(i) for i in range(iNumCivs)))":

                return dict(zip(target_names, results))
            else:
                return None

        if node.value.func.id == "range":

            if len(node.value.args) == 1:
                if isinstance( node.value.args[0], ast.Constant):
                    size = node.value.args[0].value
                elif isinstance( node.value.args[0], ast.Name):   
                    size = context.get(node.value.args[0].id)

                results = [i for i in range(size)]
                return dict(zip(target_names, results))

            elif len(node.value.args) == 2:
                # the context will be needed here!
                # Some buildings, bonusVarieties and Wonders need extra logic
                # prob pass down the results dict to be able to access all declared variables
                
                return {}


def convert_node(node, context):
    # returns all assigments from node as a dict
    if isinstance(node.targets[0], ast.Name):
        v = convert_value(node.value, context)
        if v == None:
            return {}
        else:
            # context must be updated after every assignment!
            context[node.targets[0].id] = v
            return {node.targets[0].id : v}
     
    elif isinstance(node.targets[0], ast.Tuple):
        d = convert_tuple_assignment(node, context)
        if d == None:
            return {}
        else:
            # context must be updated after every assignment!
            for k,v in d.items():
                context[k] = v
            return d
    else:
        return {}


def extract_variables(file_path, context):
    results = {}

    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
        assignments = [node for node in tree.body if isinstance(node, ast.Assign)]
        for idx, node in enumerate(assignments):
            res_temp = convert_node(node, context)
            if res_temp == {} or res_temp == None:
                targets_str = ", ".join(ast.unparse(t) for t in node.targets)
                value_str = ast.unparse(node.value)
                print(f"Did not extract: {targets_str} = ...")
            else:
                results = results | res_temp
                # print("context:")
                # print(context)
                # print("results:")
                # print(results)
    return results



