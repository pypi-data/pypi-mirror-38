import edward as ed
import inferpy as inf
from inferpy.models import Normal
import numpy as np

import tensorflow as tf

d, N =  5, 1000

with inf.replicate(size=N):
    x = inf.models.MultivariateNormalDiag(
        loc=[1., -1],
        scale_diag=[1, 2.],dim=5
    )

with inf.replicate(size=N):
    x = inf.models.Normal(0,1,dim=d)



x = inf.models.MultivariateNormalDiag(
    loc=[1., -1],
    scale_diag=[1, 2.],dim=[5,10]
)



x = inf.models.MultivariateNormalDiag(
    loc=[1., -1],
    scale_diag=[1, 2.], dim=[100,100], batch = 5
)



x.event_shape
x.dim
x.batches

x.shape

x.loc.shape


with tf.Session() as sess:
    print(x.dist.shape)




