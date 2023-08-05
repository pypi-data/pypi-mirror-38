u"""Neural Causation Coefficient.

Author : David Lopez-Paz
Ref :  Lopez-Paz, D. and Nishihara, R. and Chintala, S. and Schölkopf, B. and Bottou, L.,
    "Discovering Causal Signals in Images", CVPR 2017.
"""

from sklearn.preprocessing import scale
import numpy as np
import torch as th
from torch.autograd import Variable
from .model import PairwiseModel
from tqdm import trange


class NCC_model(th.nn.Module):
    """NCC model structure."""

    def __init__(self, n_hiddens=20):
        """Init the NCC structure with the number of hidden units.

        :param n_hiddens: Number of hidden units
        :type n_hiddens: int
        """
        super(NCC_model, self).__init__()
        self.c1 = th.nn.Conv1d(2, n_hiddens, 1)
        self.c2 = th.nn.Conv1d(n_hiddens, n_hiddens, 1)
        self.batch_norm = th.nn.BatchNorm1d(n_hiddens, affine=False)
        self.l1 = th.nn.Linear(n_hiddens, n_hiddens)
        self.l2 = th.nn.Linear(n_hiddens, 1)

    def forward(self, x):
        """Passing data through the network.

        :param x: 2d tensor containing both (x,y) Variables
        :return: output of the net
        """
        if x.dim()==2:
            x.unsqueeze_(2)
        sig = th.nn.Sigmoid()
        act = th.nn.ReLU()
        out1 = act(self.c1(x))
        out2 = act(self.c2(out1)).squeeze(2)
        out3 = self.l2(self.l1(self.batch_norm(out2).mean(dim=0)))
        return sig(out3)


class NCC(PairwiseModel):
    u"""Neural Causation Coefficient.

    Infer causal relationships between pairs of variables
    Ref :  Lopez-Paz, D. and Nishihara, R. and Chintala, S. and Schölkopf, B. and Bottou, L.,
    "Discovering Causal Signals in Images", CVPR 2017.

    """

    def __init__(self):
        super(NCC, self).__init__()
        self.model = None

    def fit(self, x_tr, y_tr, epochs=200):
        """Fit the NCC model.

        :param x_tr: CEPC-format DataFrame containing pairs of variables
        :param y_tr: array containing targets
        """
        self.model = NCC_model()
        opt = th.optim.Adam(self.model.parameters())
        criterion = th.nn.BCELoss()
        y = th.Tensor(y_tr.values)
        if th.cuda.is_available():
            self.model = self.model.cuda()
            y = y.cuda()
            y_cpu = y.cpu()
        dataset = []
        for i, (idx, row) in enumerate(x_tr.iterrows()):

            a = row['A'].reshape((len(row['A']), 1))
            b = row['B'].reshape((len(row['B']), 1))
            m = np.hstack((a, b))
            m = m.astype('float32')
            m = Variable(th.from_numpy(m))
            dataset.append(m)
        if th.cuda.is_available():
            dataset = [m.cuda() for m in dataset]
        acc = [0]
        with trange(epochs) as t:
            for epoch in t:
                for i, m in enumerate(dataset):
                    opt.zero_grad()
                    out = self.model(m)
                    loss = criterion(out, y[i])
                    loss.backward()
                    if not i:
                        t.set_postfix(loss=loss.item(), acc=np.mean(acc))
                        acc = []

                    else:
                        val = 1 if out > .5 else 0
                        if th.cuda.is_available():
                            acc.append(np.abs(y_cpu[i] - val))
                        else:
                            acc.append(np.abs(y[i] - val))
                    # NOTE : optim is called at each sample ; might want to change
                    opt.step()

    def predict_proba(self, a, b):
        """Infer causal directions using the trained NCC pairwise model.

        :param a: Variable 1
        :param b: Variable 2
        :return: probability (Value : 1 if a->b and -1 if b->a)
        :rtype: float
        """
        if self.model is None:
            print('Model has to be trained before doing any predictions')
            raise ValueError
        if len(np.array(a).shape) == 1:
            a = np.array(a).reshape((-1, 1))
            b = np.array(b).reshape((-1, 1))
        m = np.hstack((a, b))
        m = scale(m)
        m = m.astype('float32')
        m = Variable(th.from_numpy(m))

        if th.cuda.is_available():
            m = m.cuda()

        return self.model(m)
