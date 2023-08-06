.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_stats_guess_the_dist.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_stats_guess_the_dist.py:


Guess the distribution!
=======================

Fit several distributions to angular residuals.

Note: to fit the landau distribution, you need to have ROOT and the
``rootpy`` package installed.




.. code-block:: python

    from __future__ import absolute_import, print_function, division

    import h5py
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats
    from statsmodels.distributions.empirical_distribution import ECDF
    from statsmodels.nonparametric.kde import KDEUnivariate

    try:
        import ROOT
        import rootpy.plotting
        HAS_ROOT = True
    except ImportError:
        HAS_ROOT = False

    from km3pipe.stats import bootstrap_fit
    import km3pipe.style.moritz    # noqa



.. code-block:: python


    DATA_FILE = '../data/residuals.h5'

    with h5py.File(DATA_FILE) as h5:
        resid = h5['/residuals'][:]


Fit somedistributions, and obtain the confidence intervals on the
distribution parameters through bootstrapping.



.. code-block:: python


    n_bs = 5
    q = 95

    ln_par, ln_lo, ln_up = bootstrap_fit(
        stats.lognorm, resid, n_iter=n_bs, quant=q
    )
    hc_par, hc_lo, hc_up = bootstrap_fit(
        stats.halfcauchy, resid, n_iter=n_bs, quant=q
    )
    gam_par, gam_lo, gam_up = bootstrap_fit(
        stats.gamma, resid, n_iter=n_bs, quant=q
    )



.. code-block:: python


    hc = stats.halfcauchy(*stats.halfcauchy.fit(resid))
    lg = stats.lognorm(*stats.lognorm.fit(resid))
    dens = KDEUnivariate(resid)
    dens.fit()
    ecdf = ECDF(resid)


prepare X axes for plotting



.. code-block:: python


    ex = ecdf.x
    x = np.linspace(min(resid), max(resid), 2000)


Fit a Landau distribution with ROOT



.. code-block:: python


    if HAS_ROOT:
        root_hist = rootpy.plotting.Hist(100, 0, np.pi)
        root_hist.fill_array(resid)
        root_hist /= root_hist.Integral()

        land_f = ROOT.TF1('land_f', "TMath::Landau(x, [0], [1], 0)")
        fr = root_hist.fit('land_f', "S").Get()
        try:
            p = fr.GetParams()
            land = np.array([ROOT.TMath.Landau(xi, p[0], p[1], True) for xi in x])
            land_cdf = np.array([
                ROOT.ROOT.Math.landau_cdf(k, p[0], p[1]) for k in ex
            ])
        except AttributeError:
            # wtf this fails sometimes, idk, works on root6
            HAS_ROOT = False


... and plot everything.



.. code-block:: python


    fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(6 * 2, 4 * 2))

    axes[0, 0].hist(resid, bins='auto', normed=True)
    axes[0, 0].plot(x, lg.pdf(x), label='Log Norm')
    axes[0, 0].plot(x, hc.pdf(x), label='Half Cauchy')
    if HAS_ROOT:
        axes[0, 0].plot(x, land, label='Landau', color='blue')
    axes[0, 0].plot(x, dens.evaluate(x), label='KDE')
    axes[0, 0].set_xlabel('x')
    axes[0, 0].set_xlim(0, 0.3)
    axes[0, 0].set_ylabel('PDF(x)')
    axes[0, 0].legend()

    axes[0, 1].hist(resid, bins='auto', normed=True)
    axes[0, 1].plot(x, lg.pdf(x), label='Log Norm')
    axes[0, 1].plot(x, hc.pdf(x), label='Half Cauchy')
    if HAS_ROOT:
        axes[0, 1].plot(x, land, label='Landau', color='blue')
    axes[0, 1].plot(x, dens.evaluate(x), label='KDE')
    axes[0, 1].set_xlabel('x')
    axes[0, 1].set_ylabel('PDF(x)')
    axes[0, 1].set_yscale('log')
    axes[0, 1].legend()

    axes[1, 0].plot(ex, 1 - lg.cdf(ex), label='Log Norm')
    if HAS_ROOT:
        axes[1, 0].plot(ex, 1 - land_cdf, label='Landau', color='blue')
    axes[1, 0].plot(ex, 1 - hc.cdf(ex), label='Half Cauchy')
    axes[1, 0].plot(
        ex, 1 - ecdf.y, label='Empirical CDF', linewidth=3, linestyle='--'
    )
    axes[1, 0].set_xscale('log')
    axes[1, 0].set_xlabel('x')
    axes[1, 0].set_ylabel('1 - CDF(x)')
    axes[1, 0].legend()

    axes[1, 1].loglog(ex, 1 - lg.cdf(ex), label='Log Norm')
    if HAS_ROOT:
        axes[1, 1].loglog(ex, 1 - land_cdf, label='Landau', color='blue')
    axes[1, 1].loglog(ex, 1 - hc.cdf(ex), label='Half Cauchy')
    axes[1, 1].loglog(
        ex, 1 - ecdf.y, label='Empirical CDF', linewidth=3, linestyle='--'
    )
    axes[1, 1].set_xlabel('x')
    axes[1, 1].set_ylabel('1 - CDF(x)')
    axes[1, 1].legend()

**Total running time of the script:** ( 0 minutes  0.000 seconds)


.. _sphx_glr_download_auto_examples_stats_guess_the_dist.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: guess_the_dist.py <guess_the_dist.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: guess_the_dist.ipynb <guess_the_dist.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.readthedocs.io>`_
