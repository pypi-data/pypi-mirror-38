
import inferpy as inf
import edward as ed
import tensorflow as tf


theta = inf.models.Normal(0,1)
with inf.replicate(size=10):
    x = inf.models.Normal(0,1, dim=4)


theta = ed.mo


# batches autocomplete!!
x = inf.models.Normal(scale = [theta, 2*theta, 3, tf.constant(1, dtype="float32")], loc= [1,1] , batches=10)

x.scale




# tensorboard --logdir= ./log
with tf.Session() as sess:
    writer = tf.summary.FileWriter("./log/", sess.graph)
    sess.run(tf.global_variables_initializer())
