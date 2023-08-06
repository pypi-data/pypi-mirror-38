import inferpy as inf
import edward as ed
import tensorflow as tf




from inferpy.models.params import *


d=4
N=10
K=3

p = [0.2, 0.7, 0.1]
p = inf.models.Dirichlet(np.ones(K))


inf.models.Normal(0,1, dim=3).shape  # [3]
inf.models.Normal(0,1, batches=10).shape  # [10,1]
inf.models.Normal(0,1, batches=[5,2]).shape  # [10,1]
inf.models.Normal(0,1, dim=3, batches=10).shape  # [10,3]
inf.models.Normal(0,1, dim=3, batches=[10,5]).shape  # [50,3]


with inf.replicate(size=2):
    print(inf.models.Normal(0, 1, dim=3, batches=[10, 5]).shape)  # [100,3]


inf.models.Normal(0,1, dim=[1,2]).shape  # error

