import math
import matplotlib.pyplot as plt
import numpy as np
import time
#from graphviz import Digraph
from robot import Robot
from allbot import Allbot

cpg_num = 8
class CPGN:
	def __init__(self, name, t1, t2, w, b, u0, ue, uf, ve, vf):
		self.name = name

		self.t1= t1
		self.t2 = t2
		self.w = w
		self.b = b
		self.u0 = u0
		
		self.ue = ue
		self.uf = uf
		self.ve = ve
		self.vf = vf

		self.ue_n = 0
		self.uf_n = 0
		self.ve_n = 0
		self.vf_n = 0

		self.y = 0
		
		self.connected_cpgn = []
	def connect(self, cpgn, w):
		self.connected_cpgn.append([cpgn, w])
	def euler(self, dt):
		fue = -self.ue + self.w*max(0, self.uf) - self.b*self.ve + self.u0
		fuf = -self.uf + self.w*max(0, self.ue) - self.b*self.vf + self.u0
		for [cpgn, w] in self.connected_cpgn:
			fue += w*max(0, cpgn.ue)
			fuf += w*max(0, cpgn.uf)
		fve = -self.ve + max(0, self.ue)
		fvf = -self.vf + max(0, self.uf)
		self.ue_n = self.ue + dt*fue/self.t1
		self.uf_n = self.uf + dt*fuf/self.t1
		self.ve_n = self.ve + dt*fve/self.t2
		self.vf_n = self.vf + dt*fvf/self.t2
	def step(self):
		self.ue = self.ue_n
		self.uf = self.uf_n
		self.ve = self.ve_n
		self.vf = self.vf_n
		self.y = -max(0, self.ue) + max(0, self.uf)

def euler(ue, uf, v, t1, t2, w, b, u0, dt):
	u_n = ue + dt*(-ue + w*max(0, uf) - b*v + u0)/t1
	v_n = v + dt*(-v + max(0, ue))/t2
	return [u_n, v_n]

if __name__ == "__main__":
	#sim params
	steps = 50000
	dt = 0.001

	VarString = "0.41257655242500935, 0.8046931784719447, -2.213620726649234, 6.083603337271678, 1.2587318500390132, -0.8767170285553536, 0.5239295359309439, -0.6837279295103829, 0.8941848495811562"
	#neuron params
	VarString = VarString.split(", ")

	###
	t1 = float(VarString[0])
	t2 = float(VarString[1])
	w = float(VarString[2])
	b = float(VarString[3])
a	u0 = float(VarString[4])

	#start values
	ue = float(VarString[5])
	uf = float(VarString[6])
	ve = float(VarString[7]) #2
	vf = float(VarString[8])
	###
	#t1 = 0.551
	#t2 = 0.929
	#w = -3.463
	#b = 12.92
	#u0 = 1.207

	#start values
	#ue = -1
	#uf = -0.587
	#ve = 0.148 #2
	#vf = 0.313

	cpgns = []

	for i in range(cpg_num):
		cpgns.append(CPGN("N" + str(i+1), t1, t2, w, b, u0, ue, uf, ve, vf))

	cpgns[0].connect(cpgns[1], -0.6)
	cpgns[1].connect(cpgns[0], 0.6)

	cpgns[2].connect(cpgns[3], -0.6)
	cpgns[3].connect(cpgns[2], 0.6)

	cpgns[0].connect(cpgns[2], -0.2)
	cpgns[2].connect(cpgns[0], 0.2)

	cpgns[1].connect(cpgns[3], -0.2)
	cpgns[3].connect(cpgns[1], 0.2)

	cpgns[0].connect(cpgns[4], -0.6)
	cpgns[4].connect(cpgns[0], 0.6)

	cpgns[1].connect(cpgns[5], -0.6)
	cpgns[5].connect(cpgns[1], 0.6)

	cpgns[2].connect(cpgns[6], -0.6)
	cpgns[6].connect(cpgns[2], 0.6)

	cpgns[3].connect(cpgns[7], -0.6)
	cpgns[7].connect(cpgns[3], 0.6)
	#end definition

	cout = []
	for n in cpgns:
		cout.append([])

	print("running sim...")

	start = time.clock()

	for i in range(steps):
		for (i, n) in enumerate(cpgns):
			n.euler(dt)
		
		for (i, n) in enumerate(cpgns):
			n.step()
			cout[i].append(n.y)
			
	diff = (time.clock() - start)
	print("done in", diff, "s")
	x = np.linspace(0, steps*dt, steps)
	o = len(cpgns)*100
	o += 11

	r = Robot()

	r.reset_bot()
	r.reset()

	# a = Allbot()

	for i in range(len(cout[0])):
		if i < 5000:
			pass
		cmd = {
			'lff': cout[4][i],
			'rff': cout[5][i],
			'lbf': cout[6][i],
			'rbf': cout[7][i],
			'lfl': cout[0][i],
			'rfl': cout[1][i],
			'lbl': cout[2][i],
			'rbl': cout[3][i]
		}

		if i % 123 == 0:
			r.send_command(cmd)
			# a.command_robot(cmd)
			time.sleep(.1)

	# a.shutdown()

	y_target = []
	for i in range(cpg_num/2):
		y_target.append([ 0.5*np.sin(2*np.pi*33 * (i/50)) for i in np.linspace(0, steps*dt, steps)])
		y_target.append([ 0.5*np.cos(2*np.pi*33 * (i/50)) for i in np.linspace(0, steps*dt, steps)])

	for (i, n) in enumerate(cpgns):
		plt.subplot(o)
		o += 1
		plt.plot(x, cout[i])
		plt.plot(x,y_target[i])

	#f = Digraph('cpg_neurons')

	#for (i, n) in enumerate(cpgns):
	#	f.node(n.name)

	#for (i, n) in enumerate(cpgns):
	#	for [no, w] in n.connected_cpgn:
	#		f.edge(n.name, no.name, label=str(w))

	#f.view()


	plt.show()




