import math
import torch
import numpy as np
from scipy.sparse import csc_matrix
import heapq
import json


# csc encoding
def csc_encode(matrix):

    original_shape = matrix.size()
    # flat the matrix because csc_matrix() requires dimension <= 2
    matrix = matrix.view(1, -1)
    # csc encoding
    csc = csc_matrix(matrix)  # compress the sparse matrix
    # buf is a dict to store the information needed to recover the data
    buf = {}
    buf['data'] = csc.data.tolist()
    buf['indices'] =  csc.indices.tolist()
    buf['indptr'] = csc.indptr.tolist()
    buf['shape'] = matrix.size()     # the shape before csc_matrix()
    buf['original_shape'] = original_shape   # the shape before flatten

    return buf

# csc decoding
def csc_decode(pack):

    result = csc_matrix((pack['data'], pack['indices'], pack['indptr']), shape=pack['shape']).toarray()
    # recover to the original shape of the grads (like [10,1,5,5] for simple CNN layer)
    matrix = result.reshape(pack['original_shape']) 

    return torch.from_numpy(matrix)


class Gradcomp(object):
    """
        A gradient compress model
    """

    def __init__(self, name, shape) -> None:
        super().__init__()
        '''
            A gradient compress model init method
             
        '''
        self.residuals = torch.zeros(shape)
        self.name = name

    # ready
    def upgrade_threshold(self, grad, threshold):

        # compress grad with element threshold
        grad = self.residuals.add_(grad)
        # get the index matrix by > operation
        sample_matrix = (grad.abs() > threshold).float() 
        #get the sparse grad matrix
        sample_matrix.mul_(grad)   

        self.residuals.sub_(sample_matrix)


        sample = csc_encode(sample_matrix)
    
        # to send the data
        return sample


    #ready
    def upgrade_rate(self, grad, rate):   # the dimention is 
        # compress grad with compress rate
        grad = self.residuals.add_(grad)

        #print('the shape of the layer: ', self.name, ' is ', grad.size())

        original_shape = grad.size()
        #flaten the grads
        grad = grad.view(1,-1)
        nb_sample = int(max(1, grad.size()[1]*rate))
        sample, indexes = grad.abs().topk(nb_sample)   #time inefficient
        threshold = sample[0, sample.size()[1]-1]  #get the threshold

        #recover the shape 
        grad = grad.view(original_shape)
        sample_matrix = (grad.abs() > threshold).float()

        #print('after the compression by rate, ', sample_matrix.sum().int().item(), 'grads are left!')

        sample_matrix.mul_(grad)

        self.residuals.sub_(sample_matrix)

        sample = csc_encode(sample_matrix)

        return sample

        # to send the data
        #socketsend(sample_matrix)

    
    #not ready
    def upgrade_auto(self, grad, bin_size):
        # use adacomp method
        G = self.residuals.add_(grad)
        H = G + grad  #cannot use in-place add 
        original_shape = G.size()
        G = G.view(1, -1)
        H = H.view(1, -1)

        len_grad = G.size()[1]

        num_bin = math.ceil(len_grad/bin_size)

        # consider len_grad%bin_size not 0
        num_zero = num_bin * bin_size - len_grad

        if num_zero > 0:
            zeros = torch.zeros(1,num_zero)
            G = torch.cat((G, zeros), 1)
            H = torch.cat((H, zeros), 1)


        G = G.view(num_bin, bin_size)
        H = H.view(num_bin, bin_size)

        # get the max grad in each row
        grad_max = []
        for row in G:
            grad_max.append(row.abs().max().item())

        # compare 2*grad with grad(max), send the bigger part
        sample_matrix = torch.Tensor
        i = 0
        for row in H:
            if i == 0:
                sample_matrix = row.abs() > grad_max[i]
            else:
                row_sample = row.abs() > grad_max[i]
                # print('row in H: ', row.abs(), ' compared to ', grad_max[i])
                # print('get a new row sample: ',row_sample)
                sample_matrix = torch.cat((sample_matrix, row_sample), 0)
            i+=1

        sample_matrix = sample_matrix.view(num_bin, bin_size).float()
        sample_matrix.mul_(G)

        #recover to the original shape
        #这里因为之前在G和H中补了0，所以需要先把0去掉才会恢复原始的grad纬度

        sample_matrix = sample_matrix.view(1,-1)
        sample_matrix = sample_matrix[0,0:sample_matrix.size()[1]-num_zero]
        sample_matrix = sample_matrix.view(original_shape)

        self.residuals.sub_(sample_matrix)

        sample = csc_encode(sample_matrix)
 
        # to send the data
        # socketsend(sample)
        return sample



#这里的GradHandle是引用传递，传递进去的是{layer_name: para}字典，这样就相当于把para的句柄保存起来，直接可以在这个类里
#查询最新的梯度值，每次update时只要指定layer_name和threshold或者rate就行。GradComps字典保存了所有的Gradcomp对象，每
#一层网络都有一个Gradcomp对像。   

#this is the gradients of the whole model, for each level assign a Gradcomp object
class Grad_Block(object):
    def __init__(self, GradHandle):   #input the state_dict of the model

        # (name: Gradcomp) pair
        self.GradComps = {}

        #create a dict of Gradcomp object
        for name in GradHandle:
            self.GradComps[name] = Gradcomp(name, GradHandle[name].data.size())

        self.GradData = GradHandle    #contain the latest gradients data


    def update_threshold(self, layer_name, threshold):

        grads = self.GradComps[layer_name].upgrade_threshold(self.GradData[layer_name].grad.data, threshold)

        sendData = json.dumps(grads)   

        #...

        recvData = json.loads(sendData)

        grads = csc_decode(recvData)

        return grads

    def update_rate(self, layer_name, rate):

        grads = self.GradComps[layer_name].upgrade_rate(self.GradData[layer_name].grad.data, rate)

        sendData = json.dumps(grads)

        #...

        recvData = json.loads(sendData)

        grads = csc_decode(recvData)

        return grads

    def update_auto(self, layer_name, bin_size):

        grads = self.GradComps[layer_name].upgrade_auto(self.GradData[layer_name].grad.data, bin_size)

        sendData = json.dumps(grads)

        recvData = json.loads(sendData)

        grads = csc_decode(recvData)

        return grads



