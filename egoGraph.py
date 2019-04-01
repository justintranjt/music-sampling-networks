import csv
import networkx
import matplotlib.pyplot as plt
import matplotlib
import collections
from operator import itemgetter

# Set font sizes of plots
font = {'family': 'normal', 'size': 6}
matplotlib.rc('font', **font)

# Parse through spreadsheet data
with open('whosampled1250.csv', mode='r', encoding="cp850") as dataSamples:
	dataSamples = csv.reader(dataSamples)
	# Read out header with row
	header = next(dataSamples)
	rowData = [row for row in dataSamples]

# # Get all unique artists so we have 1:1 between IDs and artists
# uniqueSamplers = list(set([row[0] for row in rowData]))
# uniqueSamplees = list(set([row[4] for row in rowData]))
# # print('Unique Samplers: ' + str(len(uniqueSamplers)))
# # print('Unique Samplees: ' + str(len(uniqueSamplees)))

# # Count the number of songs in each genre
# uniqueGenreCountsSamplers = list(row[2] for row in rowData)
# uniqueGenreCountsSamplees = list(row[6] for row in rowData)
# samplerCounter = collections.Counter(uniqueGenreCountsSamplers)
# print('Unique Sampler Genres: ' + str(samplerCounter))
# sampleeCounter = collections.Counter(uniqueGenreCountsSamplees)
# print('Unique Samplee Genres: ' + str(sampleeCounter))
# # Display bar graph of sampled genres and sampling genres
# fig, ax = plt.subplots()
# for i, v in enumerate(sampleeCounter.values()):
# 	ax.text(i - .35, v, str(v))
# plt.xticks(rotation=32)
# plt.title('Most Sampled Genres by Count')
# plt.ylabel('Count')
# plt.xlabel('Genre')
# plt.gcf().subplots_adjust(bottom=0.15)
# plt.bar(*zip(*sampleeCounter.items()))
	# Hip-hop is the genre that samples the most often overall
	# Hip-hop is the 2nd-most sampled while Soul/Funk/Disco is the most sampled overall
	# What are the percentages?
	# 64.10% of the samplers are hip-hop, 31.98% of the sampled are Soul/Funk/Disco, 28.58% of sampled are hip hop

# Links is a list quintles 
# links = (samplingArtist, sampledArtist, elemSampled, samplingGenre, sampledGenre)
links = []
for row in rowData:
	links.append((row[0], row[4], row[9], row[2], row[6]))
# print(links)
# print(len(links))

# Create digraph
g = networkx.Graph()
diG = networkx.DiGraph(g, dataset="5000")
# Add nodes with genre attribute
for node in links:
	diG.add_node(node[0], genre=node[3])  # Sampling node
	diG.add_node(node[1], genre=node[4])  # Sampled node
# Put nodes in dictionary organized by {genre: artist}
byGenreNodes = collections.defaultdict(list)
for artist, genre in networkx.get_node_attributes(diG, 'genre').items():
	byGenreNodes[genre].append(artist)
# print(byGenreNodes)

# Create links and nodes, note that networkX needs links in tuples
for node in links: # Change each link and changes to tuple so it can be added
	diG.add_edge(u_of_edge=node[0], v_of_edge=node[1], audioElem=node[2])

# List of artists by number of times sampled
most_sampled = {}
# List of artists by number of times they used a sample
most_samples = {}
# Get degrees of each node
for node in diG.nodes:
	most_sampled[node] = diG.in_degree(node)
	most_samples[node] = diG.out_degree(node)

# Print number of times sampled
# print(sorted(most_sampled.items(), key=lambda sample: sample[1]))
# # Print number of times sampling something
# print(sorted(most_samples.items(), key=lambda sample: sample[1]))
# # Print associated genre
# print(networkx.get_node_attributes(diG, 'genre'))

# # Get all intragenre and intergenre samples
# intraGenre = []
# interGenre = []
# for edge in diG.edges():
# 	# Print edge if it samples somebody in the same genre
# 	if diG.nodes()[edge[0]] == diG.nodes()[edge[1]]:
# 		intraGenre.append(edge)
# 	# Print edge if it samples somebody in another genre
# 	else:
# 		interGenre.append(edge)
# # print(intraGenre)
# # print(interGenre)

# # Degree centrality
# centrality = sorted(networkx.degree_centrality(diG).items(),
# 	key=lambda degCent: degCent[1])
# # print(centrality)
# # Betweenness centrality
# betweenness = sorted(networkx.betweenness_centrality(diG).items(),
# 	key=lambda begCent: begCent[1])
# # print(betweenness)

# Display graph
# largest_hub is the artist with the most times sampled
(largest_hub, degree) = sorted(most_sampled.items(), key=itemgetter(1))[-2]
# largest_hub = 'The Winstons'
# Largest hub's samplers
largest_hub_samplers = [hub_sampler[0] for hub_sampler in networkx.edges(diG)
	if largest_hub in hub_sampler]
hub_ego = networkx.ego_graph(diG, largest_hub)
# Construct ego graph links
for link in links:
	if largest_hub in link:
		hub_ego.add_node(link[0], genre=link[3])
		hub_ego.add_edge(u_of_edge=largest_hub, v_of_edge=link[0], audioElem=link[2])
# Construct links of edges 1 away from ego hub
original_hub_nodes = dict(networkx.nodes(hub_ego))
for artist in original_hub_nodes:
	if artist == largest_hub:
		continue
	for link in links:
		if artist in link and link[0] not in original_hub_nodes:
			hub_ego.add_node(link[0], genre=link[3])
			hub_ego.add_edge(u_of_edge=link[0], v_of_edge=artist, audioElem=link[2])
		if artist in link and link[1] not in original_hub_nodes:
			hub_ego.add_node(link[1], genre=link[4])
			hub_ego.add_edge(u_of_edge=artist, v_of_edge=link[1], audioElem=link[2])
# All samplers in ego hub network
largest_hub_samplers = [hub_sampler[0] for hub_sampler in networkx.edges(hub_ego)]
pos = networkx.spring_layout(hub_ego)

# Create edge labels
edge_labels = networkx.get_edge_attributes(hub_ego, 'audioElem')
networkx.draw_networkx_edge_labels(hub_ego, pos, edge_labels, font_size=8)
# Create color map by genre by mapping respective genres to ints
color_map_genre = [hash(genre) for genre in networkx.get_node_attributes(hub_ego, 'genre').values()]

# Draw graph
networkx.draw(hub_ego, pos, cmap=plt.cm.RdYlBu, node_color=color_map_genre, node_size=100, with_labels=True, font_size=8)
del color_map_genre[0]
# Draw ego graph based on genre color
networkx.draw_networkx_nodes(hub_ego, pos, nodelist=largest_hub_samplers, node_size=100,
	cmap=plt.cm.RdYlBu, node_color=color_map_genre)
plt.show()
