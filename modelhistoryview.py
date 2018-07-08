import matplotlib.pyplot
import modelhistory
import numpy

def update_view():
	matplotlib.pyplot.figure(300).canvas.set_window_title('network status history')
	matplotlib.pyplot.clf()
	matplotlib.pyplot.plot(range(0,modelhistory.ticks+1),numpy.divide(modelhistory.num_nonbelievers,modelhistory.num_swing), label="nonbeliever")
	matplotlib.pyplot.plot(range(0,modelhistory.ticks+1),numpy.divide(modelhistory.num_believers,modelhistory.num_swing), label="believer")
	matplotlib.pyplot.plot(range(0,modelhistory.ticks+1),numpy.divide(modelhistory.num_susceptible,modelhistory.num_swing), label="susceptible")
	matplotlib.pyplot.legend()
	matplotlib.pyplot.draw()
	matplotlib.pyplot.pause(0.05)