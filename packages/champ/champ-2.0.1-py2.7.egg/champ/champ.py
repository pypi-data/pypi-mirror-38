from pyhull import halfspace as hs
from .plot_domains import plot_2d_domains
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import uniform


def create_half_space_from_partitions():
    '''

    :return:
    '''
    #TODO
    return

def create_halfspaces_from_array(coeff_array,max_pt=None,min_pt=(0,0,0)):
    '''
    :param coeff_array: list of coefficients for each partition to be considered.  Should be an array
        [ [ A_0 , P_0 , C_0 ],
           ... ,
          [ A_n , P_n , C_n ]
        ]

    Where each row represents the coefficients for a particular partition.
    If Single Layer network, omit C_i's.
    :param max_pt: Upper bound for the domains (in the xy plane).  This will restrict the
    convex hull to be within a reasonable range of gamma/omega (such as the range of parameters
    originally searched using Louvain).
    :param min_pt: Lower bound for interesections (origin)
    :return list of halfspaces with 4 boundary halfspaces appended to the end.
    '''
    if coeff_array.shape[1]==2:
        singlelayer=True

    halfspaces=[]
    for i in np.arange(coeff_array.shape[0]):
        cconst = coeff_array[i, 0]
        cgamma = coeff_array[i, 1]
        if not singlelayer:
            comega = coeff_array[i, 2]

        if singlelayer:
            nv=np.array([cgamma, 1.0])
            pt = np.array([0 , cconst])
        else:
            nv=np.array([cgamma, -1 * comega, 1.0])
            pt = np.array([0, 0, cconst])

        nv = nv/np.linalg.norm(nv)
        off = np.dot(nv, pt)

        halfspace = hs.Halfspace(-1.0 * nv, off)
        halfspaces.append(halfspace)


    #Create Boundary Halfspaces - These will always be included in the convex hull and need to be removed
    if singlelayer:
        #origin boundaries
        halfspaces.extend([hs.Halfspace(normal=(0, -1.0, 0), offset=0), hs.Halfspace(normal=(-1.0, 0, 0), offset=0)])
        #max boundaries
    else:
        halfspaces.extend([hs.Halfspace(normal=(0, -1.0, 0), offset=0), hs.Halfspace(normal=(-1.0, 0, 0), offset=0)])

    return halfspaces

def get_interior_point(hs_list):
    '''
    Find interior point to calculate intersections
    :param hs_list: list of halfspaces
    :return: interior point of intersections at (0+.001,0+.001,max(A_ij)) the
    maximum modularity value of any of the partitions at 0,0 needed to calculate
    interior intersection.
    '''

    z_vals=[ -1.0*hs.offset/hs.normal[-1] for hs in hs_list]
    #take a small step into interior from 1st plane.
    return np.array([0,0,np.max(z_vals)]) + np.array([.0001,.0001,.0001])

def calculate_coefficient(com_vec,adj_matrix):
    '''
    For a given connection matrix and set of community labels, calculate the coeffcient
    for plane/line associated with that connectivity matrix

    :param com_vec: list or vector with community membership for each element of network
    ordered the same as the rows/col of adj_matrix
    :param adj_matrix: adjacency matrix for connections to calculate coefficients for
    (i.e. A_ij, P_ij, C_ij, etc..) ordered the same as com_vec
    :return:
    '''

    com_inddict = {}

    allcoms = sorted(list(set(com_vec)))
    assert com_vec.shape[0] == adj_matrix.shape[0]
    sumA = 0

    # store indices for each community together in dict
    for i, val in enumerate(com_vec):
        com_inddict[val] = com_inddict.get(val, []) + [i]

    # convert indices to np_array
    for k, val in com_inddict.items():
        com_inddict[k] = np.array(val)

    for com in allcoms:
        cind = com_inddict[com]
        if cind.shape[0] == 1:  # throws type error if try to index with scalar
            sumA += np.sum(adj_matrix[cind, cind])
        else:
            sumA += np.sum(adj_matrix[np.ix_(cind, cind)])

    return sumA



def find_intersection(halfspaces,maxpt=None,minpt=(0,0)):
    '''

    :param halfspaces:
    :param maxpt:
    :param minpt:
    :return:
    '''
    interior_pt=get_interior_point(halfspaces)
    hs_inter = hs.HalfspaceIntersection(halfspaces, interior_pt)  # Find boundary intersection of half spaces
    ind_2_domain = {}

    non_inf_vert = np.array([v for v in hs_inter.vertices if v[0] != np.inf])
    mx = np.max(non_inf_vert,axis=0)
    # mx = multipartition_prune_rays.get_max_point(non_inf_vert).array + np.array([5, 5, 0])
    rep_verts = [v if v[0] != np.inf else mx for v in hs_inter.vertices]
    for i, vlist in enumerate(hs_inter.facets_by_halfspace):
        chs = hs_inter.halfspaces[i]
        if len(vlist) == 0:
            continue

        # these are the boundary planes appended on end
        if not i < len(hs_inter.facets_by_halfspace) - 4 :
            continue

        #use non-inf vertices to return
        ind_2_domain[i] = [rep_verts[i] for v in vlist]
    return ind_2_domain

def _random_plane():
    normal = np.array([uniform(-0.5, 0.5), uniform(-0.5, 0.5), -1])
    normal /= np.linalg.norm(normal)
    min_offset = -min(0,
                      normal[0],
                      normal[1],
                      normal[0] + normal[1])
    max_offset = -max(normal[2],
                      normal[2] + normal[0],
                      normal[2] + normal[1],
                      normal[2] + normal[0] + normal[1])
    # the 0.25 and 0.75 factors here just force more intersections
    offset = uniform(0.75 * min_offset + 0.25 * max_offset,
                     0.25 * min_offset + 0.75 * max_offset)
    return hs.Halfspace(normal, offset)

def get_random_halfspaces(n=100):
    '''Generate random halfspaces for testing
    :param n: number of halfspaces to return (default=100)
    '''
    test_hs=[]
    for _ in range(n):
        test_hs.append(_random_plane())

    return test_hs