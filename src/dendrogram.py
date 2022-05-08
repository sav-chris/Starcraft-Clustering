import graphviz

class Dendrogram:

    def __init__(self, title:str, filename:str):
        self.graph = graphviz.Digraph(title, filename=filename)

    def add_node(self, group_index: int, build_order:str):
        self.graph.edge(str(group_index), build_order)
        
    def draw_graph(self):
        self.graph.render()


