import os
import networkx as nx
from networkx.drawing.nx_pydot import read_dot

current_scope = []

class VariableTable:
    def __init__(self):
        self.table = {}

    def add_variable(self, name, scope, dimension, type, value):
        exists_already = self.get_variable(name)
        if exists_already:
            raise Exception("Variable {name} exists already")
        if name not in self.table:
            self.table[name] = {'scope': scope, 'type': type, 'dimension': dimension, 'value': value}

    def get_variable(self, name):
        if name in self.table:
            return self.table[name]
        return None

    def remove_variable(self, name):
        if name in self.table in self.table[name]:
            del self.table[name]

    def change_variable_value(self, name, value):
        variable_type = self.table[name]['type']
        try:
            if variable_type == "int":
                value = int(value)
            elif variable_type == "float":
                value = float(value)
            elif variable_type == "char":
                value = str(value)
        except:
            raise ValueError(f"Cannot save {value} to variable {name} due to incompatible types")
        if name in self.table:
            self.table[name]['value'] = value
        else:
            raise KeyError(f"Couldn't save value {value} to variable '{name}'.\n Variable '{name}' has not been declared yet.")

    def get_all_variables(self):
        return self.table
    
    def print_table(self):
        print("Variable Table:")
        print("Name\t\tScope\t\tType\t\tDimension\tValue")
        for key, value in self.table.items():
            print(f"{key}\t\t{value['scope']}\t\t{value['type']}\t\t{value['dimension']}\t\t{value['value']}")
        print("\n")
    
class AST:
    def __init__(self, dot_file_path):
        self.graph = read_dot(dot_file_path)
        self.nodes = list(self.graph.nodes())
        self.edges = [(u, v, self.graph.get_edge_data(u, v)) for u, v in self.graph.edges()]


    def get_first_node_id(self):
        if self.nodes:
            return self.nodes[0]
        return None
    
    def get_node_name(self, node_id):
        if node_id in self.nodes:
            return self.graph.nodes[node_id]["label"].replace('"', '')
        return None

    def get_left_node_id(self, node_id):
        if node_id in self.nodes:
            for edge in self.edges:
                if edge[0] == node_id and edge[2][0]["label"] == '"left"':
                    return edge[1]
        return None

    def get_right_node_id(self, node_id):
        if node_id in self.nodes:
            for edge in self.edges:
                if edge[0] == node_id and edge[2][0]["label"] == '"right"':
                    return edge[1]
        return None
    
    def traverse(self, node_id):
        if node_id in self.nodes:
            print(self.get_node_name(node_id))
            left_node_id = self.get_left_node_id(node_id)
            right_node_id = self.get_right_node_id(node_id)
            if left_node_id:
                self.traverse(left_node_id)
            if right_node_id:
                self.traverse(right_node_id)
        return



def expression(ast : AST, node_id, variable_table : VariableTable):
    return 10 #ToDo !

def condition(ast : AST, node_id, variable_table : VariableTable):
    return True #ToDo !

def assign_array_element_to(ast : AST, node_id, variable_table : VariableTable):
    return 10  #ToDo !

def assign_to_array_element(ast : AST, node_id, variable_table : VariableTable):
    return 10 #ToDo !

def list_from_syntax_tree(ast : AST, node_id):
    return [1,2,3] #ToDo !

def for_loop(ast : AST, node_id, variable_table : VariableTable):
    pass #ToDo !

def while_loop(ast : AST, node_id, variable_table : VariableTable):
    pass #ToDo !

def if_statement(ast : AST, node_id, variable_table : VariableTable):
    pass #ToDo !

def if_else_statement(ast : AST, node_id, variable_table : VariableTable):
    pass #ToDo !

def init(ast : AST, var_name, node_id, variable_table : VariableTable):
    var_type = variable_table.get_variable(var_name)['type']
    var_dim = variable_table.get_variable(var_name)['dimension']

    right_node_id = ast.get_right_node_id(node_id)
    right_node_name = ast.get_node_name(right_node_id)

    value = None
    if right_node_name == "list":
        value = list_from_syntax_tree(ast, right_node_id)
        return #ToDo ! currecntly cannot add list as value to variable tale with the change_variable_value method.
    elif right_node_name == "value":
        value_id = ast.get_left_node_id(right_node_id)
        value = ast.get_node_name(value_id)
    elif right_node_name == "identifier":
        identifier_id = ast.get_left_node_id(right_node_id)
        name = ast.get_node_name(identifier_id)
        value = variable_table.get_variable(name)['value']
    elif right_node_name == "expression":
        value = expression(ast, right_node_id, variable_table)  
    elif right_node_name == "condition":
        value = condition(ast, right_node_id, variable_table)
    elif right_node_name == "type_cast":
        value = type_cast(ast, right_node_id, variable_table)
    elif right_node_name == "assign_array_element_to":
        value = assign_array_element_to(ast, right_node_id, variable_table)
    elif right_node_name == "assign_to_array_element":
        value = assign_to_array_element(ast, right_node_id, variable_table)
        
    
    variable_table.change_variable_value(var_name, value)
    

def type_cast(ast : AST, node_id, variable_table : VariableTable):
        new_type = ast.get_node_name(ast.get_left_node_id(node_id))
        variable_name = ast.get_node_name(ast.get_right_node_id(node_id))
        variable_value = variable_table.get_variable(variable_name)['value']
        casted_value = None
        try:
            if new_type == "int":
                casted_value = int(variable_value)
            elif new_type == "float":
                casted_value = float(variable_value)
            elif new_type == "char":
                casted_value = str(variable_value)
        except ValueError as e:
            print(f"Error casting {variable_value} to {new_type}")

        return casted_value

def declaration(ast : AST, node_id, variable_table : VariableTable):
    global current_scope
    var_id = ast.get_left_node_id(node_id)
    var_name = ast.get_node_name(var_id)
    var_type = None
    var_dim = None

    type_child = ast.get_left_node_id(var_id)
    if type_child:
        type_child_name = ast.get_node_name(type_child)
        if type_child_name == "type": #should always be true
            actual_type = ast.get_node_name(ast.get_left_node_id(type_child))
            var_type = actual_type
    else:
        raise Exception("No Type at declaration of variable {var_name} in given syntax tree")

    dimension_child = ast.get_right_node_id(var_id)
    if dimension_child:
        dimension_child_name = ast.get_node_name(dimension_child)
        if dimension_child_name == "array_dim": #should always be true
            var_dim = ast.get_node_name(ast.get_left_node_id(dimension_child))
            var_dim = tuple(int(x.strip()) for x in var_dim.split(','))
    else:
        var_dim = (1)
        
    variable_table.add_variable(var_name, current_scope[-1], var_dim, var_type, None)
    return var_name


def printf(ast : AST, node_id, variable_table : VariableTable):
    left_node_id = ast.get_left_node_id(node_id)
    left_node_name = ast.get_node_name(left_node_id)
    left_node_name = left_node_name.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
    print(left_node_name[1:-1]) # Remove quotes ('') from string

def scanf(ast : AST, node_id, variable_table : VariableTable):
    value = input("")
    var_name = ast.get_node_name(ast.get_right_node_id(node_id))
    input_type = ast.get_node_name(ast.get_left_node_id(node_id))
    input_type = input_type[1:-1] # Remove quotes ('') from string
    try:
        if input_type == "%s":
            value = str(value)
        elif input_type == "%d":
            value = int(value)
        elif input_type == "%f":
            value = float(value)
    except ValueError as e:
        raise ValueError(f"Cannot cast {value} to the specified type: {input_type}") from e
    variable_table.change_variable_value(var_name, value)

def interpret_tree(ast : AST, node_id, variable_table : VariableTable):
    global current_scope
    added_scope = False

    left_node_id = ast.get_left_node_id(node_id)
    right_node_id = ast.get_right_node_id(node_id)

    node_name = ast.get_node_name(node_id)

    if node_name == "if" or node_name == "if_else" or node_name == "for" or node_name == "while" or node_name == "program":
        current_scope += [node_id]
        added_scope = True
    
    if node_name == "program":
        pass

    elif node_name == "body":
        pass

    elif node_name == "printf":
        printf(ast, node_id, variable_table)
        return
        
    elif node_name == "scanf":
        scanf(ast, node_id, variable_table)
        return

    elif node_name == "declaration":
        declaration(ast, node_id, variable_table)
        return

    elif node_name == "declaration_init":
        var_name = declaration(ast, node_id, variable_table)
        init(ast, var_name, node_id, variable_table)
        return

    elif node_name == "if":	
        if_statement(ast, node_id, variable_table)

    elif node_name == "if_else":
        if_else_statement(ast, node_id, variable_table)

    elif node_name == "for":
        for_loop(ast, node_id, variable_table)

    elif node_name == "while":
        while_loop(ast, node_id, variable_table)

    if (node_id != left_node_id) and left_node_id:    
        interpret_tree(ast, left_node_id, variable_table)
    if (node_id != right_node_id) and right_node_id:
        interpret_tree(ast, right_node_id, variable_table)

    if added_scope:
        current_scope.pop()
    if node_name == "program":
        variable_table.print_table()
    
    return


def main():
    tree_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),  'bin', 'tree.dot')
    ast = AST(tree_path)
    first_node_id = ast.get_first_node_id()
    #traverse(ast, first_node_id)
    variable_table = VariableTable()
    interpret_tree(ast, first_node_id, variable_table)

if __name__ == "__main__":
    main()