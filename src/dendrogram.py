import graphviz

class Dendrogram:

    def __init__(self, title:str, filename:str):
        self.graph = graphviz.Digraph(title, filename=filename)

    def add_node(self, group_index: int, build_order:str):
        self.graph.edge(str(group_index), build_order)
        
    def draw_graph(self):
        self.graph.view()



        

#import pydot
# class Dendrogram:

#     def __init__(self, title:str):
#         groups: List[int] = []
#         graph = pydot.Dot(title, graph_type="graph", bgcolor="white")

#     def add_group(self, group_index: int):
#         pass

#     def add_node9


#     def generate_dendrogram(self):
        

#         # Add nodes
#         my_node = pydot.Node("a", label="Foo")
#         graph.add_node(my_node)
#         # Or, without using an intermediate variable:
#         graph.add_node(pydot.Node("b", shape="circle"))

#         # Add edges
#         my_edge = pydot.Edge("a", "b", color="blue")
#         graph.add_edge(my_edge)
        
#         graph.write_png("output.png")

