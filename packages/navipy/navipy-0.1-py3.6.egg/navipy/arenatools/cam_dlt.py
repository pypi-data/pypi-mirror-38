import pandas as pd
import numpy as np


def dlt_reconstruct(coeff, campts, z=None):
    """
    This function reconstructs the 3D position of a coordinate based on a set
    of DLT coefficients and [u,v] pixel coordinates from 2 or more cameras

   :param coeff: - 11 DLT coefficients for all n cameras, [11,n] array
   :param campts: - [u,v] pixel coordinates from all n cameras over f frames
   :param z: the z coordinate of all points for reconstruction \
from a single camera
   :returns: xyz - the xyz location in each frame, an [f,3] array\
rmse - the root mean square error for each xyz point, and [f,1] array,\
units are [u,v] i.e. camera coordinates or pixels
    """
    # number of cameras
    ncams = campts.columns.levels[0].shape[0]
    if (ncams == 1) and (z is None):
        raise NameError('reconstruction from a single camera require z')

    # setup output variables
    xyz = pd.DataFrame(index=campts.index, columns=[
                       'x', 'y', 'z'], dtype=float)
    rmse = pd.Series(index=campts.index)
    # process each frame
    for ii, frame_i in enumerate(campts.index):
        # get a list of cameras with non-NaN [u,v]
        row = campts.loc[frame_i, :].unstack()
        validcam = row.dropna(how='any')
        cdx = validcam.index
        if validcam.shape[0] >= 2:
            # Two or more cameras
            u = campts.loc[frame_i, cdx].swaplevel().u
            v = campts.loc[frame_i, cdx].swaplevel().v

            # initialize least-square solution matrices
            m1 = np.zeros((cdx.shape[0]*2, 3))
            m2 = np.zeros((cdx.shape[0]*2, 1))

            m1[0: cdx.size*2: 2, 0] = u*coeff.loc[8, cdx]-coeff.loc[0, cdx]
            m1[0: cdx.size*2: 2, 1] = u*coeff.loc[9, cdx]-coeff.loc[1, cdx]
            m1[0: cdx.size*2: 2, 2] = u*coeff.loc[10, cdx]-coeff.loc[2, cdx]
            m1[1: cdx.size*2: 2, 0] = v*coeff.loc[8, cdx]-coeff.loc[4, cdx]
            m1[1: cdx.size*2: 2, 1] = v*coeff.loc[9, cdx]-coeff.loc[5, cdx]
            m1[1: cdx.size*2: 2, 2] = v*coeff.loc[10, cdx]-coeff.loc[6, cdx]
            m2[0: cdx.size*2: 2, 0] = coeff.loc[3, cdx]-u
            m2[1: cdx.size*2: 2, 0] = coeff.loc[7, cdx]-v

            # get the least squares solution to the reconstruction
            xyz.loc[frame_i, ['x', 'y', 'z']] = \
                np.linalg.lstsq(m1, m2, rcond=None)[0][:, 0]

            # compute ideal [u,v] for each camera
            uv = m1.dot(xyz.loc[frame_i, ['x', 'y', 'z']].transpose())
            uv = uv[:, np.newaxis]  # because m2 has size n,1
            # compute the number of degrees of freedom in the reconstruction
            dof = m2.size-3

            # estimate the root mean square reconstruction error
            rmse.loc[frame_i] = (np.sum((m2-uv) ** 2)/dof) ** 0.5

        elif (validcam.shape[0] == 1) and (z is not None):
            # http://www.kwon3d.com/theory/dlt/dlt.html
            # equation 19 with z = constant
            # the term with z can be move to right side
            # then equation 21 can be solved as follow:
            u = campts.loc[frame_i, cdx].unstack().u
            v = campts.loc[frame_i, cdx].unstack().v

            # initialize least-square solution matrices
            m1 = np.zeros((cdx.shape[0]*2, 2))
            m2 = np.zeros((cdx.shape[0]*2, 1))

            m1[0: cdx.size*2: 2, 0] = u*coeff.loc[8, cdx]-coeff.loc[0, cdx]
            m1[0: cdx.size*2: 2, 1] = u*coeff.loc[9, cdx]-coeff.loc[1, cdx]
            m1[1: cdx.size*2: 2, 0] = v*coeff.loc[8, cdx]-coeff.loc[4, cdx]
            m1[1: cdx.size*2: 2, 1] = v*coeff.loc[9, cdx]-coeff.loc[5, cdx]
            m2[0: cdx.size*2: 2, 0] = coeff.loc[3, cdx]-u
            m2[1: cdx.size*2: 2, 0] = coeff.loc[7, cdx]-v

            m2[0: cdx.size*2: 2, 0] -= \
                (u*coeff.loc[10, cdx] - coeff.loc[2, cdx])*z.loc[frame_i]
            m2[1: cdx.size*2: 2, 0] -= \
                (v*coeff.loc[10, cdx] - coeff.loc[6, cdx])*z.loc[frame_i]

            # get the least squares solution to the reconstruction
            xyz.loc[frame_i, ['x', 'y']] = \
                np.squeeze(np.linalg.lstsq(m1, m2, rcond=None)[0])
            xyz.loc[frame_i, 'z'] = z.loc[frame_i]

            # compute ideal [u,v] for each camera
            uv = m1.dot(xyz.loc[frame_i, ['x', 'y']].transpose())
            uv = uv[:, np.newaxis]  # because m2 has size n,1
            # compute the number of degrees of freedom in the reconstruction
            dof = m2.size-3

            # estimate the root mean square reconstruction error
            rmse.loc[frame_i] = (np.sum((m2-uv) ** 2)/dof) ** 0.5
    return xyz, rmse


def dlt_inverse(coeff, frames):
    """
    This function reconstructs the pixel coordinates of a 3D coordinate as
    seen by the camera specificed by DLT coefficients c

   :param coeff: - 11 DLT coefficients for the camera, [11,1] array
   :param frames: - [x,y,z] coordinates over f frames,[f,3] array
   :returns: uv - pixel coordinates in each frame, [f,2] array
    """
    # write the matrix solution out longhand for vector operation over
    # all pointsat once
    uv = np.zeros((frames.shape[0], 2))
    frames = frames.loc[:, ['x', 'y', 'z']].values

    normalisation = frames[:, 0]*coeff[8] + \
        frames[:, 1]*coeff[9]+frames[:, 2]*coeff[10] + 1
    uv[:, 0] = frames[:, 0]*coeff[0]+frames[:, 1] * \
        coeff[1]+frames[:, 2]*coeff[2]+coeff[3]
    uv[:, 1] = frames[:, 0]*coeff[4]+frames[:, 1] * \
        coeff[5]+frames[:, 2]*coeff[6]+coeff[7]
    uv[:, 0] /= normalisation
    uv[:, 1] /= normalisation
    return uv


def dlt_compute_coeffs(frames, campts):
    """
    A basic implementation of 11 parameters DLT

    : param frames: an array of x, y, z calibration point coordinates
    : param campts: an array of u, v pixel coordinates from the camera
    : returns: dlt coefficients and root mean square error

    Notes: frame and camera points must have the same number of rows and at \
least contains six rows. Also the frame points must not all lie within a \
single plane.
    """

    # remove NaNs
    valid_idx = frames.dropna(how='any').index
    valid_idx = campts.loc[valid_idx, :].dropna(how='any').index

    # valid df
    vframes = frames.loc[valid_idx, :]
    vcampts = campts.loc[valid_idx, :]

    # re arange the frame matrix to facilitate the linear least
    # sqaures solution
    matrix = np.zeros((vframes.shape[0]*2, 11))  # 11 for the dlt
    for num_i, index_i in enumerate(vframes.index):
        matrix[2*num_i, 0:3] = vframes.loc[index_i, ['x', 'y', 'z']]
        matrix[2*num_i+1, 4:7] = vframes.loc[index_i, ['x', 'y', 'z']]
        matrix[2*num_i, 3] = 1
        matrix[2*num_i+1, 7] = 1
        matrix[2*num_i, 8:11] = \
            vframes.loc[index_i, ['x', 'y', 'z']]*(-vcampts.loc[index_i, 'u'])
        matrix[2*num_i+1, 8:11] = \
            vframes.loc[index_i, ['x', 'y', 'z']]*(-vcampts.loc[index_i, 'v'])

    # re argen the campts array for the linear solution
    vcampts_f = np.reshape(np.flipud(np.rot90(vcampts)), vcampts.size, 1)
    print(vcampts_f.shape)
    print(matrix.shape)
    # get the linear solution the 11 parameters
    coeff = np.linalg.lstsq(matrix, vcampts_f, rcond=None)[0]
    # compute the position of the frame in u,v coordinates given the linear
    # solution from the previous line

    matrix_uv = dlt_inverse(coeff, vframes)

    # compute the rmse between the ideal frame u,v and the
    # recorded frame u,v
    rmse = np.sqrt(np.mean(np.sum((matrix_uv-vcampts)**2)))
    return coeff, rmse
