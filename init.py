import Load_MNIST as lm 
import Neural_Networks as nn 

train_data , validate_date , test_data = lm.prepare_dataset()
net = nn.Network([784,30,10])
net.stochastic_gradient_descent(train_data,30,10,3.0,test_data)
