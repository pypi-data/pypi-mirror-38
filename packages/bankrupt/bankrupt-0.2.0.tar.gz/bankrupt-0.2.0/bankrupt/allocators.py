import doctest


def cea(estate, d):
    """ Constrained Equal Award.

    :param estate: nonnegative int or float.
    :param d: claims of the claimants (list or tuple).
    :return: allocation vector (list).

    >>> d = [100, 300, 200]
    >>> cea(120, d)
    [40.0, 40.0, 40.0]
    >>> cea(330, d)
    [100, 115.0, 115.0]
    >>> cea(520, d)
    [100, 220.0, 200]
    >>> cea(800, d)
    [100, 300, 200]
    >>> cea(0, d)
    [0.0, 0.0, 0.0]
    >>> d = [200, 200, 200]
    >>> cea(300, d)
    [100.0, 100.0, 100.0]
    """
    k = len(d)
    x = [0] * k
    if k == 0:
        return x

    # sort d and remember the order
    sc = __SortClaims(d)
    d_sorted = sc.sort()
    # allocate w.r.t. d_sorted
    for i in range(k):
        x[i] = d_sorted[i] if (k-i) * d_sorted[i] <= estate else estate / (k-i)
        estate -= x[i]
    # recover the order
    return sc.reorder(x)


class __SortClaims(object):

    def __init__(self, array):
        self.array = array
        self.len = len(array)
        self.sorted = []
        self.sorted_indices = []

    def sort(self):
        array_dict = dict(zip(range(self.len), self.array))
        sorted_things = list(zip(*sorted(array_dict.items(), key=lambda item: item[1])))
        self.sorted_indices = sorted_things[0]
        self.sorted = sorted_things[1]
        return self.sorted

    def reorder(self, x):
        """ Reorder allocation vector x such that x[i] matches array[i].
        """
        y = [0] * self.len
        for i in range(self.len):
            y[self.sorted_indices[i]] = x[i]
        return y


def cea_i(estate, d):
    """ Constrained Equal Award.
    Note: input and output take integer values.
    Round down floats if there exist.

    :param estate: nonnegative int.
    :param d: claims of the claimants (list or tuple of integers).
    :return: allocation vector (list of integers).

    >>> d = [100.5, 300, 200]
    >>> cea_i(121, d)
    [40, 41, 40]
    >>> cea_i(331, d)
    [100, 116, 115]
    >>> cea_i(521, d)
    [100, 221, 200]
    >>> cea_i(800, d)
    [100, 300, 200]
    >>> cea_i(0, d)
    [0, 0, 0]
    >>> cea_i(1, d)
    [0, 1, 0]
    """
    k = len(d)
    x = [0] * k
    if k == 0:
        return x
    estate = int(estate)

    # sort d and remember the order
    sc = __SortClaims(d)
    d_sorted = sc.sort()

    for i in range(k):
        di = int(d_sorted[i])
        x[i] = di if (k-i) * di <= estate else estate // (k-i)
        x[i] = int(x[i])
        estate -= x[i]

    # recover the order
    return sc.reorder(x)


def wcea(estate_w, d, w):
    """ Weighted Constrained Equal Award.

    :param estate_w: weighted estate.
    :param d: claims of the claimants (list or tuple).
    :param w: weights of the claimants.
    :return: allocation vector (list).

    >>> d = [100, 300, 200]
    >>> w = [1, 2, 1]
    >>> wcea(120, d, w)
    [40.0, 20.0, 40.0]
    >>> wcea(330, d, w)
    [100.0, 57.5, 115.0]
    >>> wcea(520, d, w)
    [100.0, 110.0, 200.0]
    >>> wcea(800, d, w)
    [100.0, 250.0, 200.0]
    >>> wcea(1000, d, w)
    [100.0, 300.0, 200.0]
    >>> wcea(0, d, w)
    [0.0, 0.0, 0.0]
    >>> d = [200, 200, 200]
    >>> wcea(300, d, w)
    [100.0, 50.0, 100.0]
    """
    dw = list(map(lambda a, b: a*b, d, w))
    xw = cea(estate_w, dw)
    return list(map(lambda a, b: a/b, xw, w))


def wcea_i(estate_w, d, w):
    """ Weighted Constrained Equal Award.
    Note: input and output take integer values.
    Round down floats if there exist.

    :param estate_w: weighted estate (nonnegative int).
    :param d: claims of the claimants (list or tuple of integers).
    :param w: weights of the claimants (list or tuple of integers).
    :return: allocation vector (list of integers).

    >>> d = [100, 300, 200]
    >>> w = [1, 2, 1]
    >>> wcea_i(121, d, w)
    [40, 20, 40]
    >>> wcea_i(330, d, w)
    [100, 57, 115]
    >>> wcea_i(521, d, w)
    [100, 110, 200]
    >>> wcea_i(801, d, w)
    [100, 250, 200]
    >>> wcea_i(1000, d, w)
    [100, 300, 200]
    >>> wcea_i(0, d, w)
    [0, 0, 0]
    >>> d = [200, 200, 200]
    >>> wcea_i(300, d, w)
    [100, 50, 100]
    """
    dw = list(map(lambda a, b: a * b, d, w))
    xw = cea_i(estate_w, dw)
    return list(map(lambda a, b: int(a // b), xw, w))


def cg(estate, d):
    """ Contested Garment.

    :param estate: nonnegative int or float
    :param d: claims of the claimants (list or tuple).
    :return: allocation vector (list).

    >>> d = [100, 300, 200]
    >>> cg(102, d)
    [34.0, 34.0, 34.0]
    >>> cg(200, d)
    [50, 75.0, 75.0]
    >>> cg(300, d)
    [50, 150, 100]
    >>> cg(501, d)
    [67.0, 267.0, 167.0]
    >>> cg(800, d)
    [100, 300, 200]
    >>> cg(0, d)
    [0.0, 0.0, 0.0]
    """
    total_claim = sum(d)
    d_half = [i // 2 for i in d]
    if estate >= total_claim:
        return d
    if estate < total_claim / 2:
        return cea(estate, d_half)
    else:
        lost = cea(total_claim - estate, d_half)
        return [d[i] - lost[i] for i in range(len(lost))]


def cg_i(estate, d):
    """ Contested Garment.
    Note: input and output take integer values.
    Round down floats if there exist.
    :param estate: int.
    :param d: claims of the claimants (list or tuple of integers).
    :return: allocation vector (list of integers).

    >>> d = [100.5, 300, 200]
    >>> cg_i(101.5, d)
    [33, 34, 34]
    >>> cg_i(201, d)
    [50, 76, 75]
    >>> cg_i(301, d)
    [50, 151, 100]
    >>> cg_i(500.5, d)
    [67, 266, 167]
    >>> cg_i(800, d)
    [100, 300, 200]
    >>> cg_i(0.5, d)
    [0, 0, 0]
    >>> cg_i(1, d)
    [0, 1, 0]
    """
    estate = int(estate)
    total_claim = sum(d)
    d_half = [i // 2 for i in d]
    if estate >= total_claim:
        return [int(i) for i in d]
    if estate < total_claim / 2:
        return cea_i(estate, d_half)
    else:
        lost = cea_i(total_claim - estate, d_half)
        return [int(d[i]) - lost[i] for i in range(len(lost))]


def wcg(estate_w, d, w):
    """ Weighted Contested Garment.

    :param estate_w: weighted estate.
    :param d: claims of the claimants (list or tuple).
    :param w: weights of the claimants (list or tuple).
    :return: allocation vector (list).

    >>> d = [100, 300, 200]
    >>> w = [1, 2, 1]
    >>> wcg(120, d, w)
    [40.0, 20.0, 40.0]
    >>> wcg(200, d, w)
    [50.0, 37.5, 75.0]
    >>> wcg(300, d, w)
    [50.0, 75.0, 100.0]
    >>> wcg(600, d, w)
    [50.0, 225.0, 100.0]
    >>> wcg(900, d, w)
    [100.0, 300.0, 200.0]
    >>> wcg(0, d, w)
    [0.0, 0.0, 0.0]
    """
    dw = list(map(lambda a, b: a * b, d, w))
    xw = cg(estate_w, dw)
    return list(map(lambda a, b: a / b, xw, w))


def wcg_i(estate_w, d, w):
    """ Weighted Contested Garment.
    Note: input and output take integer values.
    Round down floats if there exist.
    :param estate_w: weighted estate (int).
    :param d: claims of the claimants (list or tuple of integers).
    :param w: weights of the claimants (list or tuple of integers).
    :return: allocation vector (list of integers).

    >>> d = [100.5, 300, 200]
    >>> w = [1, 2, 1]
    >>> wcg_i(120, d, w)
    [40, 20, 40]
    >>> wcg_i(200, d, w)
    [50, 37, 75]
    >>> wcg_i(300.1, d, w)
    [50, 75, 100]
    >>> wcg_i(600, d, w)
    [50, 225, 100]
    >>> wcg_i(900, d, w)
    [100, 300, 200]
    >>> wcg_i(0, d, w)
    [0, 0, 0]
    """
    dw = list(map(lambda a, b: a * b, d, w))
    xw = cg_i(estate_w, dw)
    return list(map(lambda a, b: int(a // b), xw, w))


def allocate(estate, d, w=None, round_down=True):
    """ Allocate (weighted) estate by Contested Garment (CG) rule.
    :param estate: estate or total weight (integer).
    :param d: claims by claimants (list).
    :param w: weights of claims (list).
    :param round_down: boolean. If true, allocate integral values.
    :return: allocation vector (list).

    >>> d = [100, 300, 200]
    >>> allocate(200, d)
    [50, 75, 75]
    >>> allocate(800, d)
    [100, 300, 200]
    >>> w = [1.2, 1, 1]
    >>> allocate(100, d, w)
    [27, 34, 33]
    >>> allocate(200, d, w)
    [50, 70, 70]
    >>> allocate(300, d, w)
    [50, 140, 100]
    >>> w = [1.2, 1, 1]
    >>> allocate(100, d, [1, 2, 1])
    [33, 17, 33]
    >>> d = [100, 100, 100]
    >>> allocate(200, d, [1, 2, 1])
    [50, 50, 50]
    >>> allocate(200, d, [1, 2, 1000])
    [50, 37, 0]
    """
    if not isinstance(d, list):
        raise ValueError("d must be a list!")
    if not d:
        raise ValueError("d can not be empty")
    if w is None:
        w = [1] * len(d)
    elif not isinstance(d, list):
        raise ValueError("w must be a list!")
    if estate <= 0:
        raise ValueError("estate cannot be negative!")
    for di in d:
        if di < 0:
            raise ValueError("claim cannot be negative!")
    for wi in w:
        if wi < 0:
            raise ValueError("weight cannot be negative!")

    return wcg_i(estate, d, w) if round_down else wcg(estate, d, w)


if __name__ == '__main__':
    doctest.testmod()

