import os
import shutil
import argparse
import re
import warnings
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import to_pydot
from networkx.drawing.nx_pydot import write_dot  
from networkx.drawing.nx_pydot import read_dot
from generate_video_from_dots import generate_video_from_dots
from PIL import Image, ImageDraw, ImageFont


import os

# Construct the path to the Graphviz bin directory
graphviz_bin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin', 'Graphviz-11.0.0-win64', 'bin')
# Add the Graphviz bin directory to the PATH environment variable for the current process
os.environ["PATH"] += os.pathsep + graphviz_bin_path
# Now you can attempt to use 'dot' as if it was in the system's PATH


current_scope = []
main_dir = ""
include_dir = ""
frame_counter = 0

class VariableTable:
    def __init__(self):
        self.table = {}

    def add_variable(self, name, scope, dimension, type):
        exists_already = self.get_variable(name)
        if exists_already:
            raise Exception(f"Variable {name} exists already")
        self.table[name] = {'scope': scope, 'type': type, 'dimension': dimension, 'value': None}

    def get_variable(self, name):
        if name in self.table:
            return self.table[name]
        return None

    def remove_variable(self, name):
        if name in self.table:
            del self.table[name]
        else:
            self.print_table()
            raise KeyError(f"Couldn't remove variable '{name}'.\n Variable '{name}' does not exist in the table.")

    def change_variable_value(self, name, value):
        variable_type = self.table[name]['type']
        if isinstance(value, list):
            list_type = check_uniform_list_type(value)
            if variable_type != list_type:
                raise ValueError(f"found list of types {list_type} but expected type {variable_type}")
            list_dimensions = get_list_dimensions(value)
            variable_dimensions = self.table[name]['dimension']
            if list_dimensions != variable_dimensions:
                if variable_dimensions == [1]: 
                    raise ValueError(f"found list of dimensions {list_dimensions} but {name} is not an array")
                else:
                    raise ValueError(f"found list of dimensions {list_dimensions} but expected dimensions {variable_dimensions}")
        else:
            try:
                convert_to_value(value, variable_type)
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

    def save_table_as_dot(self, file_name):
        with open(file_name, 'w') as f:
            f.write("digraph G {\n")
            f.write("node [shape=plaintext]\n")
            f.write("rankdir=LR\n")
            f.write("Variables [label=<\n")
            f.write("<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">")
            f.write("<tr><td>Variable Name</td><td>Scope</td><td>Type</td><td>Dimension</td><td>Value</td></tr>")
            for key, value in self.table.items():
                f.write(f"<tr><td>{str(key)}</td><td>{str(value['scope'])}</td><td>{str(value['type'])}</td><td>{str(value['dimension'])}</td><td>{str(value['value'])}</td></tr>")
            f.write("</table>>];\n}")

# Create a global variable table       
variable_table = VariableTable()

class AST:
    def __init__(self, dot_file_path, generate_parse_frames=False):
        self.generate_parse_frames = generate_parse_frames
        global variable_table
        try:
            self.graph = read_dot(dot_file_path)
        except Exception as e:
            raise Exception(f"Failed to read the dot file at {dot_file_path} due to the following error: {e}")

        if self.graph:
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
    
    last_node_geted = None
    last_edge_geted = None

    def get_left_node_id(self, node_id):
        if node_id in self.nodes:
            for edge in self.edges:
                if edge[0] == node_id and edge[2][0]["label"] == '"left"':
                    left_node_id = edge[1]
                    if self.generate_parse_frames:
                        self.color_node(left_node_id, "green")
                        self.color_edge(node_id, left_node_id, "green")
                        self.color_last_geted()
                        self.last_node_geted = (left_node_id, "left")
                        self.last_edge_geted = (node_id, left_node_id)
                        self.save_dot_frame()
                    return left_node_id
        return None

    def get_right_node_id(self, node_id):
        if node_id in self.nodes:
            for edge in self.edges:
                if edge[0] == node_id and edge[2][0]["label"] == '"right"':
                    right_node_id = edge[1]
                    if self.generate_parse_frames:
                        self.color_node(right_node_id, "green")
                        self.color_edge(node_id, right_node_id, "green")
                        self.color_last_geted()
                        self.last_node_geted = (right_node_id, "right")
                        self.last_edge_geted = (node_id, right_node_id)
                        self.save_dot_frame()
                    return right_node_id
        return None
    
    def color_last_geted(self):
        if self.last_node_geted:
            node_id, direction = self.last_node_geted
            if direction == "left":
                color = "blue"
            elif direction == "right":
                color = "red"
            node_id1, node_id2 = self.last_edge_geted
            self.color_node(node_id, color)
            self.color_edge(node_id1, node_id2, color)

    frame_counter = 0

    def save_dot_frame(self):
        self.frame_counter += 1
        # Construct the directory path
        dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin', 'interpretation_frames')
        # Ensure the directory exists
        os.makedirs(dir_path, exist_ok=True)
        # Now construct the file path
        file_path = os.path.join(dir_path, f'frame_{self.frame_counter}.dot')
        # Save the current frame as dor
        self.save_to_dot(file_path)
        print(f"Saved tree for frame {self.frame_counter} as DOT")
        variable_table.save_table_as_dot(os.path.join(dir_path, f'variableTable_{self.frame_counter}.dot'))
        print(f"Saved variable table for frame {self.frame_counter} as DOT")
       
    def close(self):
        self.executor.shutdown(wait=True)
    
    def color_node(self, node_id, color):
        if node_id in self.nodes:
            self.graph.nodes[node_id]['color'] = color
        else:
            print(f"Node {node_id} does not exist in the graph.")

    def color_edge(self, node_id1, node_id2, color):
        if node_id1 in self.nodes and node_id2 in self.nodes:
            self.graph.edges[node_id1, node_id2, 0]['color'] = color
        else:
            print(f"Edge between nodes {node_id1} and {node_id2} does not exist in the graph.")
    
    def add_second_label_to_node(self, node_id, second_label):
        if node_id in self.nodes:
            # Assign the second label to a new attribute in the node's data
            self.graph.nodes[node_id]["second_label"] = second_label
        else:
            # Handle the case where the node_id does not exist in the graph
            print(f"Node {node_id} does not exist in the graph.")
    
    
    def prepare_polydot_graph(self):
        # Convert the NetworkX graph to a PyDot graph
        pydot_graph = to_pydot(self.graph)
        
        # Iterate over PyDot nodes to modify the label
        for node in pydot_graph.get_nodes():
            node_id = node.get_name().strip('"')
            # Check if the node exists in the original NetworkX graph
            if node_id in self.graph:
                # Access the original node data
                original_node_data = self.graph.nodes[node_id]
                # Check if a second label exists and modify the PyDot node label accordingly
                if 'second_label' in original_node_data:
                    new_label = f"{original_node_data['second_label']}\n\n{original_node_data.get('label', '')}"
                    node.set_label(new_label)
        return pydot_graph

    def save_to_png(self, file_path, keep_dot = False):
        try:
            pydot_graph = self.prepare_polydot_graph()
            # Set the 'dpi' attribute of the graph
            pydot_graph.set_graph_defaults(dpi="55")  # Default is usually 96
            # Now write the PNG file with the modified DPI (resolution)
            pydot_graph.write_png(file_path)
            if keep_dot:
                dot_file_path = file_path.replace(".png", ".dot")
                pydot_graph.write(dot_file_path)
        except Exception as e:
            raise Exception(f"Failed to save the graph as PNG at {file_path} due to the following error: {e}")
    
    def save_to_dot(self, file_path):
        try:
            pydot_graph = self.prepare_polydot_graph()
            # Write the graph to a DOT file
            pydot_graph.write(file_path)
        except Exception as e:
            raise Exception(f"Failed to save the graph as DOT at {file_path} due to the following error: {e}")
        
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


def get_type_from_string(s):
    s = str(s)
    if s.isdigit():
        return 'int'
    else:
        try:
            return 'float'
        except ValueError:
            return 'char'
        
        
def convert_string_to_value(var):
    type = get_type_from_string(var)

    return convert_to_value(var, type)

def convert_to_value(value, type):
    if type == "int":
        return int(value)
    elif type == "float":
        return float(value)
    elif type == "char":
        return str(value)


def expression(ast : AST, node_id, variable_table : VariableTable):

    node_name = ast.get_node_name(node_id)

    if(node_name == "expression"):
        node_id = ast.get_left_node_id(node_id)
        node_name = ast.get_node_name(node_id)

    value = None

    if(node_name == "value"):

        value = convert_string_to_value(ast.get_node_name(ast.get_left_node_id(node_id)))
    elif(node_name == "unary"):
        var_name = ast.get_node_name(ast.get_left_node_id(node_id))
        if(ast.get_node_name(ast.get_right_node_id(node_id)) == "++"):
            value = variable_table.get_variable(var_name)['value'] + 1
        elif(ast.get_node_name(ast.get_right_node_id(node_id)) == "--"):
            value = variable_table.get_variable(var_name)['value'] - 1
        variable_table.change_variable_value(var_name, value)
    elif(node_name == "identifier"):
        identifier_id = ast.get_left_node_id(node_id)
        name = ast.get_node_name(identifier_id)
        value = variable_table.get_variable(name)['value']
    else:
        left_node_id = ast.get_left_node_id(node_id)
        right_node_id = ast.get_right_node_id(node_id)
        left_value = expression(ast, left_node_id, variable_table)
        right_value = expression(ast, right_node_id, variable_table)
        operator = node_name

        if operator == "+":
            value = left_value + right_value
        elif operator == "-":
            value = left_value - right_value
        elif operator == "*":
            value = left_value * right_value
        elif operator == "/":
            value = left_value / right_value

    ast.add_second_label_to_node(node_id, str(value))	

    return value

def value_to_bool(value):
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        if(value == 0):
            return False
        else:
            return True

def condition(ast : AST, node_id, variable_table : VariableTable):

    node_name = ast.get_node_name(node_id)

    if(node_name == "condition"):
        node_id = ast.get_left_node_id(node_id)
        node_name = ast.get_node_name(node_id)

    if(node_name == "true"):
        value = True
    elif(node_name == "false"):
        value = False
    elif(node_name == "value"):
        value = ast.get_node_name(ast.get_left_node_id(node_id))
    elif(node_name == "identifier"):
        value = variable_table.get_variable(ast.get_node_name(ast.get_left_node_id(node_id)))['value']
    elif(node_name == "expression"):
        value = expression(ast, node_id, variable_table)
    else:
        left_node_id = ast.get_left_node_id(node_id)
        right_node_id = ast.get_right_node_id(node_id)
        
        left_value = condition(ast, left_node_id, variable_table)
        right_value = condition(ast, right_node_id, variable_table)

        operator = ast.get_node_name(node_id)

        if operator == "==":
            value = left_value == right_value
        elif operator == "!=":
            value = left_value != right_value
        elif operator == "<":
            value = left_value < right_value
        elif operator == ">":
            value = left_value > right_value
        elif operator == "<=":
            value = left_value <= right_value
        elif operator == ">=":
            value = left_value >= right_value
        elif operator == "&&":
            value = left_value and right_value
        elif operator == "||":
            value = left_value or right_value
    
    ast.add_second_label_to_node(node_id, str(value))  
    return value


def assign_array_element_to(ast : AST, node_id, variable_table : VariableTable):
    left_node_id = ast.get_left_node_id(node_id)
    right_node_id = ast.get_right_node_id(node_id)
    array_name = ast.get_node_name(left_node_id)
    
    array = variable_table.get_variable(array_name)['value']
    array_dim = variable_table.get_variable(array_name)['dimension']

    index = ast.get_node_name(ast.get_left_node_id(right_node_id))
    index = [int(x.strip()) for x in index.split(',')]

    value = handle_statement(ast, ast.get_right_node_id(right_node_id), variable_table)

    if str(get_type_from_string(value)) != str(variable_table.get_variable(array_name)['type']):
        raise Exception("Type mismatch")

    for dim in index:
        if not dim <= array_dim[index.index(dim)]: 
            raise Exception("Index out of range")
    array = assign_array_element_to_value(index, value, array)

def assign_array_element_to_value(index, value, array):
    if len(index) == 1:
        array[index[0]] = value
    else:
        assign_array_element_to_value(index[1:], value, array[index[0]])
    return array

def assign_value_to_array_element(index, array):
    if len(index) == 1:
        return array[index[0]]
    else:
        return assign_value_to_array_element(index[1:], array[index[0]])

def assignment(ast : AST, node_id, variable_table : VariableTable):
    var_name = ast.get_node_name(ast.get_left_node_id(node_id))
    
    init(ast, var_name, node_id, variable_table)


def list_from_syntax_tree(ast : AST, node_id):
    """
    Has to be called with the right child node of a list node.
    """
    node_name = ast.get_node_name(node_id)
    left_child = ast.get_left_node_id(node_id)
    right_child = ast.get_right_node_id(node_id)
  
    list = []
    if node_name == "list":
        list = list_from_syntax_tree(ast, right_child)
        ast.add_second_label_to_node(node_id, str(list))
        list = [list]
        list = list + list_from_syntax_tree(ast, left_child)
        
        

    elif node_name == "value":
        list = [convert_string_to_value(ast.get_node_name(left_child))]
        if right_child:
            next_value = list_from_syntax_tree(ast, right_child)
            list = list + next_value

    return list

def get_list_dimensions(lst):
    """
    This function takes a nested list (potentially multi-dimensional) and returns the dimensions of the list.
    For example, for a 3D list, it will return the dimensions in the form of [dim1, dim2, dim3].
    """
    if not isinstance(lst, list):
        return 1
    dimensions = []
    while isinstance(lst, list):
        dimensions.append(len(lst))
        lst = lst[0] if len(lst) > 0 else []
    return dimensions

def flatten_list(nested_lst):
    """Flatten a nested list into a flat list"""
    flat_list = []
    for item in nested_lst:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))  # Recursively flatten the list
        else:
            flat_list.append(item)
    return flat_list

def check_uniform_list_type(lst):
    if not lst:  # Check if the list is empty
        return "Empty list"
    
    # Flatten the list to get the real values
    flat_list = flatten_list(lst)
    
    if not flat_list:  # Check if the flattened list is empty
        return "Empty list after flattening"
    
    first_type = type(flat_list[0])
    if all(isinstance(item, first_type) for item in flat_list):  # Check if all elements are of the same type
        if first_type is str:
            return "char"
        elif first_type is int:
            return "int"
        elif first_type is float:
            return "float"
        else:
            return "Unsupported type"
    else:
        return "Mixed types"



def for_loop(ast : AST, node_id, variable_table : VariableTable):
    loop_header_id = ast.get_left_node_id(node_id)
    body_id = ast.get_right_node_id(node_id)
    statement_id = ast.get_right_node_id(loop_header_id)
    statement_and_condition_id = ast.get_left_node_id(loop_header_id)
    init_statement_id = ast.get_left_node_id(statement_and_condition_id)
    condition_id = ast.get_right_node_id(statement_and_condition_id)

    # declaration_init
    iterator = declaration(ast, init_statement_id, variable_table)
    init(ast, iterator, init_statement_id, variable_table)

    for_loop_body(ast, node_id, condition_id, body_id, statement_id, iterator, variable_table)

def for_loop_body(ast : AST, node_id, condition_id, body_id, statement_id, iterator, variable_table : VariableTable):
    # condition
    if(value_to_bool(condition(ast, condition_id, variable_table))):
        interpret_tree(ast, body_id, variable_table)
        expression(ast, statement_id, variable_table)
        for_loop_body(ast, node_id, condition_id, body_id, statement_id, iterator, variable_table)

def while_loop(ast : AST, node_id, variable_table : VariableTable):
    condition_id = ast.get_left_node_id(node_id)
    body_id = ast.get_right_node_id(node_id)

    if(value_to_bool(condition(ast, condition_id, variable_table))):
        interpret_tree(ast, body_id, variable_table)
        while_loop(ast, node_id, variable_table)

def if_else_statement(ast : AST, node_id, variable_table : VariableTable):
    global current_scope

    left_node_id = ast.get_left_node_id(node_id)
    left_node_name = ast.get_node_name(left_node_id)
    
    if(left_node_name == "else"):
        interpret_tree(ast, ast.get_right_node_id(left_node_id), variable_table)
        return
    
    if(condition(ast, ast.get_left_node_id(left_node_id), variable_table)):
        interpret_tree(ast, ast.get_right_node_id(left_node_id), variable_table)
        return
    else:
        if(ast.get_right_node_id(node_id)):
            if_else_statement(ast, ast.get_right_node_id(node_id), variable_table)
            return

def init(ast : AST, var_name, node_id, variable_table : VariableTable):

    right_node_id = ast.get_right_node_id(node_id)

    value = handle_statement(ast, right_node_id, variable_table)
    exists = variable_table.get_variable(var_name)
    if exists == None:
        dim = get_list_dimensions(value)
        type = None
        if dim != 1:
            type = check_uniform_list_type(value)
        else:
            type = get_type_from_string(value)
            if (type == "Unsupported type"): 
                raise Exception("Unsupported type in list")
            elif type == "Mixed types":
                raise Exception("Mixed types in list")
        variable_table.add_variable(var_name, current_scope[-1], dim, type)
    variable_table.change_variable_value(var_name, value)


def handle_statement(ast : AST, node_id, variable_table : VariableTable):
    node_name = ast.get_node_name(node_id)

    if node_name == "list":
        value = list_from_syntax_tree(ast, ast.get_right_node_id(node_id))
    elif node_name == "value":
        value_id = ast.get_left_node_id(node_id)
        value = ast.get_node_name(value_id)
    elif node_name == "identifier":
        identifier_id = ast.get_left_node_id(node_id)
        name = ast.get_node_name(identifier_id)
        value = variable_table.get_variable(name)['value']
    elif node_name == "expression":
        value = expression(ast, ast.get_left_node_id(node_id), variable_table)
    elif node_name == "condition":
        value = condition(ast, ast.get_left_node_id(node_id), variable_table)
    elif node_name == "type_cast":
        value = type_cast(ast, node_id, variable_table)
    elif node_name == "assign_to_array_element":
        arr_name = ast.get_node_name(ast.get_left_node_id(node_id))
        arr = variable_table.get_variable(arr_name)['value']
        index = ast.get_node_name(ast.get_left_node_id(ast.get_right_node_id(node_id)))
        index = [int(x.strip()) for x in index.split(',')]
        value = assign_value_to_array_element(index, arr)

    ast.add_second_label_to_node(node_id, str(value))
    return value
    

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
            var_dim = list(int(x.strip()) for x in var_dim.split(','))
    else:
        var_dim = [1]
        
    variable_table.add_variable(var_name, current_scope[-1], var_dim, var_type)
    return var_name


def printf(ast : AST, node_id, variable_table : VariableTable):
    global frame_counter
    right_node_id = ast.get_right_node_id(node_id)
    right_node_name = ast.get_node_name(right_node_id)

    left_node_id = ast.get_left_node_id(node_id)
    left_node_name = ast.get_node_name(left_node_id)
    left_node_name = left_node_name.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
    if right_node_id == None:
        print(left_node_name[1:-1]) # Remove quotes ('') from string
    else: 
        name = ast.get_node_name(right_node_id)
        if name not in variable_table.get_all_variables():
            raise Exception(f"Invalid variable in printf statement. '{name}' does not exist in the variable table.")
        value = variable_table.get_variable(name)['value']

        if '%d' in left_node_name:
            value = int(value)
        elif '%f' in left_node_name:
            value = float(value)

        formatted_string = re.sub(r'%[df]', '{}', left_node_name)
        pritf_string = formatted_string.format(value)[1:-1]
        print(pritf_string)
        dot = f'''
        digraph G {{
            node [shape=rectangle, style=filled, color=black, fontcolor=white];
            labelloc="t";
            label="Console Output";
            a [label="{pritf_string}"];
        }}
        '''
            

def headers(ast, node_id, variable_table):
    global include_dir
    global main_dir

    node_name = ast.get_node_name(node_id)
    match = re.search(r'^#include\s*<(.+\.dot)>', node_name)
    if match:
        print(node_name)
        header_name = match.group(1)
        header_path_main_dir = os.path.join(main_dir, header_name)
        header_path_include_dir = os.path.join(include_dir, header_name) if include_dir else None
        
        if os.path.exists(header_path_main_dir):
            header_ast = AST(header_path_main_dir)
            if header_ast.graph:
                interpret_tree(header_ast, header_ast.get_first_node_id(), variable_table)
        elif include_dir and os.path.exists(header_path_include_dir):
            ast = AST(header_path_include_dir)
            if header_ast.graph:
                interpret_tree(header_ast, header_ast.get_first_node_id(), variable_table)
        else:
            message = f"Header file {header_name} not found in {main_dir} or {include_dir}. Trying to interpret it anyway."
            warnings.warn(message)
    left_node_id = ast.get_left_node_id(node_id)
    right_node_id = ast.get_right_node_id(node_id)
    if left_node_id:
        headers(ast, left_node_id, variable_table)
    if right_node_id:
        headers(ast, right_node_id, variable_table)

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

def return_statement(ast : AST, node_id, variable_table : VariableTable):
        left_node_id = ast.get_left_node_id(node_id)
        left_node_id = ast.get_node_name(left_node_id)
        value = None
        if left_node_id == "value":
            value_id = ast.get_left_node_id(left_node_id)
            value = ast.get_node_name(value_id)
        elif left_node_id == "identifier":
            identifier_id = ast.get_left_node_id(left_node_id)
            name = ast.get_node_name(identifier_id)
            value = variable_table.get_variable(name)['value']
        return value
        
def interpret_tree(ast : AST, node_id, variable_table : VariableTable):
    global current_scope
    added_scope = False
    left_node_id = ast.get_left_node_id(node_id)
    right_node_id = ast.get_right_node_id(node_id)

    node_name = ast.get_node_name(node_id)

    if node_name == "if" or node_name == "if_else" or node_name == "for" or node_name == "while" or node_name == "program":
        current_scope += [node_id]
        added_scope = True
    
    if node_name == "program" or node_name == "main" or node_name == "body":
        # Recursion only for program, main and body nodes
        if (node_id != left_node_id) and left_node_id:    
            interpret_tree(ast, left_node_id, variable_table)
        if (node_id != right_node_id) and right_node_id:
            interpret_tree(ast, right_node_id, variable_table)


    elif node_name == "printf":
        printf(ast, node_id, variable_table)
        
        
    elif node_name == "scanf":
        scanf(ast, node_id, variable_table)
        

    elif node_name == "declaration":
        declaration(ast, node_id, variable_table)
        

    elif node_name == "declaration_init":
        var_name = declaration(ast, node_id, variable_table)
        init(ast, var_name, node_id, variable_table)
        
    
    elif node_name == "assign_array_element_to":
        assign_array_element_to(ast, node_id, variable_table)
        
    
    elif node_name == "assignment":
        assignment(ast, node_id, variable_table)
        

    elif node_name == "if_else":
        if_else_statement(ast, node_id, variable_table)
        

    elif node_name == "for":
        for_loop(ast, node_id, variable_table)
        

    elif node_name == "while":
        while_loop(ast, node_id, variable_table)
        

    elif node_name == "headers":
        headers(ast, node_id, variable_table)

    elif node_name == "expression":
        expression(ast, node_id, variable_table)
        

    elif node_name == "return":
        value = return_statement(ast, left_node_id, variable_table)
        return value
    

    if added_scope:
        scope_to_remove = current_scope[-1]
        variables_to_remove = [variable for variable, value in variable_table.get_all_variables().items() if value['scope'] == scope_to_remove]
        for variable in variables_to_remove:
            variable_table.remove_variable(variable)
        current_scope.pop()


def main():
    global main_dir
    global include_dir
    global variable_table

    bin_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin')

    parser = argparse.ArgumentParser(description='Process the tree path.')
    parser.add_argument('tree_path', help='Path to the tree file', nargs='?', default=os.path.join(bin_dir, 'tree.dot'))
    parser.add_argument('--include', help='Include folder path', type=str)
    parser.add_argument('--generate_video', action='store_true', help='If set, generate video of parse process')
    
    args = parser.parse_args()

    tree_path = args.tree_path
    main_dir = os.path.dirname(tree_path)
    include_dir = args.include if args.include else None

    ast = AST(tree_path, generate_parse_frames=args.generate_video)
    first_node_id = ast.get_first_node_id()


    if args.generate_video:
        frames_dir = os.path.join(bin_dir, 'interpretation_frames')
        time_stamp = os.path.getmtime(tree_path)
        old_frames_dir_base = os.path.join(bin_dir, 'interpretation_frames_OLD_')
        old_frames_dir = f"{old_frames_dir_base}{str(time_stamp)}"

        # Ensure the old_frames_dir is unique to avoid the error
        counter = 1
        while os.path.exists(old_frames_dir):
            old_frames_dir = f"{old_frames_dir_base}{str(time_stamp)}_{counter}"
            counter += 1

        if os.path.exists(frames_dir):
            shutil.move(frames_dir, old_frames_dir)

        interpretation_video = os.path.join(bin_dir, 'interpretation_video.mp4')
        if os.path.exists(interpretation_video):
            base, extension = os.path.splitext(interpretation_video)
            new_filename = f"{base}_OLD_{str(time_stamp)}{extension}"
            # Ensure the new_filename is unique
            counter = 1
            while os.path.exists(new_filename):
                new_filename = f"{base}_OLD_{str(time_stamp)}_{counter}{extension}"
                counter += 1
            # Renaming the file
            shutil.move(interpretation_video, new_filename)
    try:
        interpret_tree(ast, first_node_id, variable_table)
    except Exception as e:
        print(f"Error: {e}")

    if args.generate_video:
        print("Parsing Done. Generating video...")
        generate_video_from_dots(frames_dir, interpretation_video)


if __name__ == "__main__":
    main()