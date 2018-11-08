
	
def get_new_file(graph_name):
	output = open('%s.csv' % (graph_name),'wb')
	return output


def list_dot_plot_values(data, filename):
	output = get_new_file(filename)
	output.write("IRI's, IRT's" + '\r\n')
	#lentemp = data[0]
	#length = len(lentemp)
	#for x in range(length):
	for i in range(len(data[0])):
		output.write(str(data[0][i]) + ',' + str(data[1][i]) + '\r\n')
	output.close()