import numpy as np
import matplotlib.pyplot as plt
import threading as th
import nengo
import nengo_spinnaker
from scipy.interpolate import interp1d
import allbot

dimensions = 3
spinnaker = False

#Allbot = allbot.Allbot()
model = nengo.Network()
with model:
    num_neurons = dimensions * 30

    inp = nengo.Node(lambda t: np.sin(t*4), size_out=dimensions)
    pre = nengo.Ensemble(num_neurons, dimensions=dimensions)
    nengo.Connection(inp, pre)
    post = nengo.Ensemble(num_neurons, dimensions=dimensions)

    #voja = nengo.Voja(post_tau=None, learning_rate=5e-2)
    conn = nengo.Connection(pre, post, function=lambda x: np.random.random(dimensions))
    #conn = nengo.Connection(pre,post,synapse=None, learning_rule_type=voja)
    inp_p = nengo.Probe(inp)
    pre_p = nengo.Probe(pre, synapse=0.01)
    post_p = nengo.Probe(post, synapse=0.01)

    error = nengo.Ensemble(num_neurons, dimensions=dimensions)
    error_p = nengo.Probe(error, synapse=0.03)

    # Error = actual - target = post - pre
    nengo.Connection(post, error)
    nengo.Connection(pre, error, transform=-1)

    # Add the learning rule to the connection
    conn.learning_rule_type = nengo.PES()

    # Connect the error into the learning rule
    nengo.Connection(error, conn.learning_rule)

    inp2 = nengo.Node(lambda t: -np.cos(t*4), size_out=dimensions)
    pre2 = nengo.Ensemble(num_neurons, dimensions=dimensions)
    nengo.Connection(inp2, pre2)
    post2 = nengo.Ensemble(num_neurons, dimensions=dimensions)
    conn2 = nengo.Connection(pre2, post2, function=lambda x: np.random.random(dimensions))
    inp_p2 = nengo.Probe(inp2)
    pre_p2 = nengo.Probe(pre2, synapse=0.01)
    post_p2 = nengo.Probe(post2, synapse=0.01)

    error2 = nengo.Ensemble(num_neurons, dimensions=dimensions)
    error_p2 = nengo.Probe(error2, synapse=0.03)

    # Error = actual - target = post - pre
    nengo.Connection(post2, error2)
    nengo.Connection(pre2, error2, transform=-1)

    # Add the learning rule to the connection
    conn2.learning_rule_type = nengo.PES()

    # Connect the error into the learning rule
    nengo.Connection(error2, conn2.learning_rule)

if spinnaker:
    sim = nengo_spinnaker.Simulator(model)
else:
    sim = nengo.Simulator(model)
simTime  = 10
for t in range(simTime):
    sim.run(1.0)

inter = interp1d([-1.1,1.1],[0,90])
#data_new = []
#samples = np.arange(0,20000,16)

#for d in range(dimensions):
data_1 = inter(sim.data[post_p].T[0][::500])
data_2 = inter(sim.data[post_p2].T[0][::500])
cmd1 = data_1.astype(int)
cmd2 = data_2.astype(int)
print(cmd1)
for value1, value2 in zip(cmd1,cmd2):
    #Allbot.command_robot(value1,value2,value1,value2,value1,value2,value1,value2)
    print(value1)
figure, axes = plt.subplots(dimensions + 1, sharex=True)

for a, d in zip(axes, range(dimensions)):
    a.plot(sim.trange(), sim.data[inp_p].T[d], c='k', label='Input')
    a.plot(sim.trange(), sim.data[pre_p].T[d], c='b', label='Pre')
    a.plot(sim.trange(), sim.data[post_p].T[d], c='r', label='Post')
    a.plot(sim.trange(), sim.data[post_p2].T[d], c='g', label='Post 2')

    a.set_ylabel("Dimensions 1")
    a.legend()

axes[dimensions].plot(sim.trange(), sim.data[error_p], c='b')
axes[dimensions].set_ylim(-1, 1)
axes[dimensions].set_ylabel("Error")
#axes[dimensions].legend(("Error[0]", "Error[1]"), loc='best');
#axes[dimensions+1].plot(data_1)
plt.show()
plt.savefig('test1.png')

