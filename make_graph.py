# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

class FG:
    def __init__(self, path, save_fig='graph.png', node_size=5, node_color='#a65628', pathlist=None):
        self.PATH = path
        self.rawDF = pd.read_csv(
            self.PATH / 'intersection_list.dat', sep=' ')
        self.fracturePOS = self.make_new_translation()
        self.featureDF = self.rawDF[(self.rawDF.f2 > 0) | (
            self.rawDF.f2 == -3) | (self.rawDF.f2 == -5)].reset_index(drop=True)
        self.nodes = np.unique(
            np.append(self.featureDF.f1.values, self.featureDF.f2.values))
        self.edges = self.featureDF[['f1', 'f2']].values
        self.edges_widths = self.featureDF['length'].values
        self.G = nx.Graph()
        self.pos = {}
        self.weightEdges = [[]]
        self.edgelabels = {}
        self.save_fig = save_fig
        self.set_graph()
        # self.add_st()

        self.node_color = node_color
        self.node_size = 5
        self.set_graph_color_size()
        if pathlist is not None:
            self.pathlist = pathlist
            self.set_path_color_size()

    def make_new_translation(self):
        dfn_dir = self.PATH
        data_dir = dfn_dir / 'translations.dat'
        datalist = pd.read_csv(self.PATH / 'translations.dat', sep=' ', skiprows=1, names=['x', 'y', 'z', 'rm'])
        '''
        with open(data_dir) as f:
            next(f)
            datalist = f.readlines()
            for data in datalist[:]:
                if data.endswith('R\n'):
                    datalist.remove(data)
        '''
        data_pd = datalist.query('rm != "R"').reset_index()
        data_pd = data_pd[['x', 'y', 'z']]
        return data_pd
        

    def set_graph(self):
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)
        for i in self.G.nodes:
            if i < 0:
                continue
            self.pos[i] = (self.fracturePOS.loc[i-1, 'x'],
                           self.fracturePOS.loc[i-1, 'y'])

        self.pos[-3] = (self.featureDF.x.min()-1.0, 0)
        self.pos[-5] = (self.featureDF.x.max()+1, 0)

    def add_st(self):
        connectS = list(
            self.featureDF[self.featureDF.f2 == -3].index)
        connectT = list(
            self.featureDF[self.featureDF.f2 == -5].index)

        for s in connectS:
            self.G.add_edge(-3, s, weight=0)

        for t in connectT:
            self.G.add_edge(-5, t, weight=0)

    def set_graph_color_size(self, opt=True):
        nx.set_node_attributes(self.G, name='color', values=self.node_color)
        nx.set_node_attributes(self.G, name='size', values=10)
        nx.set_node_attributes(self.G, name='label', values='')
        self.G.nodes[-3]['color'] = '#f781bf'
        self.G.nodes[-5]['color'] = '#81ddf7'
        self.G.nodes[-3]['size'] = 20
        self.G.nodes[-5]['size'] = 20
        self.G.nodes[-3]['label'] = 'source'
        self.G.nodes[-5]['label'] = 'target'
        nx.set_edge_attributes(self.G, name='color', values='#deb887')

    def set_specific_node_color(self, nodes_dic):
        nx.set_node_attributes(self.G, nodes_dic, name='color')

    def graph_show(self):

        self.node_size = list(nx.get_node_attributes(
            self.G, 'node_size').values())

        nx.draw_networkx_nodes(
            self.G,
            pos=self.pos,
            node_size=list(nx.get_node_attributes(self.G, 'size').values()),
            node_color=list(nx.get_node_attributes(self.G, 'color').values())
        )
        nx.draw_networkx_labels(self.G, labels=nx.get_node_attributes(self.G, 'label'), pos=self.pos,
                                font_size=10)

        nx.draw_networkx_edges(self.G, pos=self.pos, edge_color=list(
            nx.get_edge_attributes(self.G, 'color').values()), alpha=0.3)
        # nx.draw_networkx_edge_labels(
        # self.G, pos=self.pos, edge_labels=self.edgelabels, fontsize=1)

        plt.axis('off')
        # plt.title('FG')
        plt.savefig(self.save_fig)

    def set_path_color_size(self, node_color='#ff0000', node_size=100, edge_color='#ff0000'):
        path = [-3] + self.pathlist + [-5]
        for n, fracture in enumerate(path):
            if fracture < 0:
                continue
            self.G.nodes[fracture]['color'] = node_color
            self.G.nodes[fracture]['size'] = node_size
            self.G.nodes[fracture]['label'] = str(fracture)
            self.G.edges[(path[n-1], fracture)]['color'] = edge_color
        self.G.edges[(path[n-1], fracture)]['color'] = edge_color

if __name__ == "__main__":
    dfn_path = Path('/root/datadrive/predict_pathline/raw/full/dfn_0')
    fg = FG(dfn_path, pathlist=[8, 85, 8, 28, 16, 26, 22, 21, 22, 7, 92, 4, 47])
    fg.graph_show()
