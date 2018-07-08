import model
import networkx
import matplotlib.pyplot

color = {'nonbeliever':'blue','believer':'red','susceptible':'gray'}
pos = None
node_size = None

def setup_view(layout=True):
	global pos
	if layout:
		pos = networkx.drawing.spring_layout(model.graph)
	else:
		pos = networkx.drawing.random_layout(model.graph)
	node_size = [10000 / len(model.graph.nodes)]*len(model.graph.nodes)
	matplotlib.pyplot.show(block=False)

labels = None
def setup_buzzers_view():
	global labels
	labels = {node:"" if model.is_swing[node] else "b" if model.is_hoax_buzzer[node] else "b" for node in model.graph.nodes}

def update_view():
	colormap = [node_color(node) for node in model.graph.nodes]
	matplotlib.pyplot.figure(200).canvas.set_window_title('current network status')
	matplotlib.pyplot.clf()
	networkx.draw(model.graph,pos, node_color=colormap, node_size = node_size)
	if labels is not None:
		networkx.draw_networkx_labels(model	.graph,pos,labels)
	matplotlib.pyplot.draw()
	matplotlib.pyplot.pause(0.05)

def node_color(node):
	if model.is_believer[node]:
		return color['believer']
	elif model.is_nonbeliever[node]:
		return color['nonbeliever']
	else:
		return color['susceptible']

