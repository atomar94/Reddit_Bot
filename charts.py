import seaborn as sns

class Charts:


	def __init__(self):
		pass

	def kdeplot(data1, data2, xmin=-50, xmax=100, ymin=0, ymax=700):
		kde = sns.kdeplot(data1, data2, shade=True)
		axes = kde.axes
		axes.set_xlim(xmin, xmax) #set the x range
		axes.set_ylim(ymin, ymax)
		return kde


