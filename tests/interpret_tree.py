import os
import networkx as nx
from networkx.drawing.nx_pydot import read_dot

current_scope = ""

class VariableTable:
    def __init__(self):
        self.table = {}

    def add_variable(self, name, scope, dimension, type, value):
        if name not in self.table:
            self.table[name] = {}
        self.table[name][scope] = {'type': type, 'dimension': dimension, 'value': value}

    def get_variable(self, name, scope):
        if name in self.table and scope in self.table[name]:
            return self.table[name][scope]
        return None

    def remove_variable(self, name, scope):
        if name in self.table and scope in self.table[name]:
            del self.table[name][scope]

    def get_all_variables(self):
        return self.table
    
    
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
            return self.graph.nodes[node_id]['label']
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


def array_assignment(ast : AST, node_id, variable_table : VariableTable):
    pass    
    
def array_declaration_init(ast : AST, node_id, variable_table : VariableTable):
    global current_scope
    var_name = "name"
    list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    variable_table.add_variable(var_name, current_scope, "int", list)

def declaration(ast : AST, node_id, variable_table : VariableTable):
    pass


def traverse(ast : AST, node_id):
    print(ast.get_node_name(node_id))

    left_node_id = ast.get_left_node_id(node_id)

    if left_node_id != node_id:
        traverse(ast, left_node_id)

    right_node_id = ast.get_right_node_id(node_id)
    if right_node_id != node_id:
        traverse(ast, right_node_id)


def interpret_tree(ast : AST, node_id, variable_table : VariableTable):
    node_name = ast.get_node_name(node_id)
    if node_name == "program":
        pass
    elif node_name == "declatation":
        declaration(ast, node_id, variable_table)

    left_node_id = ast.get_left_node_id(node_id)
    if left_node_id != node_id:
        interpret_tree(ast, left_node_id, variable_table)

    right_node_id = ast.get_right_node_id(node_id)
    if right_node_id != node_id:
        interpret_tree(ast, right_node_id, variable_table)

    return variable_table


def main():
    tree_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),  'bin', 'tree.dot')
    ast = AST(tree_path)
    first_node_id = ast.get_first_node_id()
    traverse(ast, first_node_id)
    variable_table = VariableTable()
    interpret_tree(ast, first_node_id, variable_table)

if __name__ == "__main__":
    main()