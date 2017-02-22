import numpy as np
import nengo

model = nengo.Network()
tau = 0.1
ENS_SEED = 1
ENS_N_NEURONS = 100
trange =[10]
with model:
  # map from an oscilator to a pattern
  sig = nengo.Node(lambda t: (np.cos(t), np.sin(t)))
  readout = nengo.Ensemble(n_neurons=ENS_N_NEURONS, dimensions=2, seed=ENS_SEED)
  nengo.Connection(sig, readout, synapse=None)

  # get the spikes for future decoding
  p_spikes = nengo.Probe(readout.neurons, synapse=0.01)

sim_train = nengo.Simulator(model)
with sim_train:
    print(sim_train.dt)
    sim_train.run(trange[1])

solver = nengo.solvers.LstsqL2(reg=0.02)
decoders, info = solver(sim_train.data[p_spikes], target(sim_train.trange())[:, None])

test_model = nengo.Network()
with test_model:
    sig = nengo.Node(lambda t: (np.cos(t), np.sin(t)))

    readout = nengo.Ensemble(n_neurons=ENS_N_NEURONS, dimensions=2, seed=ENS_SEED)
    nengo.Connection(sig, readout, synapse=None)

    output = nengo.Node(size_in=1)
    nengo.Connection(readout.neurons, output, transform=decoders.T)

    p_out = nengo.Probe(output, synapse=0.01)