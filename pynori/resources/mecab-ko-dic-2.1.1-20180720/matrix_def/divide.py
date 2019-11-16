import os


cur_path = os.getcwd()

###

conn_costs = []
with open(cur_path+'/matrix.def', 'r') as rf:
	for line in rf:
		line = line.strip()
		conn_costs.append(line)

print(len(conn_costs))

###

file_num = 10
step_size = int(len(conn_costs) / file_num)
ver = 0

for i, line in enumerate(conn_costs):

	if i % step_size == 0:
		ver += 1
		first_line = True
		
	with open(cur_path+'/matrix_split_{}.txt'.format(ver), 'a') as wf:
		if len(line.split()) == 3:

			if first_line == False:
				wf.write('\n')
		
			wf.write(line)
			first_line = False







