from collections import namedtuple

from mgc.ksample import KSample

Point = namedtuple("Point", ["x", "y"])


def _get_counts(graphs, point_1, point_2):

    X = []

    for graph in graphs:
        block = graph[point_1.x : point_2.x, point_1.y : point_2.y]
        X.append(block.flatten())

    return X


def test_block(blocks, expr_1, expr_2, indep_test, *samples, **mgc_kwargs):
    """
    Test block connectivity in an SBM using MGC.

    Parameters
    ----------
    blocks : pd.DataFrame
        Dataframe of block assignments.
    expr_1 : str
        Expression to subset the first block from `blocks`
    expr_2 : str
        Expression to subset the second block from `blocks`
    indep_test : {"CCA", "Dcorr", "HHG", "RV", "Hsic", "MGC", "DcorrRF", "HsicRF", "MGCRF"}
        A string corresponding to the desired independence test from `mgc.independence`.
    *samples : np.ndarray
        Matrices with vectorized edgeweights from the input block
    mgc_kwars : dict
        Dictionary of keyword arguments to `KSample.test`

    Returns
    -------
    stat : float
        The computed k-Sample statistic.
    pvalue : float
        The computed k-Sample p-value.
    """

    point_1 = Point(*blocks.query(expr_1).values[0][2:])
    point_2 = Point(*blocks.query(expr_2).values[0][2:])
    counts = [_get_counts(sample, point_1, point_2) for sample in samples]

    stat, pvalue = KSample(indep_test).test(*counts, **mgc_kwargs)
    return stat, pvalue
