"""

Main module for grid generation in fractured domains in 2d and 3d.

The module serves as the only neccessary entry point to create the grid. It
will therefore wrap interface to different mesh generators, pass options to the
generators etc.

"""
import numpy as np
import scipy.sparse as sps

from gridding.fractured import grid_2d, grid_3d
from gridding.grid_bucket import GridBucket
from utils import setmembership


def create_grid(fracs, domain, **kwargs):
    """
    Main function for grid generation.

    Parameters:
        fracs (list of np.ndarray): One list item for each fracture. Each item
            consist of a (nd x n) array describing fracture vertices. The
            fractures may be intersecting.
        domain (dict): Domain specification, determined by
        **kwargs: May contain fracture tags, options for gridding, etc.

    """

    ndim = fracs[0].shape[0]

    # Call relevant method, depending on grid dimensions
    # Note: If we ever develop interfaces to grid generators other than gmsh,
    # this should not be visible here, but rather in the respective
    # nd.create_grid methods.
    if ndim == 2:
        # This will fail, either change method parameters, or process data.
        f_lines = np.reshape(np.arange(2 * len(fracs)), (2, -1), order='F')
        f_pts = np.hstack(fracs)
        frac_dic = {'points': f_pts, 'edges': f_lines}
        grids = grid_2d.create_grid(frac_dic, domain, **kwargs)
    elif ndim == 3:
        grids = grid_3d.create_grid(fracs, domain, **kwargs)

    return assemble_in_bucket(grids)


def assemble_in_bucket(grids):
    bucket = GridBucket()
    [bucket.add_nodes(g_d) for g_d in grids]
    for dim in range(len(grids) - 1):
        for hg in grids[dim]:
            # Sort the face nodes for simple comparison. np.sort returns a copy
            # of the list,
            fn_loc = hg.face_nodes.indices.reshape((hg.dim, hg.num_faces),
                                                   order='F')
            # Convert to global numbering
            fn = hg.global_point_ind[fn_loc]
            fn = np.sort(fn, axis=0)

            for lg in grids[dim + 1]:
                cell_2_face, cell = obtain_interdim_mappings(lg, fn)
                face_cells = sps.csc_matrix(
                    (np.array([True] * cell.size), (cell, cell_2_face)),
                    (lg.num_cells, hg.num_faces))

                # This if may be unnecessary, but better safe than sorry.
                if face_cells.size > 0:
                    bucket.add_edge([hg, lg], face_cells)

    return bucket


def obtain_interdim_mappings(lg, fn):
    # Next, find mappings between faces in one dimension and cells in the lower
    # dimension
    if lg.dim > 0:
        cn_loc = lg.cell_nodes().indices.reshape((lg.dim + 1,
                                                  lg.num_cells),
                                                 order='F')
        cn = lg.global_point_ind[cn_loc]
        cn = np.sort(cn, axis=0)
    else:
        cn = np.array([lg.global_point_ind])
        # We also know that the higher-dimensional grid has faces
        # of a single node. This sometimes fails, so enforce it.
        fn = fn.ravel()

    is_mem, cell_2_face = setmembership.ismember_rows(cn, fn)

    # An element in cell_2_face gives, for all cells in the
    # lower-dimensional grid, the index of the corresponding face
    # in the higher-dimensional structure.

    low_dim_cell = np.where(is_mem)[0]
    return cell_2_face, low_dim_cell
