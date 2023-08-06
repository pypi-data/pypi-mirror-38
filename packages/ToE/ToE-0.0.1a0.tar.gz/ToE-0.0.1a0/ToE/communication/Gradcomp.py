import math
import torch
import numpy as np
from scipy.sparse import csc_matrix
import heapq


class Gradcomp(object):
    """
        A gradient compress model
    """

    def __init__(self, shape) -> None:
        super().__init__()
        '''
            A gradient compress model init method
             
        '''
        self.residuals = torch.zeros(shape)

    def upgrade_threshold(self, grad, threshold):
        # compress grad with element threshold
        grad = self.residuals.add_(grad)
        # get the index matrix by > operation
        sample_matrix = grad > threshold
        sample_matrix.mul_(grad)  
        self.residuals.sub_(sample_matrix)
        sample = csc_matrix(sample_matrix)
  
        # to send the data
        socketsend(sample)

    def upgrade_rate(self, grad, rate):
        # compress grad with compress rate
        grad = self.residuals.add_(grad)
        len_row = len(grad)
        len_col = len(grad[0])
        grad = grad.reshape(len_row*len_col)
        nb_sample = int(max(1, len(grad)*rate))
        sample, indexes = grad.topk(nb_sample)
        row, col = [], []

        # get row & col from index for built a sparse matrix
        for index in indexes:
            row.append((index // len_col).item())
            col.append((index % len_row).item())
        sample_matrix = csc_matrix((sample, (row, col)), shape=(len_row, len_row))
        self.residuals.sub_(torch.from_numpy(sample_matrix.toarray()))

        # to send the data
        #socketsend(sample_matrix)

        # return the grad data
        return sample_matrix

    def upgrade_auto(self, grad, bin_size):
        # use adacomp method
        grad = self.residuals.add_(grad)
        len_row = len(grad)
        len_col = len(grad[0])
        grad = grad.reshape(len_row * len_col)
        len_grad = len(grad)
        num_bin = math.ceil(len_grad/bin_size)

        # consider len_grad%bin_size not 0
        num_zero = num_bin * bin_size - len_grad
        if num_zero:
            for _ in range(num_zero):
                grad.appand(0)

        grad = grad.veiw(num_bin, bin_size)
        high = grad.add(grad)

        # get the max grad in each row
        grad_max = []
        for row in grad:
            grad_max.append(row.abs().max().item())

        # compare 2*grad with grad(max), send the bigger part
        sample_matrix = torch.Tensor
        i = 0
        for row in high:
            if i == 0:
                sample_matrix = row > grad_max[i]
            else:
                row_sample = row.abs() > grad_max[i]
                sample_matrix = torch.cat((sample_matrix, row_sample), 0)
        sample_matrix.mul_(grad)
        self.residuals.sub_(sample_matrix)
        sample = csc_matrix(sample_matrix)

        # to send the data
        socketsend(sample)





