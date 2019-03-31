import csv
import networkx
import matplotlib.pyplot as plt
import collections

# Parse through spreadsheet data
rowData = []
with open('whosampled30k.csv', mode='r', encoding="cp850") as dataSamples:
	dataSamples = csv.reader(dataSamples)
	# Read out header with row
	header = next(dataSamples)
	for row in dataSamples:
		if int(row[7]) >= 1970 and int(row[7]) <= 1979:
			rowData.append(row)

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
# Print number of times sampling something
# print(sorted(most_samples.items(), key=lambda sample: sample[1]))
# Print associated genre
# print(networkx.get_node_attributes(diG, 'genre'))

# Get all intragenre and intergenre samples
intraGenre = []
interGenre = []
for edge in diG.edges():
	# Print edge if it samples somebody in the same genre
	if diG.nodes()[edge[0]] == diG.nodes()[edge[1]]:
		intraGenre.append(edge)
	# Print edge if it samples somebody in another genre
	else:
		interGenre.append(edge)
# print(intraGenre)
# print(interGenre)

# Degree centrality
centrality = sorted(networkx.degree_centrality(diG).items(),
	key=lambda degCent: degCent[1])
# print(centrality)
# Betweenness centrality
betweenness = sorted(networkx.betweenness_centrality(diG).items(),
	key=lambda begCent: begCent[1])
# print(betweenness)

# Display graph
layout = networkx.shell_layout(diG)
# Create edge labels
edge_labels = networkx.get_edge_attributes(diG, 'audioElem')
networkx.draw_networkx_edge_labels(diG, layout, edge_labels, font_size=8)
# Create color map by genre by mapping respective genres to ints
color_map_genre = [hash(genre) for genre in networkx.get_node_attributes(diG, 'genre').values()]
# print(color_map_genre)
networkx.draw(diG, layout, with_labels=True, cmap=plt.cm.RdYlBu, node_color=color_map_genre, 
	node_size=[v * 100 for v in most_sampled.values()], font_size=8)
plt.show(diG)