import inferpy as inf



# NO crea un replicate



with inf.replicate(size=10):
    x = inf.models.Normal(0,1,dim=[5,4])        # batches = 50


inf.models.Normal(0,1,dim=[5,4]).shape   # batches = 5