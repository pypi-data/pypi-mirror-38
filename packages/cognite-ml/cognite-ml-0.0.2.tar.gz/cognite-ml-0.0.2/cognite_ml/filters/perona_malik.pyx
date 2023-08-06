# distutils: language=c++

import numpy as np
cimport numpy as np
from libcpp.vector cimport vector




def __exponential(phi, z, K):
    cdef int num_points = len(z)

    for i in range(num_points):
        phi[i] = np.exp(-np.abs(z[i])**2/K)

    return 1



def __classic(phi, z, K):
    cdef int num_points = len(z)
    cdef double tmp

    for i in range(num_points):
        tmp = 1.0 + np.abs(z[i]/K)**2
        phi[i] = 1.0/tmp

    return 1


def __tukey(phi, z, K):
    cdef int num_points = len(z)

    for i in range(num_points):
        if(np.abs(z[i]) <= K):
            phi[i] = 0.5*(1.0 - np.abs(z[i]/K)**2)**2
        else:
            phi[i] = 0.0

        
    return 1


def __guo(phi, z, K):
    cdef int num_points = len(z)
    cdef double tmp
    cdef double alpha
    cdef double beta

    for i in range(num_points):
        beta = 1.0 + np.abs(z[i]/K)**2
        alpha = 2 - 2/beta
        phi[i] = 1.0 + np.abs(z[i]/K)**alpha

    return 1


def __weikert(phi, z, K):
    cdef int num_points = len(z)
    cdef double tmp
    cdef double alpha
    cdef double beta

    for i in range(num_points):
        if(np.abs(z[i]) > 0.0000000001):
            phi[i] = 1.0 - np.exp(-3.31488*K**8/np.abs(z[i])**8)
        else:
            phi[i] = 0.0

    return 1



def __solve_tri_linear(a, b, c, d, x):

    cdef int num_points = len(a)
    cdef double w

    #Forward sweep
    for i in range(1, num_points):
        w = a[i]/b[i-1]
        b[i] = b[i] - w*c[i-1]
        d[i] = d[i] - w*d[i-1] 

    #Backward sweep
    x[num_points-1] = d[num_points-1]/b[num_points-1]
    for i in range(num_points-2, -1, -1):
        x[i] = (1.0/b[i])*(d[i] - c[i]*x[i+1])

    return 1

def __perona_malik_implicit(X, t=None, smoothing_factor=1, gradient_threshold=1, method='classic'):
    cdef int num_points = len(X)

    cdef np.ndarray[np.double_t, ndim=1] Y      # The returned function
    cdef np.ndarray[np.double_t, ndim=1] phi    # Gradient stop function
    cdef np.ndarray[np.double_t, ndim=1] dx     # Gradient at i+0.5
    cdef np.ndarray[np.double_t, ndim=1] dt     # Time diff i+0.5

    cdef np.ndarray[np.double_t, ndim=1] Adia     # Matrix diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiap    # Matrix sup-diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiam    # Matrix sub-diagonal
    cdef np.ndarray[np.double_t, ndim=1] b        # Linear system RHS
    
    # Tmp storage we will need later
    cdef double DT
    cdef double gammaP
    cdef double gammaM
    
    # Let us allocate space for the vectors
    Y     = np.zeros(num_points)
    phi   = np.zeros(num_points)
    dx    = np.zeros(num_points-1)
    dt    = np.ones(num_points-1)
    Adia  = np.zeros(num_points)
    Adiap = np.zeros(num_points)
    Adiam = np.zeros(num_points)
    b     = np.zeros(num_points)

    # Now, let us calculate gradients
    if(type(t) != type(None)):
        for i in range(0, num_points-1):
            dt[i] = t[i+1]-t[i]

    for i in range(0, num_points-1):
        dx[i] = (X[i+1]-X[i])/dt[i]

    # Next, we calculate the stop gradient
    if(method=='classic'):
        __classic(phi, dx, smoothing_factor)
    elif(method=='exponential'):
        __exponential(phi, dx, smoothing_factor)
    elif(method=='tukey'):
        __tukey(phi, dx, smoothing_factor)
    elif(method=='guo'):
        __guo(phi, dx, smoothing_factor)
    elif(method=='weikert'):
        __weikert(phi, dx, smoothing_factor)

    DT = smoothing_factor
    
    #--- Now build the linear system ---
    
    # We begin with the internal points 
    cdef double theta = 1.0
    for i in range(1, num_points-1):
        gammaP = 2*DT/(dt[i]*(dt[i-1]+dt[i]))
        gammaM = 2*DT/(dt[i-1]*(dt[i-1]+dt[i]))
        Adia[i]  = (1.0 + gammaP*theta*phi[i] + gammaM*theta*phi[i-1])
        Adiap[i] = -theta*gammaP*phi[i]
        Adiam[i] = -theta*gammaM*phi[i-1]
        b[i] = X[i] + (1-theta)*(gammaP*phi[i]*(X[i+1]-X[i]) - gammaM*phi[i-1]*(X[i]-X[i-1]))

    # Then the boundary
    Adia[0] = 1.0
    Adiap[0]= -1.0
    b[0]    = 0.0
    Adia[num_points-1] = 1.0
    Adiam[num_points-1] = -1.0
    b[num_points-1] = 0.0
     
    # Next, we solve the linear system
    __solve_tri_linear(Adiam, Adia, Adiap,  b, Y)

    return Y



def __perona_malik_explicit(X, t=None, smoothing_factor=1, gradient_threshold=1, method='classic'):
    cdef int num_points = len(X)

    cdef np.ndarray[np.double_t, ndim=1] Y      # The returned function
    cdef np.ndarray[np.double_t, ndim=1] phi    # Gradient stop function
    cdef np.ndarray[np.double_t, ndim=1] dx     # Gradient at i+0.5
    cdef np.ndarray[np.double_t, ndim=1] dt     # Time diff i+0.5

    cdef np.ndarray[np.double_t, ndim=1] Adia     # Matrix diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiap    # Matrix sup-diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiam    # Matrix sub-diagonal
    cdef np.ndarray[np.double_t, ndim=1] b        # Linear system RHS
    
    # Tmp storage we will need later
    cdef double DT
    cdef double gammaP
    cdef double gammaM
    
    # Let us allocate space for the vectors
    Y     = np.zeros(num_points)
    phi   = np.zeros(num_points)
    dx    = np.zeros(num_points-1)
    dt    = np.ones(num_points-1)
    Adia  = np.zeros(num_points)
    Adiap = np.zeros(num_points)
    Adiam = np.zeros(num_points)
    b     = np.zeros(num_points)

    # Now, let us calculate gradients
    if(type(t) != type(None)):
        for i in range(0, num_points-1):
            dt[i] = t[i+1]-t[i]
    
    for i in range(0, num_points):
        Y[i] = X[i]

    cdef int k=0
    DT = smoothing_factor
    while(k<DT):

        for i in range(0, num_points-1):
            dx[i] = (Y[i+1]-Y[i])/dt[i]

        # Next, we calculate the stop gradient
        if(method=='classic'):
            __classic(phi, dx, smoothing_factor)
        elif(method=='exponential'):
            __exponential(phi, dx, smoothing_factor)
        elif(method=='tukey'):
            __tukey(phi, dx, smoothing_factor)
        elif(method=='guo'):
            __guo(phi, dx, smoothing_factor)
        elif(method=='weikert'):
            __weikert(phi, dx, smoothing_factor)

        
    
        for i in range(1, num_points-1):
            gammaP = .5/(dt[i]*(dt[i-1]+dt[i]))
            gammaM = .5/(dt[i-1]*(dt[i-1]+dt[i]))
            Y[i] = Y[i] + (gammaP*phi[i]*(Y[i+1]-Y[i]) - gammaM*phi[i-1]*(Y[i]-Y[i-1]))

        Y[0] = Y[1]
        Y[num_points-1] = Y[num_points-2]
        k = k +1

    return Y


def __perona_malik_midpoint(X, t=None, smoothing_factor=1, gradient_threshold=1, method='classic'):
    cdef int num_points = len(X)

    cdef np.ndarray[np.double_t, ndim=1] Y      # The returned function
    cdef np.ndarray[np.double_t, ndim=1] phi    # Gradient stop function
    cdef np.ndarray[np.double_t, ndim=1] phi_next    # Gradient stop function
    cdef np.ndarray[np.double_t, ndim=1] dx     # Gradient at i+0.5
    cdef np.ndarray[np.double_t, ndim=1] dx_next     # Gradient at i+0.5
    cdef np.ndarray[np.double_t, ndim=1] dt     # Time diff i+0.5

    cdef np.ndarray[np.double_t, ndim=1] Adia     # Matrix diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiap    # Matrix sup-diagonal
    cdef np.ndarray[np.double_t, ndim=1] Adiam    # Matrix sub-diagonal
    cdef np.ndarray[np.double_t, ndim=1] b        # Linear system RHS
    
    # Tmp storage we will need later
    cdef double DT
    cdef double gammaP
    cdef double gammaM
    
    # Let us allocate space for the vectors
    Y     = np.zeros(num_points)
    phi   = np.zeros(num_points)
    phi_next   = np.zeros(num_points)
    dx    = np.zeros(num_points-1)
    dx_next    = np.zeros(num_points-1)
    dt    = np.ones(num_points-1)
    Adia  = np.zeros(num_points)
    Adiap = np.zeros(num_points)
    Adiam = np.zeros(num_points)
    b     = np.zeros(num_points)

    # Now, let us calculate gradients
    if(type(t) != type(None)):
        for i in range(0, num_points-1):
            dt[i] = t[i+1]-t[i]

    Xnext = __perona_malik_implicit(X, t, smoothing_factor, gradient_threshold, method)
    
    for i in range(0, num_points-1):
        dx_next[i] = (Xnext[i+1]-Xnext[i])/dt[i]

    # Next, we calculate the stop gradient
    if(method=='classic'):
        __classic(phi, dx, smoothing_factor)
        __classic(phi_next, dx_next, smoothing_factor)
    elif(method=='exponential'):
        __exponential(phi, dx, smoothing_factor)
        __exponential(phi_next, dx_next, smoothing_factor)
    elif(method=='tukey'):
        __tukey(phi, dx, smoothing_factor)
        __tukey(phi_next, dx_next, smoothing_factor)
    elif(method=='guo'):
        __guo(phi, dx, smoothing_factor)
        __guo(phi_next, dx_next, smoothing_factor)
    elif(method=='weikert'):
        __weikert(phi, dx, smoothing_factor)
        __weikert(phi_next, dx_next, smoothing_factor)

    DT = smoothing_factor
    
    #--- Now build the linear system ---
    
    # We begin with the internal points 
    cdef double theta = 1.0
    for i in range(1, num_points-1):
        gammaP = 2*DT/(dt[i]*(dt[i-1]+dt[i]))
        gammaM = 2*DT/(dt[i-1]*(dt[i-1]+dt[i]))
        Adia[i]  = (1.0 + gammaP*theta*phi_next[i] + gammaM*theta*phi_next[i-1])
        Adiap[i] = -theta*gammaP*phi_next[i]
        Adiam[i] = -theta*gammaM*phi_next[i-1]
        b[i] = X[i] + (1-theta)*(gammaP*phi[i]*(X[i+1]-X[i]) - gammaM*phi[i-1]*(X[i]-X[i-1]))

    # Then the boundary
    Adia[0] = 1.0
    Adiap[0]= -1.0
    b[0]    = 0.0
    Adia[num_points-1] = 1.0
    Adiam[num_points-1] = -1.0
    b[num_points-1] = 0.0
     
    # Next, we solve the linear system
    __solve_tri_linear(Adiam, Adia, Adiap,  b, Y)

    return Y



def perona_malik(X, t=None, smoothing_factor=1, gradient_threshold=1, method='classic', integration='implicit'):
    """
    perona_malik(X, t=None, smoothing_factor=1, gradient_threshold=1, method='classic', integration='implicit')
    
    Perona_Malik edge preserving smoothing of a sequence or timeseries (1D) with various gradient stop functions.
       
    Args:
        :X (ndarray):                    input timeseries.

        :t (ndarray):                    input timestamps (also dictates smoothing rate, hence Epoch in ms will smooth very fast).

        :smoothing_factor (double):      The amount of smoothing (corresponds to the time of integration).

        :gradient_threshold (double):    Dictates the order of influcial gradients (no smoothing for large gradients).

        :integration (str):              explicit or implicit integration (implicit is always stable but has slightly more diffusion).
        
        :method: 
            :'classical':    phi(z) = 1/(1+(z/K)**2).

            :'exponential':  phi(z) = exp(-np.abs(z)**2/K).

            :'tukey':        phi(z) = 0.5*(1.0 - z/K)**2)**2 if z<K and 0 otherwise.

            :'guo':          beta = 1.0 + np.abs(z/K)**2.
                            alpha = 2 - 2/beta.
                            phi(z) = 1.0 + (z/K)**alpha.
            :'weikert':      phi[i] = 1.0 - exp(-3.31488*K**8/z**8).
    Returns:
         :Y: the smoothed signal
    """
    if(integration=='implicit'):
        return __perona_malik_midpoint(X, t, smoothing_factor, gradient_threshold, method)
    else:
        return __perona_malik_explicit(X, t, smoothing_factor, gradient_threshold, method)