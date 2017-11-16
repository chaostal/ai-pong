import nn

input_nodes = 4
hidden_nodes = 3
output_nodes = 3

learning_rate = 0.3

n = nn.neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

for a in range(0,1000):
    n.train([1,2,3,7],[0.2,0.8,0.4])

#r = n.query([1.0,0.5,-1.5])
r = n.query([1,2,3,0]) #.0,0.5,-1.5])
print r




