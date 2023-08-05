#pythran export cc(float64[])
def cc(c):
    import numpy as np
    return np.cos(c)
