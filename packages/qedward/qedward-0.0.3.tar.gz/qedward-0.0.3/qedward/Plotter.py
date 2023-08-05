import numpy as np
import matplotlib.pyplot as plt


class Plotter:
    """
    matplotlib plotting routines.

    Many inputs to the functions of this class are arrays of shape (nt, 2,
    len1). In that shape,

    * nt refers to time (aka iteration).  fin_t <= nt-1 and only the first
    fin_t entries of the array contain valid data.

    * 2 refers to whether for conc0 or conc1.

    * len1 refers to the number of layers. For instance, for NbTrols and
    NoNbTrols models, len1=na+nb.

    For plotting purposes, to reduce number of angles being displayed,
    each layer of list1_conc0 and list1_conc1 is averaged so that it becomes
    a scalar.

    """

    @staticmethod
    def plot_conc_traces(fin_t, conc_nt_2_len1, delta_conc_nt_2_len1):
        """
        The input parameters of this function are created and filled when
        one runs Fitter:do_fit().

        This function plots time series (aka traces), for t = int in range(
        fin_t), of concentrations conc0 and conc1 and their deltas
        delta_conc0, delta_conc1, for each layer.

        Parameters
        ----------
        fin_t : int
            final time. Must be <= nt-1
        conc_nt_2_len1 : np.array
            shape=(nt, 2, len1). This array is stored within Fitter and
            filled by a call to Fitter:do_fit(). It contains the time-series
            of conc0, conc1 for each layer.
        delta_conc_nt_2_len1 : np.array
            shape=(nt, 2, len1). This array is stored within Fitter and
            filled by a call to Fitter:do_fit(). It contains the time-series
            of the CHANGES in conc0 and conc1 for each layer. (here CHANGES
            refers to changes between consecutive time steps).

        Returns
        -------
        None

        """
        y_shape = conc_nt_2_len1.shape
        assert fin_t <= y_shape[0]-1
        len1 = y_shape[2]

        fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True)
        for k in range(len1):
            for y in range(2):
                ax[0, y].plot(range(fin_t), conc_nt_2_len1[0:fin_t, y, k],
                              label='layer ' + str(k))
                ax[0, y].legend(loc='best', fontsize='xx-small')
                ax[0, y].set_ylabel("conc" + str(y))

                ax[1, y].plot(range(fin_t),
                              delta_conc_nt_2_len1[0:fin_t, y, k],
                              label='layer ' + str(k))
                ax[1, y].legend(loc='best', fontsize='xx-small')
                ax[1, y].set_ylabel("delta_conc" + str(y))

        ax[0, 0].get_shared_y_axes().join(ax[0, 0], ax[0, 1])
        ax[1, 0].get_shared_y_axes().join(ax[1, 0], ax[1, 1])
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_elbo_traces(fin_t, elbo_nt_len1):
        """
        The input parameters of this function are created and filled when
        one runs Fitter:do_fit().

        This function plots time series (aka traces), for t = int in range(
        fin_t), of ELBO for each layer. Since we are attempting to maximize
        ELBO, ideally this curve should be increasing or flat.

        Parameters
        ----------
        fin_t : int
            final time. Must be <= nt-1
        elbo_nt_len1 : np.array
            shape=(nt, len1) This array is stored within Fitter and
            filled by a call to Fitter:do_fit(). It contains the time-series
            of ELBO for each layer.

        Returns
        -------
        None

        """
        y_shape = elbo_nt_len1.shape
        assert fin_t <= y_shape[0]
        len1 = y_shape[1]

        for k in range(len1):
            plt.plot(range(fin_t), elbo_nt_len1[0:fin_t, k],
                     label='layer ' + str(k))
        plt.xlabel("t")
        plt.ylabel("ELBO")
        plt.legend(loc=0, fontsize='xx-small')
        plt.show()
