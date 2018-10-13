import networkx as nx
import collections
import csv
import sys

# número do repositório para criação do GML
repository_id = int(sys.argv[1])

print('Gerando a rede completa...')
G = nx.read_weighted_edgelist('data/complete_network_%d.csv' % (repository_id), delimiter=',', nodetype=str)

nx.write_gml(G, 'data/GML/GML_complete_network_%d.gml' % (repository_id))

print("\n===Rede completa===")
print("Número de nós:", G.number_of_nodes())
print("Número de arestas:", G.number_of_edges())

print('\n\nGerando a rede filtrada por datas...')
G = nx.read_weighted_edgelist('data/network_with_dates_%d.csv' % (repository_id), delimiter=',', nodetype=str)

nx.write_gml(G, 'data/GML/GML_network_with_dates_%d.gml' % (repository_id)) 

print("\n===Rede filtrada===")
print("Número de nós:", G.number_of_nodes())
print("Número de arestas:", G.number_of_edges())