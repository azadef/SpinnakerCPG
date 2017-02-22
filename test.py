import nengo
import nengo_spinnaker
import numpy as np

model = nengo.Network()
with model:
    # ... Build a model
    n = nengo.Node(np.sin)
    e = nengo.Ensemble(100, 1)
    p = nengo.Probe(e)

    nengo.Connection(n, e)

sim = nengo_spinnaker.Simulator(model)
sim.run(10.)
sim.close()