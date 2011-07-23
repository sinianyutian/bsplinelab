# -*- coding: UTF-8 -*-
from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from IPython.Debugger import Tracer
dh = Tracer()

class BSpline(object):

	def __init__(self, points, knots):
		self.points = np.array(points, float)
		self.knots = np.array(knots, float)
		self.length = len(knots) - len(points)
		self.degree = self.length + 1

	ktol = 1e-1

	def find(self, t):
		"""
		Unfinished function to find out between which node a time t is.
		"""
		raise DeprecationWarning
		# test this!
		dist = self.knots - t
		# test if it's right on a knot
		on_knot = abs(dist)
		nearest = on_knot.argmin()
		# if the nearest is on the right, return the previous one:
		knot = self.knots[nearest]
		if t < knot:
			nearest -= 1
# 		if nearest not in range(self.length,len(self.knots) + )
		return nearest
## 		# otherwise take the left node
## 		candidate = (dist > 0).argmax() - 1
## 		return candidate

	def plot_points(self):
		"""
		Plot the control points.
		"""
		plt.plot(self.points[:,0],self.points[:,1],'ro:')

## 	def plot_knots(self):
## 		kns = self.knots[self.length:-self.length]
## 		pts = np.array([self(kn,i) for i,kn in enumerate(kns[:-1])])
## 		plot(pts[:,0],pts[:,1],'sg')

	plotres = 200

	def k_range(self):
		return range(self.length, len(self.knots)-self.length-1)

	def generate_points(self, k_range=None):
		"""
		Compute the points from knot numbers k_range till the next ones.
		"""
		if k_range is None:
			k_range = self.k_range()
		for k in k_range:
			left, right = self.knots[k], self.knots[k+1]
			times = np.linspace(left, right, self.plotres * (right-left) + 1)
			yield (times,k,self(times,k,))


	def plot(self, knot=None, with_knots=False):
		"""
		Plot the curve.
		"""
		self.plot_points()
		for t,k,val in self.generate_points(knot):
			plt.plot(val[:,0],val[:,1], label="%1.f - %1.f" % (self.knots[k], self.knots[k+1]))
			if with_knots:
				plt.plot(val[[0,-1],0], val[[0,-1],1], 'gs')


	def __call__(self, t, lknot=None):
		if lknot is None:
			if np.isscalar(t):
				lknot = self.find(t)
			else:
				raise ValueError("A time array is only possible when the left knot is specified.")

		pts = self.points[lknot-self.length:lknot+2]
		kns = self.knots[lknot - self.degree +1:lknot + self.degree + 1]
		if len(kns) != 2*self.degree or len(pts) != self.length + 2:
			raise ValueError("Wrong knot index.")

		scalar_t = np.isscalar(t)
		if scalar_t:
			t = np.array([t])
		# we put the time on the first index; all other arrays must be reshaped accordingly
		t = t.reshape(-1,1,1)
		pts = pts[np.newaxis,...]

		for n in reversed(1+np.arange(self.degree)):
			diffs = kns[n:] - kns[:-n]
			lcoeff = (kns[n:] - t)/diffs
			rcoeff = (t - kns[:-n])/diffs
			pts = rcoeff.transpose(0,2,1) * pts[:,1:,:] + lcoeff.transpose(0,2,1) * pts[:,:-1,:]
			kns = kns[1:-1]
		result = pts[:,0,:]
		if scalar_t:
			result = np.squeeze(result) # test this
		return result

## class BSpline_basis(BSpline):
## 	def __init__(self, *args, **kwargs):
## 		super(BSpline_basis, self).__init__(self, *args, **kwargs)
## 		self.points = arange(len(self.points)).reshape(-1,1)



if __name__ == '__main__':
	ex1 = {
	'points': np.array([[1.,2], [2,3], [2,5], [1,6]]),
	'knots': np.array([3.,3.,3.,4.,4.,4.])
	}

	ex2 = {
	'points': np.array([[1.,2], [2,3], [2,5], [1,6], [1,9]]),
	'knots': np.array([1.,2.,3.,4.,5.,6.,7.])
	}

	# only C0
	ex3 = {
	'points': np.array([[1.,2], [2,3], [2,5], [1,6], [1,9], [2,11], [2,9]]),
	'knots': np.array([1.,2.,3.,4.,4.,4.,5.,6.,6.])
	}

	# discontinuous cubic
	ex4 = {
	'points': np.array([[1.,2], [2,3], [2,5], [1,6], [1,9], [2,11], [2,9], [1.5,8]]),
	'knots': np.array([1.,2.,3.,4.,4.,4.,4.,5.,6.,6.])
	}

	# discontinuous quad
	ex_d2 = {
	'points': np.array([[1.,2], [2,3], [1,6], [1,9], [2,11],  [1.5,8]]),
	'knots': np.array([1.,1.,2.,2.,2.,3.,3.,])
	}


	deBoor=[[0.7,-0.4],[1.0,-0.4],[2.5,-1.2],[3.2,-.5],[-0.2,-.5],[.5,-1.2],[2.0,-.4],[2.3,-.4]]
	param=[1.,1.,1.,1.2,1.4,1.6,1.8,2.,2.,2.]

	ex_Claus = {}
	ex_Claus['points'] = np.array(deBoor)
	ex_Claus['knots'] = np.array(param)

	ex = ex4

	s = BSpline(ex['pts'], ex['knots'])

	print s(np.array([3.2,3.5]), 2)
#	s.plot_points()
#	s.plot_knots()
	s.plot(with_knots=True)

## 	deBoor = array([[0.7,-0.4],
## 				[1.0,-0.4],
## 				[2.5,-1.2],
## 				[3.2,-.5],
## 				[-0.2,-.5],
## 				[.5,-1.2],
## 				[2.0,-.4],
## 				[2.3,-.4]])
## 	param = np.array([1.,1.,1.,1.2,1.4,1.6,1.8,2.,2.,2.])
## 	sc = BSpline(deBoor,param)
## 	sc.plot()
