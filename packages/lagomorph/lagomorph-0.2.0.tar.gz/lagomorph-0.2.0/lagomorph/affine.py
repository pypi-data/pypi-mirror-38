import torch
import lagomorph_cuda

class AffineInterpFunction(torch.autograd.Function):
    """Interpolate an image using an affine transformation, parametrized by a
    separate matrix and translation vector.
    """
    @staticmethod
    def forward(ctx, I, A, T):
        ctx.save_for_backward(I, A, T)
        return lagomorph_cuda.affine_interp_forward(
            I.contiguous(),
            A.contiguous(),
            T.contiguous())
    @staticmethod
    def backward(ctx, grad_out):
        I, A, T = ctx.saved_tensors
        d_I, d_A, d_T = lagomorph_cuda.affine_interp_backward(
                grad_out.contiguous(),
                I.contiguous(),
                A.contiguous(),
                T.contiguous(),
                *ctx.needs_input_grad)
        return d_I, d_A, d_T
affine_interp = AffineInterpFunction.apply

class AffineInterp(torch.nn.Module):
    """Module wrapper for AffineInterpFunction"""
    def __init__(self):
        super(AffineInterp, self).__init__()
    def forward(self, I, A, T):
        return AffineInterpFunction.apply(I, A, T)

def det_2x2(A):
    return A[:,0,0]*A[:,1,1] - A[:,0,1]*A[:,1,0]

def invert_2x2(A):
    """Invert 2x2 matrix using simple formula in batch mode.
    This assumes the matrix is invertible and provides no further checks."""
    det = det_2x2(A)
    Ainv = torch.stack((A[:,1,1],-A[:,0,1],-A[:,1,0],A[:,0,0]), dim=1).view(-1,2,2)/det.view(-1,1,1)
    return Ainv

def minor(A, i, j):
    assert A.shape[1] == A.shape[2]
    n = A.shape[1]
    M = torch.cat((A.narrow(1, 0, i), A.narrow(1,i+1,n-i-1)), dim=1)
    M = torch.cat((M.narrow(2, 0, j), M.narrow(2,j+1,n-j-1)), dim=2)
    return M

def invert_3x3(A):
    """Invert a 3x3 matrix in batch mode. We use the formula involving
    determinants of minors here
    http://mathworld.wolfram.com/MatrixInverse.html
    """
    cofactors = torch.stack((
        det_2x2(minor(A,0,0)),
       -det_2x2(minor(A,0,1)),
        det_2x2(minor(A,0,2)),
       -det_2x2(minor(A,1,0)),
        det_2x2(minor(A,1,1)),
       -det_2x2(minor(A,1,2)),
        det_2x2(minor(A,2,0)),
       -det_2x2(minor(A,2,1)),
        det_2x2(minor(A,2,2)),
        ), dim=1).view(-1,3,3).transpose(1,2)
    # write determinant using minors matrix
    det =   cofactors[:,0,0]*A[:,0,0] \
          + cofactors[:,1,0]*A[:,0,1] \
          + cofactors[:,2,0]*A[:,0,2]
    return cofactors/det.view(-1,1,1)

def affine_inverse(A, T):
    """Invert an affine transformation.
    
    A transformation (A,T) is inverted by computing (A^{-1}, -A^{-1} T)
    """
    assert A.shape[1] == A.shape[2]
    assert A.shape[1] == T.shape[1]
    dim = A.shape[1]
    assert dim == 2 or dim == 3
    if dim == 2:
        Ainv = invert_2x2(A)
    elif dim == 3:
        Ainv = invert_3x3(A)
    Tinv = -torch.matmul(Ainv, T.unsqueeze(2)).squeeze(2)
    return (Ainv, Tinv)

def rotation_exp_map(v):
    """Convert a collection of tangent vectors to rotation matrices. This allows
    for rigid registration using unconstrained optimization by composing this
    function with the affine interpolation methods and a loss function.

    For 2D rotations, v should be a vector of angles in radians. For 3D
    rotations v should be an n-by-3 array of 3-vectors indicating the requested
    rotation in axis-angle format, in which case the conversion is done using
    the Rodrigues' rotation formula.
    https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    """
    if v.dim() == 1: # 2D case
        c = torch.cos(v).view(-1,1)
        s = torch.sin(v).view(-1,1)
        return torch.stack((c, -s, s, c), dim=1).view(-1,2,2)
    elif v.dim() == 2 and v.size(1) == 3:
        raise NotImplementedError()
    else:
        raise Exception(f"Cannot infer dimension from v shape {v.shape}")

def rigid_inverse(v, T):
    """Invert a rigid transformation using the formula
        (R(v),T)^{-1} = (R(-v), -R(-v) T)
    """
    negv = -v
    Rinv = rotation_exp_map(negv)
    Tinv = -torch.matmul(Rinv, T.unsqueeze(2)).squeeze(2)
    return (negv, Tinv)
