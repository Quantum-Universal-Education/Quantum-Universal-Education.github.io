import os
import seaborn 
import matplotlib.pyplot as plt

state_values = dict()

def init_variables(n=50,filename="bell_state.slq"):
	global state_values
	for i in range(n):
		os.system("silq " +filename+ " --run >> temp.log")


	f = open("temp.log", "r")
	values = []
	for x in f:
		values.append(x[1:len(x)-2].replace(",", "")) 
	state_values = {i:values.count(i)/n for i in values}
	os.system("rm -r temp.log")

def counts():
	return state_values

def plot_histogram():
	plt.bar(state_values.keys(),state_values.values(), align='edge', width=-0.5)
	plt.ylabel('Percentage (%)')
	plt.xlabel('State values')
	plt.title('Probability')
	plt.show()


#init_variables()
#init_variables(n=5,filename="peres_gate.slq")
#plot_histogram()




