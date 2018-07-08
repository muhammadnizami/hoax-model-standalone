import networkx
from numpy import random
from numpy import argpartition

#we implement the model into two parts: the graph and the attributes of the nodes
graph = networkx.empty_graph()
is_hoax_buzzer = []
is_clarifying_buzzer = []
is_swing = []
is_nonbeliever = []
is_believer = []
is_susceptible = []

#temporary attributes
become_believer_probability = []
become_nonbeliever_probability = []
become_susceptible_probability = []

def init_attrs():
	n = len(graph)
	global is_hoax_buzzer, is_clarifying_buzzer, is_swing, is_nonbeliever, is_believer, is_susceptible, become_believer_probability, become_susceptible_probability, become_nonbeliever_probability
	is_hoax_buzzer = [False] * n
	is_clarifying_buzzer = [False] * n
	is_swing = [False] * n
	is_nonbeliever = [False] * n
	is_believer = [False] * n
	is_susceptible = [False] * n
	become_believer_probability = [0.33333333333333] * n
	become_nonbeliever_probability = [0.33333333333333] * n
	become_susceptible_probability = [0.33333333333333] * n

#node procedures
def become_hoax_buzzer(node):
	is_hoax_buzzer[node]=True
	is_clarifying_buzzer[node]=False
	is_swing[node]=False
	become_believer(node)
	
def become_clarifying_buzzer(node):
	is_hoax_buzzer[node]=False
	is_clarifying_buzzer[node]=True
	is_swing[node]=False
	become_nonbeliever(node)
	
def become_swing(node):
	is_hoax_buzzer[node]=False
	is_clarifying_buzzer[node]=False
	is_swing[node]=True

def become_susceptible(node):
	is_nonbeliever[node]=False
	is_believer[node]=False
	is_susceptible[node]=True

def become_nonbeliever(node):
	is_nonbeliever[node]=True
	is_believer[node]=False
	is_susceptible[node]=False

def become_believer(node):
	is_nonbeliever[node]=False
	is_believer[node]=True
	is_susceptible[node]=False

# setups the network and initial outbreak
def setup_network(network_type, n, k, initial_outbreak):
	global graph

	if (network_type=='barabasi-albert'):
		m = k / 1.95
		graph = networkx.barabasi_albert_graph(n,k)
	else:
		p = k / n
		graph = networkx.erdos_renyi_graph(n,p)
	init_attrs()

	for node in graph.nodes:
		become_swing(node)
		become_susceptible(node)

	for node in random.choice(graph.nodes,initial_outbreak):
		become_believer(node)

# turns some of the swing agents into buzzers
def setup_buzzers(num_clarifying_buzzers, clarifying_buzzer_placement, num_hoax_buzzers, hoax_buzzer_placement, threshold = 0.05):
	clear_clarifying_buzzers()
	clear_hoax_buzzers()
	setup_clarifying_buzzers(num_clarifying_buzzers,clarifying_buzzer_placement, threshold)
	setup_hoax_buzzers(num_hoax_buzzers,hoax_buzzer_placement, threshold)

# turns every clarifying buzzers into swing agents
def clear_clarifying_buzzers():
	for node in (node for node in graph.nodes if is_clarifying_buzzer[node]):
		become_swing(node)
		become_susceptible(node)

# turns every hoax buzzers into swing agents
def clear_hoax_buzzers():
	for node in (node for node in graph.nodes if is_hoax_buzzer[node]):
		become_swing(node)
		become_susceptible(node)

# selects some buzzer candidate based on placement strategy and number
def select_buzzers(number, strategy, threshold=0.05):
	swing_nodes = [node for node in graph.nodes if is_swing[node]]
	num_threshold = round(threshold*len(swing_nodes))
	degrees = list(zip(*networkx.degree(graph,swing_nodes)))[1]
	if strategy=='random':
		candidates=swing_nodes
	elif strategy=='supernodes':
		candidates=[swing_nodes[index] for index in argpartition(degrees, -num_threshold)[-num_threshold:]]
	else:
		candidates=[swing_nodes[index] for index in argpartition(degrees, num_threshold)[:num_threshold]]
	return random.choice(candidates,number)

# setups clarifying buzzers
def setup_clarifying_buzzers(number, strategy, threshold=0.05):
	for node in select_buzzers(number, strategy, threshold):
		become_clarifying_buzzer(node)

#setups hoax buzzers
def setup_hoax_buzzers(number, strategy, threshold=0.05):
	for node in select_buzzers(number, strategy, threshold):
		become_hoax_buzzer(node)

def go(spread_chance,hoax_believability,forget_chance,vv_chance,iv_chance,bf_chance):
	for node in [node for node in graph.nodes if is_swing[node]]:
		update_probabilities(node,spread_chance,hoax_believability,forget_chance,vv_chance,iv_chance,bf_chance)
	for node in [node for node in graph.nodes if is_swing[node]]:
		execute_probabilities(node)

def update_probabilities(node,spread_chance,hoax_believability,forget_chance,vv_chance,iv_chance,bf_chance):
	become_believer_probability[node] = is_swing[node]*(f(node,spread_chance,hoax_believability)*is_susceptible[node]+(1- j(node, spread_chance, hoax_believability, forget_chance, vv_chance, iv_chance, bf_chance)- h(node, spread_chance, hoax_believability, vv_chance, iv_chance, bf_chance))*is_believer[node]) + is_hoax_buzzer[node] * 1
	become_nonbeliever_probability[node] = is_swing[node]*(g(node, spread_chance, hoax_believability)*is_susceptible[node]+ h(node, spread_chance, hoax_believability, vv_chance, iv_chance, bf_chance)*is_believer[node]+(1-forget_chance)*is_nonbeliever[node]) + is_clarifying_buzzer[node] * 1
	become_susceptible_probability[node] = is_swing[node]*(j(node, spread_chance, hoax_believability, forget_chance, vv_chance, iv_chance, bf_chance)*is_believer[node]+forget_chance*is_nonbeliever[node]+(1-f(node,spread_chance,hoax_believability)-g(node, spread_chance, hoax_believability))*is_susceptible[node])

# transition functions
# please refer to the paper for more details
def f(node,spread_chance,hoax_believability):
	nB = len([neighbor for neighbor in graph.neighbors(node) if is_believer[neighbor]])
	nN = len([neighbor for neighbor in graph.neighbors(node) if is_nonbeliever[neighbor]])
	if nB * (1 + hoax_believability) == 0: #avoid division by zero
		return 0
	else:
		return spread_chance * (nB * (1 + hoax_believability))/(nB * (1 + hoax_believability) + nN * (1 - hoax_believability))

def g(node, spread_chance, hoax_believability):
	nB = len([neighbor for neighbor in graph.neighbors(node) if is_believer[neighbor]])
	nN = len([neighbor for neighbor in graph.neighbors(node) if is_nonbeliever[neighbor]])
	if nN * (1 - hoax_believability) == 0: #avoid division by zero
		return 0
	else:
		return spread_chance * (nN * (1 - hoax_believability))/(nB * (1 + hoax_believability) + nN * (1 - hoax_believability))

def h(node, spread_chance, hoax_believability, vv_chance, iv_chance, bf_chance):
	nB = len([neighbor for neighbor in graph.neighbors(node) if is_believer[neighbor]])
	nN = len([neighbor for neighbor in graph.neighbors(node) if is_nonbeliever[neighbor]])
	if nN * iv_chance == 0: #avoid division by zero
		return vv_chance;
	else:
		return (1 - vv_chance) * spread_chance * (nN * iv_chance)/(nB * (1 - iv_chance - bf_chance) + nN * (iv_chance + bf_chance)) + vv_chance

def j(node, spread_chance, hoax_believability, forget_chance, vv_chance, iv_chance, bf_chance):
	nB = len([neighbor for neighbor in graph.neighbors(node) if is_believer[neighbor]])
	nN = len([neighbor for neighbor in graph.neighbors(node) if is_nonbeliever[neighbor]])
	if nN * (iv_chance + bf_chance) == 0: #avoid division by zero
		return forget_chance;
	else:
		return forget_chance * (1 - spread_chance * (nN * (iv_chance + bf_chance)/(nB * (1 - iv_chance - bf_chance) + nN * (iv_chance + bf_chance))))

def execute_probabilities(node):
	r = random.uniform()
	if r < become_believer_probability[node]:
		become_believer(node)
	elif r - become_believer_probability[node] < become_nonbeliever_probability[node]:
		become_nonbeliever(node)
	else:
		become_susceptible(node)

def counts():
	count_nonbeliever = len([node for node in graph.nodes if is_swing[node] and is_nonbeliever[node]])
	count_believer = len([node for node in graph.nodes if is_swing[node] and is_believer[node]])
	count_susceptible = len([node for node in graph.nodes if is_swing[node] and is_susceptible[node]])
	return count_nonbeliever, count_believer, count_susceptible

def precentages():
	return counts() / len([node for node in graph.nodes if is_swing[node]])