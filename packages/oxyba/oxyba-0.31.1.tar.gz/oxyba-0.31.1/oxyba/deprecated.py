
import warnings


def corr(x, axis=0):
    warnings.warn(
        ("'oxyba.corr' is deprecated;"
         "use 'korr.pearson' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.pearson(x, axis=axis)


def corr_tau(x, axis=0):
    warnings.warn(
        ("'oxyba.corr' is deprecated;"
         "use 'korr.kendall' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.kendall(x, axis=axis)


def corr_rank(x, axis=0):
    warnings.warn(
        ("'oxyba.corr' is deprecated;"
         "use 'korr.spearman' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.spearman(x, axis=axis)


def mapencode(data, mapping, nastate=False):
    warnings.warn(
        ("'oxyba.mapencode' is deprecated;"
         "use 'grouplabelencode.grouplabelencode' instead."),
        DeprecationWarning, stacklevel=2)
    import grouplabelencode
    return grouplabelencode.grouplabelencode(data, mapping, nastate=nastate)


def illcond_corrmat(D, random_state=None):
    warnings.warn(
        ("'oxyba.illcond_corrmat' is deprecated;"
         "use 'illmat.illmat' instead."),
        DeprecationWarning, stacklevel=2)
    import illmat
    return illmat.illmat(D, random_state=random_state)


def subjcorr_kfactor(R, k=2, algorithm='COBYLA'):
    warnings.warn(
        ("'oxyba.subjcorr_kfactor' is deprecated;"
         "use 'kfactor.kfactor' instead."),
        DeprecationWarning, stacklevel=2)
    import kfactor
    return kfactor.kfactor(R, k=k, algorithm=algorithm)


def subjcorr_luriegold(R):
    warnings.warn(
        ("'oxyba.subjcorr_onepara' is deprecated;"
         "use 'onepara.onpara' instead."),
        DeprecationWarning, stacklevel=2)
    import luriegold
    return luriegold.luriegold(R)


def subjcorr_onepara(R):
    warnings.warn(
        ("'oxyba.subjcorr_onepara' is deprecated;"
         "use 'onepara.onpara' instead."),
        DeprecationWarning, stacklevel=2)
    import onepara
    return onepara.onepara(R)


def threeway_split(*data, test_size=0.2, random_state=None, shuffle=True):
    # load modules
    import numpy as np
    import warnings

    warnings.warn(
        ("'oxyba.threeway_split' is deprecated;"
         "use 'threesplit.threesplit' instead."),
        DeprecationWarning, stacklevel=2)

    # subfunction - enforce numpy arrays, variables as columns
    def to_colvec(dat):
        out = np.asarray(dat)
        if len(out.shape) == 1:
            out = out.reshape(out.shape[0], 1)
        return out

    # read *data=(x,y) or data=x
    if len(data) == 2:
        xonly = False
        x = to_colvec(data[0])
        y = to_colvec(data[1])
        # check number of observations
        if x.shape[0] != y.shape[0]:
            raise Exception('x and y have not the same number of observations')
    else:
        xonly = True
        x = to_colvec(data[0])

    # number of obs
    n = x.shape[0]

    # check number of observations
    if n < 3:
        raise Exception('only n<3 observations provided')

    # number of obs for the validation and test set each
    nv = 1 if test_size * n < 1.0 else round(test_size * n)

    # number of obs for the training set
    nt = n - 2 * nv

    # use a generic row index variable for the splitting task
    idx = np.arange(0, n)

    # set initial random state
    if shuffle and random_state:
        np.random.seed(random_state)
    # shuffle the index
    if shuffle:
        np.random.shuffle(idx)

    # output: x_train, x_valid, x_test, y_train, y_valid, y_test,
    if xonly:
        return x[idx[:nt], :], x[idx[nt:(nt + nv)], :], x[idx[-nv:], :]
    else:
        return x[idx[:nt], :], x[idx[nt:(nt + nv)], :], x[idx[-nv:], :],
        y[idx[:nt], :], y[idx[nt:(nt + nv)], :], y[idx[-nv:], :]


def rand_dates(num, posix_start=0, posix_end=None):
    warnings.warn(
        ("'oxyba.rand_dates' is deprecated;"
         "use 'randdate.randdate' instead."),
        DeprecationWarning, stacklevel=2)
    import randdate
    return randdate.randdate(
        num, posix_start=posix_start, posix_end=posix_end)


def heatmap_corr(r, pval, varnames=None, dpi=96, cmap='RdBu'):
    warnings.warn(
        ("'oxyba.heatmap_corr' is deprecated;"
         "use 'korr.corrgram' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.corrgram(r, pval, varnames=varnames, dpi=dpi, cmap=cmap)


def hist_corr_pval(r, pval, plim=0.01, rlim=0.4, dpi=96):
    warnings.warn(
        ("'oxyba.heatmap_corr' is deprecated;"
         "use 'korr.corr_vs_pval' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.corr_vs_pval(r, pval, plim=plim, rlim=rlim, dpi=dpi)


def hist_corr_pval_groups(r, pval, plim=[.1, .01, .001], nbins=None, dpi=96):
    warnings.warn(
        ("'oxyba.heatmap_corr' is deprecated;"
         "use 'korr.bracket_pval' instead."),
        DeprecationWarning, stacklevel=2)
    import korr
    return korr.bracket_pval(r, pval, plim=plim, nbins=nbins, dpi=dpi)
