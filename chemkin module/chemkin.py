import numpy as np
from functools import reduce

def toy_prog_rate(v, x, k):
    """ This function calculates the progress rate of a reaction of the following form:
                Va*A+Vb*B -> Vc*C
    It taken in the vectors v and x in the order [[A],[B],[C]].
    -------
    Args: v,x; vectors, numpy arrays (or lists) of the same length
          k; float, the k constant in the reaction of elementary equations.
    -------
    Returns: float; the progress rate of the reaction, w.
    -------
    Raises: ValueError if the lengths of v and x are not both 3.
            TypeError if k cannot be converted to a float
    =========
    Example:
    >>> toy_prog_rate([2.,1.,1.], [1.,2.,3.], 10)
    20.0
    """
    if len(v) != 3 or len(x) !=3:
        raise ValueError('The lists must both be of length 3, not v, {0} and x, {1}'.format(len(v),len(x)))
    try:
        v = [float(i) for i in v]
        x = [float(i) for i in x]
        k = float(k)
    except ValueError:
        raise ValueError('One of the types in v, x, or k is not convertable to a float.')
    w = k * x[0]**v[0] * x[1]**v[1]
    return w


def progress_rate(vprime, v2prime, x, k):
    """ This function calculates the progress rate of a reaction of the following form:
                V'11*A + V'21*B -> V''31*C
            V'12*A + V'32*C -> V''22*B + V''32*C
    It taken in the vectors v', v'' and x in the order [[A],[B],[C]].
    -------
    Args: v',v'', matrices, numpy arrays of form mxn where m is the number of reactants and n is number of equations.
          x; vector, numpy array (or list of lists) of length equal to the number of reactants in the system of equations.
          k; float or list of length n (number of equations), the k constant in the reaction of elementary equations.
    -------
    Returns: list of floats; the progress rate of the reaction for each equation
    -------
    Raises: ValueError if the shapes of the v matrices are not equal and if the x vector is not mx1
    =======
    Examples:
    >>> vp = np.array([[1.,2.],[2.,0.],[0.,2.]])
    >>> vpp = np.array([[0.,0.],[0.,1.],[2.,1.]])
    >>> x = np.array([[1.],[2.],[1.]])
    >>> progress_rate(vp,vpp,x,10)
    [40.0, 10.0]
    """
    if vprime.shape==v2prime.shape:
        m,n = vprime.shape
    else:
        raise ValueError('The vprime and vdprime matrices must be the same size.')
    if x.shape != (m,1):
        raise ValueError('The x vector must be {0} given your v matrices, but it was {1}'.format((m,1),x.shape))
    if not isinstance(k,(float,int)):
        if len(k) != n:
            raise ValueError('The coefficient k must either be a list of length {0} or a float, not {1}'.format(n,k))
    w = []
    if isinstance(k,(float,int)):
        for j in range(n):
            w.append(k*reduce((lambda x,y: x*y),np.power(x.T[0],vprime.T[j])))
    else:
        for j in range(n):
            w.append(k[j]*reduce((lambda x,y: x*y),np.power(x.T[0],vprime.T[j])))
    return w


def reaction_rate(vprime, v2prime, x, k):
    """ This function calculates the reaction rate of a reaction of the following form:
                V'11*A + V'21*B -> V''31*C
                V'32*C -> V'12*A + V''22*B
    It taken in the vectors v', v'' and x in the order [[A],[B],[C]].
    -------
    Args: v',v'', matrices, numpy arrays of form mxn where m is the number of reactants and n is number of equations.
          x; vector, numpy array (or list) of length equal to the number of reactants in the system of equations.
          k; float, the k constant in the reaction of elementary equations.
    -------
    Returns: vector of floats; the reaction rate for each equation
    -------
    Raises: ValueError when vprime and v2prime are not the same shape or x is not (mx1)
    =======
    Example:
    >>> vp = np.array([[1.,0.],[2.,0.],[0.,2.]])
    >>> vpp = np.array([[0.,1.],[0.,2.],[1.,0.]])
    >>> x = np.array([[1.],[2.],[1.]])
    >>> reaction_rate(vp,vpp,x,10)
    [-30.0, -60.0, 20.0]

    """
    if vprime.shape==v2prime.shape:
        m,n = vprime.shape
    else:
        raise ValueError('The vprime and vdprime matrices must be the same size.')
    if x.shape != (m,1):
        raise ValueError('The x vector must be {0} given your v matrices, but it was {1}'.format((m,1),x.shape))
    w = progress_rate(vprime,v2prime,x,k)
    v = v2prime - vprime
    f = []
    for i in range(m):
        f.append(sum([v[i][j]*w[j] for j in range(n)]))
    return f
