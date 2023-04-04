import numpy as np

# some constants for coord math (mostly premature optimization)
pi_2 = np.pi / 2.
to_deg = 180. / np.pi
to_rad = np.pi / 180.
id_2d = np.array([[1, 0], [0, 1]])


class Sym:
    def __init__(self, desc, pairs, weight=1.):
        self.desc = desc
        self.pairs = np.array(pairs)
        self.weight = weight
        self.weight_tot = len(self.pairs) * weight

    def get_left(self):
        return self.pairs[:, 0]

    def get_right(self):
        return self.pairs[:, 1]


default_syms = [
    # NOTE: I haven't tested this a lot, but I don't expect
    #       it will be a great/reliable way to address tilt...
    # Sym(
    #     'cheeks',
    #     ((i, 16 - i) for i in range(8)),
    #     .5,
    # ),
    # NOTE: The corners of the eyes seem good-enough on their own
    #       for the purpose of normalizing yaw
    Sym(
        'canthi',
        [
            [36, 45],
            [39, 42],
        ],
        4.  # higher weight for canthi
    ),
    # TODO: delete?
    # NOTE: This is probably not worth keeping, especially
    #       since its weight is so low...
    Sym(
        'eyelids',
        [
            # [36, 45], # already included in eyes corners
            [37, 44],
            [38, 43],
            # [39, 42], # already included in eyes corners
            [40, 47],
            [41, 46],
        ],
        .5,  # due to expressions (e.g. squinting)
    ),
]


def _get_yaw(coords, sym):
    '''
    This function calculates the angle offset based on the given
    coordinates and expected symmetric point pairs.

    Parameters
    ----------
    coords : number with shape(landmarks,dimensions)
        the landmark coordinates to check.
    sym : Sym
        The basis of symmetry (essentially a combination of point pairs).

    Returns
    -------
    angle : float
        The estimated angle of rotation (in radians).

    '''
    # calculate diffs per pair
    left, right = np.squeeze(np.split(coords[sym.pairs.T], 2))
    xx, yy = np.squeeze(np.split((right - left).T, 2))
    yy = -yy  # neg y because image y starts at top
    xx = xx.astype(np.float64)
    yy = yy.astype(np.float64)

    hypots = np.hypot(xx, yy)
    weight_tot = np.sum(hypots)  # use pair distance as weight

    x = np.sum(xx * hypots) / weight_tot
    y = np.sum(yy * hypots) / weight_tot

    # calculate angle
    y_neg = np.sign(y) == -1
    if x == 0:
        angle = -pi_2 if y_neg else pi_2
    else:
        angle = np.arctan(y / x)
        x_neg = np.sign(x) == -1
        if x_neg:
            if y_neg:
                angle -= np.pi
            else:
                angle += np.pi

    return angle


def get_angle(coords, syms=default_syms, deg=False):
    angles = []
    weights = []
    for sym in syms:
        angle = _get_yaw(coords, sym)
        angles.append(angle)
        weights.append(sym.weight_tot)
    angles = np.array(angles)
    weights = np.array(weights)
    angle = np.sum(angles * weights) / np.sum(weights)
    if deg:
        return to_deg * angle
    else:
        return angle


def rotate(row, x_cols, y_cols):
    coords = np.stack([row[cols].values for cols in [x_cols, y_cols]], 1)
    angle = get_angle(coords)
    cos = np.cos(angle)
    sin = np.sin(angle)
    rotx = np.array([[cos, sin], [-sin, cos]])

    # perform rotation
    coords = coords @ rotx  # apply rotation matrix
    row[x_cols] = coords[:, 0]
    row[y_cols] = coords[:, 1]
    return row
