import doctest


def allocate(estate, d, w=None):
    """ Allocate (weighted) estate by Contested Garment (CG) rule.
    :param estate: estate or total weight (integer).
    :param d: claims by claimants (list).
    :param w: weights of claims (list).
    :return: allocation vector (list).
    """
    if not isinstance(d, list):
        raise ValueError("d must be a list!")
    if not d:
        raise ValueError("d can not be empty")
    if w is None:
        w = [1] * len(d)
    else:
        raise ValueError("w must be a list!")
    if estate <= 0:
        raise ValueError("estate must be a positive integer!")

    return weighted_contested_garment(estate, d, w)


def weighted_contested_garment(estate_w, d, w):
    """ Allocate estate by Contested Garment (CG) rule.

    :param estate_w: estate w.r.t. total weight (integer).
    :param d: claims by claimants (list).
    :param w: weights of claims (list).
    :return: allocation vector (list).
    >>> d = [100, 300, 200]
    >>> w = [1.2, 1, 1]
    >>> weighted_contested_garment(100, d, w)
    [27, 34, 33]
    >>> weighted_contested_garment(200, d, w)
    [50, 70, 70]
    >>> weighted_contested_garment(300, d, w)
    [50, 140, 100]
    """
    total_claim = sum(d)
    d_half = [i//2 for i in d]
    if estate_w <= total_claim/2:
        return weighted_constrained_equal_award(estate_w, d_half, w)
    else:
        lost = weighted_contested_garment(total_claim - estate_w, d_half, w)
        return [d[i]-lost[i] for i in range(len(lost))]


def weighted_constrained_equal_award(estate_w, d, w):
    """ Allocate estate by Constrained Equal Award rule.

    :param estate_w: estate w.r.t. total weight (integer).
    :param d: claims by claimants (list).
    :param w: weights of claims (list).
    :return: allocation vector (list).
    """
    x = []
    n = len(d)
    dw = list(map(lambda a, b: a * b, d, w))
    # sort dw and remember orders.
    claims = dict(zip(range(n), dw))
    claims = list(zip(*sorted(claims.items(), key=lambda item: item[1])))
    dw_index = claims[0]
    dw_sorted = claims[1]
    w_sorted = [w[dw_index[i]] for i in range(n)]
    # allocate
    __wcea(estate_w, dw_sorted, w_sorted, x)
    # give reward to the right person.
    y = [0] * n
    for i in range(n):
        y[dw_index[i]] = x[i]

    # allocate in terms of claims and return.
    return [round(y[i]/w_sorted[i]) for i in range(n)]


def __wcea(estate, dw, w, x):
    """ Allocate estate by Constrained Equal Award rule, where weighted claims (dw) are in ascent order.
    """
    k = len(dw)
    if k == 0:
        return

    if k * dw[0] <= estate:
        x0 = dw[0]
    else:
        x0 = estate // k
        x0 = x0 - x0 % w[0]  # x0 should be multiple of w[0]

    x.append(x0)
    __wcea(estate - x0, dw[1:], w[1:], x)


if __name__ == '__main__':
    doctest.testmod()
