import torch
from torch.legacy import nn

class CrossEntropyCriterion(nn.Criterion):

    def __init__(self, weights=None):
        super(CrossEntropyCriterion, self).__init__()
        self.lsm = nn.LogSoftMax()
        self.nll = nn.ClassNLLCriterion(weights)

    def updateOutput(self, input, target):
        input = input.squeeze()
        target = target.squeeze()
        self.lsm.updateOutput(input)
        self.nll.updateOutput(self.lsm.output, target)
        self.output = self.nll.output
        return self.output

    def updateGradInput(self, input, target):
        size = input.size()
        input = input.squeeze()
        target = target.squeeze()
        self.nll.updateGradInput(self.lsm.output, target)
        self.lsm.updateGradInput(input, self.nll.gradInput)
        self.gradInput.view(self.lsm.gradInput, size)
        return self.gradInput

