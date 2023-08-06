
def corr_rank(x, axis=0):
    import korr
    import warnings

    warnings.warn(
        ("'oxyba.corr' is deprecated;"
         "use 'korr.spearman' instead."),
        DeprecationWarning, stacklevel=2)

    return korr.spearman(x, axis=axis)
