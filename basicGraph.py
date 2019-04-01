import csv
import networkx
import matplotlib.pyplot as plt
import matplotlib
import collections

# Set font sizes of plots
font = {'family': 'normal', 'size': 6}
matplotlib.rc('font', **font)

# Parse through spreadsheet data
with open('whosampled30k.csv', mode='r', encoding="cp850") as dataSamples:
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
# Print number of times sampling something
# print(sorted(most_samples.items(), key=lambda sample: sample[1]))
# Print associated genre
# print(networkx.get_node_attributes(diG, 'genre'))

# # Top 10 sampled and top 10 samplers
# top_10_sampled = sorted(most_sampled.items(), key=lambda sample: sample[1])[-10:]
# top_10_sampling = sorted(most_samples.items(), key=lambda sample: sample[1])[-10:]
# 	# Most sampled artists: ('Beside', 203), ('Lyn Collins', 233), ('Public Enemy', 258), ('The Winstons', 272), ('James Brown', 599)
# 	# Most sampling artists: ('J Dilla', 65), ('Lil B', 65), ('DJ Shadow', 77), ('Madlib', 88), ('Girl Talk', 99)
# fig, ax = plt.subplots()
# plt.xticks(rotation=25)
# plt.title('Most Sampling Artists by Count')
# plt.ylabel('Count')
# plt.xlabel('Sampling Artist')
# plt.gcf().subplots_adjust(bottom=0.15)
# # Separate tuple of top artists for graphing
# top_10_artists, top_10_artists_counts = zip(*top_10_sampling)
# for i, v in enumerate(top_10_sampling):
# 	ax.text(i - .15, v[1], str(v[1]))
# plt.bar(x=top_10_artists, height=top_10_artists_counts)

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

# # Display graph
# layout = networkx.shell_layout(diG)
# # Create edge labels
# edge_labels = networkx.get_edge_attributes(diG, 'audioElem')
# networkx.draw_networkx_edge_labels(diG, layout, edge_labels, font_size=8)
# # Create color map by genre by mapping respective genres to ints
# color_map_genre = [hash(genre) for genre in networkx.get_node_attributes(diG, 'genre').values()]
# networkx.draw(diG, layout, with_labels=True, cmap=plt.cm.RdYlBu, node_color=color_map_genre, 
# 	node_size=[v * 100 for v in most_sampled.values()], font_size=8)
plt.savefig('topSamplingArtistsCount.png')
