from numpy import *

def readVertex(filename, REAL):
    x = []
    y = []
    z = []
    for line in file(filename):
        line = line.split()
        x0 = line[0]
        y0 = line[1]
        z0 = line[2]
        x.append(REAL(x0))
        y.append(REAL(y0))
        z.append(REAL(z0))

    x = array(x)
    y = array(y)
    z = array(z)
    vertex = zeros((len(x),3))
    vertex[:,0] = x
    vertex[:,1] = y
    vertex[:,2] = z
    return vertex 

def readTriangle(filename):
    triangle = []

    for line in file(filename):
        line = line.split()
        v1 = line[0]
        v2 = line[2] # v2 and v3 are flipped to match my sign convention!
        v3 = line[1]
        triangle.append([int(v1)-1,int(v2)-1,int(v3)-1])
        # -1-> python starts from 0, matlab from 1

    triangle = array(triangle)

    return triangle


def readpqr(filename, REAL):

    pos = []
    q   = []

    for line in file(filename):
        line = array(line.split())
   
        if line[0]=='ATOM':
            x = line[5]
            y = line[6]
            z = line[7]
            q.append(REAL(line[8]))
            pos.append([REAL(x),REAL(y),REAL(z)])
    
    pos = array(pos)
    q   = array(q)
    Nq  = len(q)
    return pos, q, Nq


def readcrd(filename, REAL):

    pos = []
    q   = []

    start = 0
    for line in file(filename):
        line = array(line.split())
   
        if len(line)>8:# and start==2:
            x = line[4]
            y = line[5]
            z = line[6]
            q.append(REAL(line[9]))
            pos.append([REAL(x),REAL(y),REAL(z)])
    
        '''
        if len(line)==1:
            start += 1
            if start==2:
                Nq = int(line[0])
        '''
    pos = array(pos)
    q   = array(q)
    Nq  = len(q)
    return pos, q, Nq

def readParameters(param, filename):

    val  = []
    for line in file(filename):
        line = line.split()
        val.append(line[1])

    dataType = val[0]      # Data type
    if dataType=='double':
        param.REAL = float64
    elif dataType=='float':
        param.REAL = float32

    REAL = param.REAL
    param.K         = int (val[1])      # Gauss points per element
    param.Nk        = int (val[2])      # Number of Gauss points per side 
                                        # for semi analytical integral
    param.threshold = REAL(val[3])      # L/d threshold to use analytical integrals
                                        # Over: analytical, under: quadrature
    param.BSZ       = int (val[4])      # CUDA block size
    param.restart   = int (val[5])      # Restart for GMRES
    param.tol       = REAL(val[6])      # Tolerance for GMRES
    param.max_iter  = int (val[7])      # Max number of iteration for GMRES
    param.P         = int (val[8])      # Order of Taylor expansion for treecode
    param.eps       = REAL(val[9])      # Epsilon machine
    param.NCRIT     = int (val[10])     # Max number of targets per twig box of tree
    param.theta     = REAL(val[11])     # MAC criterion for treecode
    param.GPU       = int (val[12])     # =1: use GPU, =0 no GPU

    return dataType


def readFields(filename):

    LorY    = []
    pot     = []
    E       = []
    kappa   = []
    charges = []
    qfile   = []
    Nparent = []
    parent  = []
    Nchild  = []
    child   = []

    for line in file(filename):
        line = line.split()
        if line[0]=='FIELD':
            LorY.append(line[1])
            pot.append(line[2])
            E.append(line[3])
            kappa.append(line[4])
            charges.append(line[5])
            qfile.append(line[6])
            Nparent.append(line[7])
            parent.append(line[8])
            Nchild.append(line[9])
            for i in range(int(Nchild[-1])):
                child.append(line[10+i])

    return LorY, pot, E, kappa, charges, qfile, Nparent, parent, Nchild, child

def readSurf(filename):

    files = []
    for line in file(filename):
        line = line.split()
        if line[0]=='FILE':
            files.append(line[1])

    return files