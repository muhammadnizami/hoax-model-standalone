import model

ticks = None
num_nonbelievers = []
num_believers = []
num_susceptible = []
num_swing = []

def reset():
	global ticks
	ticks = 0
	del num_nonbelievers[:]
	del num_believers[:]
	del num_susceptible[:]
	del num_swing[:]
	insert_current_status()

def tick():
	global ticks
	ticks = ticks + 1
	insert_current_status()

def insert_current_status():
	global num_susceptible, num_believers, num_nonbelievers
	nN = len([node for node in model.graph.nodes if model.is_swing[node] and model.is_nonbeliever[node]])
	nB = len([node for node in model.graph.nodes if model.is_swing[node] and model.is_believer[node]])
	nS = len([node for node in model.graph.nodes if model.is_swing[node] and model.is_susceptible[node]])
	nSwing = len([node for node in model.graph.nodes if model.is_swing[node]])
	num_nonbelievers.append(nN)
	num_believers.append(nB)
	num_susceptible.append(nS)
	num_swing.append(nSwing)