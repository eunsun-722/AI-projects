# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch


np.random.seed(0)
torch.manual_seed(0)

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        """
        super(NeuralNet, self).__init__()

        '''
        self.layer1 = torch.nn.Linear(in_size, 100)
        self.relu1 = torch.nn.Tanh()
        self.layer2 = torch.nn.Linear(100,88)
        self.relu2 = torch.nn.ReLU()
        self.layer3 = torch.nn.Linear(88, out_size)
        '''
        self.conv1 = torch.nn.Conv2d(3, 6, 5)
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.conv2 = torch.nn.Conv2d(6, 16, 5)
        self.fc1 = torch.nn.Linear(16 * 5 * 5, 30)
        self.fc2 = torch.nn.Linear(30, 60)
        self.fc3 = torch.nn.Linear(60, out_size)


        self.loss_fn = loss_fn

        '''
        0.8416
        self.layer1,
        self.relu1,
        self.layer2,
        self.relu2,
        self.layer3


        self.model = torch.nn.Sequential(
            self.layer1,
            self.relu1,
            self.layer2,
            self.relu2,
            self.layer3
        )
        '''


        self.optimizer = torch.optim.Adam(self.parameters(), lr=lrate)
        # self.optimizer = torch.optim.Adam(self.get_parameters(), lr=lrate)


    def set_parameters(self, params):
        """ Set the parameters of your network
        @param params: a list of tensors containing all parameters of the network
        """
        #self.parameters = params
        pass

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters()
        #return list(self.model.parameters())


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        #return torch.ones(x.shape[0], 1)

        x = x.view(-1, 3, 32, 32)
        x = self.pool(torch.nn.functional.relu(self.conv1(x)))
        x = self.pool(torch.nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

        #return self.model(x)

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        loss=self.loss_fn(self.forward(x),y)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()



def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, out_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of epochs of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    #lrate = 0.00051234667
    lrate = 0.0001
    loss_fn = torch.nn.CrossEntropyLoss()
    net = NeuralNet(lrate, loss_fn, len(train_set[0]), 2)

    #train
    losses = []
    loss = 0
    '''
    for epoch in range(n_iter):
        curr_loss = net.step(train_set, train_labels)
        loss += curr_loss
        losses.append(loss)

    PATH = '.net.model'
    torch.save(net.state_dict(), PATH)
    '''

    trainset = torch.utils.data.TensorDataset(train_set, train_labels)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size)

    for epoch in range(n_iter):
        loss = 0
        for i, data in enumerate(trainloader, 0):
            inputs, label = data
            curr_loss = net.step(inputs, label)
            loss += curr_loss
        losses.append(loss)


    #PATH = './net.model'
    #torch.save(net.state_dict(), PATH)

    # test_set = torch.utils.data.TensorDataset(dev_set)
    # testLoader = torch.utils.data.DataLoader(test_set, batch_size=batch_size)

    yhats = np.zeros(len(dev_set))
    i = 0
    for data in dev_set:
        output = net(data)
        #_, predicted = torch.max(output.detach(), 0)
        yhats[i] = np.argmax(output.detach())
        i += 1

    return losses,yhats, net
