import csv
import networkx
import matplotlib.pyplot as plt
import collections
import community

# Parse through spreadsheet data
with open('whosampled50.csv', mode='r', encoding="cp850") as dataSamples:
	dataSamples = csv.reader(dataSamples)
	# Read out header with row
	header = next(dataSamples)
	rowData = [row for row in dataSamples]

# Get all unique artists so we have 1:1 between IDs and artists
uniqueSamplers = list(set([row[0] for row in rowData]))
uniqueSamplees = list(set([row[4] for row in rowData]))
# print('Unique Samplers: ' + str(len(uniqueSamplers)))
# print('Unique Samplees: ' + str(len(uniqueSamplees)))

# Count the number of songs in each genre
uniqueGenreCountsSamplers = list(row[2] for row in rowData)
uniqueGenreCountsSamplees = list(row[6] for row in rowData)
counter = collections.Counter(uniqueGenreCountsSamplers)
# print('Unique Sampler Genres: ' + str(counter))
counter = collections.Counter(uniqueGenreCountsSamplees)
# print('Unique Samplee Genres: ' + str(counter))

# creates a list of tuples with unique ids and their names for each artist
idSampler = list(enumerate(uniqueSamplers))
idSamplee = list(enumerate(uniqueSamplees))
# creates a dictionary(hash map) that maps each id to the artist names
keysSampler = {name: i for i, name in enumerate(uniqueSamplers)}
keysSamplee = {name: i for i, name in enumerate(uniqueSamplees)}

# Links is a list quintles 
# links = (samplingArtist, sampledArtist, elemSampled, samplingGenre, sampledGenre)
links = []
for row in rowData:
	# Maps all arists in spreadsheet to their IDs
	# try:
	# 	# Note this creates links from sampler only. TODO: Change in future to just creating a tuple from start?
	# 	links.append({keysSampler[row[0]]: keysSampler[row[4]]})
	# except:
	links.append((row[0], row[4], row[9], row[2], row[6]))
# print(links)
# print(len(links))

# Create digraph
g = networkx.Graph()
diG = networkx.DiGraph(g, dataset="5000")

# Add nodes with genre attribute
for node in links:
	g.add_node(node[0], genre=node[3])  # Sampling node
	g.add_node(node[1], genre=node[4])  # Sampled node
# Put nodes in dictionary organized by {genre: artist}
byGenreNodes = collections.defaultdict(list)
for artist, genre in networkx.get_node_attributes(g, 'genre').items():
	byGenreNodes[genre].append(artist)
# print(byGenreNodes)

# Create links, note that networkX needs links in tuples
for node in links: # Change each link and changes to tuple so it can be added
	# print(node)
	g.add_edge(node[0], node[1], audioElem=node[2])

# List of artists by number of times sampled
most_sampled = {}
# List of artists by number of times they used a sample
most_samples ={}
# TODO: Remove zeros from lists
for node in diG.nodes:
	most_sampled[node] = diG.in_degree(node)
	most_samples[node] = diG.out_degree(node)

# Print number of times sampled
# print(sorted(most_sampled.items(), key=lambda sample: sample[1]))
# Print number of times sampling something
# print(sorted(most_samples.items(), key=lambda sample: sample[1]))
# Print associated genre
# print(networkx.get_node_attributes(diG, 'genre'))

# Get all intragenre and intergenre samples
intraGenre = []
interGenre = []
for edge in g.edges():
	# Print edge if it samples somebody in the same genre
	if g.nodes()[edge[0]] == g.nodes()[edge[1]]:
		intraGenre.append(edge)
	# Print edge if it samples somebody in another genre
	else:
		interGenre.append(edge)
# print(intraGenre)
# print(interGenre)

# Compute communities using Louvain method
partition = community.best_partition(g)
# Gather all communities and members of each community (group them by value)
unsortLouv = collections.defaultdict(list)
for key, val in partition.items():
	unsortLouv[val].append(key)
# Arranging largest communities first in sortedLouv
sortLouvIndex = sorted(unsortLouv, key=lambda k: len(unsortLouv[k]), reverse=True)
sortedLouv = []
for i in range(len(sortLouvIndex)):
	
	if len(unsortLouv[sortLouvIndex[i]]) > 2:
		sortedLouv.append(unsortLouv[sortLouvIndex[i]])
	else:
		break
# print(sortedLouv)

# Here is an alternative community-forming algorithm for k-components
# Arranging largest communities first in kComponents
sortedkComp = []
for kComp in networkx.k_components(g)[1]:
	# Only include k-components greater than 2
	if len(kComp) > 2:
		sortedkComp.append(kComp)
sortedkComp = sorted(sortedkComp, key=len, reverse=True)
# print(sortedkComp)

# TODO: We have communities now; how do we know who they're centered around?
# Take centrality measurement?
# Maybe take the top 10 communities only and study those in-depth?
pos = networkx.spring_layout(g)  # compute graph layout
# Create edge labels
edge_labels = networkx.get_edge_attributes(g, 'audioElem')
networkx.draw_networkx_edge_labels(g, pos, edge_labels, font_size=8)
# Create color map by genre by mapping respective genres to ints
color_map_genre = [hash(genre) for genre in networkx.get_node_attributes(g, 'genre').values()]
plt.axis('off')
networkx.draw_networkx_nodes(g, pos, node_size=100, cmap=plt.cm.RdYlBu,
	node_color=color_map_genre)
networkx.draw_networkx_edges(g, pos, alpha=0.3)
networkx.draw_networkx_labels(g, pos, font_size=8)
# plt.show(g)
