import seaborn as sns

#Helper class for plotting
#Is static class so dont need to instantiate anything.
class Charts:

	def kdeplot(data1, data2, xmin=-50, xmax=100, ymin=0, ymax=700):
		kde = sns.kdeplot(data1, data2, shade=True)
		axes = kde.axes
		axes.set_xlim(xmin, xmax) #set the x range
		axes.set_ylim(ymin, ymax)
		return kde


	def jointplot(data1, data2):
		jp = sns.jointplot(data1, data2, kind="hex", color="#4CB391", xlim=(0, 500), ylim=(0, 1000))
		return jp

