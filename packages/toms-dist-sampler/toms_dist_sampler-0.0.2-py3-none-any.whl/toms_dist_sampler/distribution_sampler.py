import numpy as np
import warnings


def _validate_params(size, dist, mean, sd, lam, trials, prob):
    '''
    Sub function for the distribution_sampler function to validate the
    user input parameters. If the parameters are incorrect, a TypeError
    is raised to alert the user to change the input parameters
    '''

    # Mandatory parameter error handling

    if dist not in ['Normal', 'Poisson', 'Binomial']:
        raise ValueError(
            "The dist parameter is mandatory and must equal 'Normal'",
            "'Poisson', or 'Binomial'"
        )

    if not isinstance(size, int):
        raise ValueError(
            'The size parameter is mandatory and must be an integer.'
        )

    # Distribution specific error handling and warnings

    if dist == 'Normal':
        # Raise an error if the mean or sd parameters aren't set
        if (mean is None) or (sd is None):
            raise NameError(
                "The mean and sd parameters must be set where dist == 'Normal'"
            )

        # Raise a warning if irrelevent parameters are provided
        elif (lam is not None) or (trials is not None) or (prob is not None):
            warnings.warn(
                'The lam, trials and prob parameters are not used in the '
                'selection of a normal distribution. These parameters will be'
                ' ignored.'
            )

    if dist == 'Poisson':
        # Raise an error if the lam parameter isn't set
        if lam is None:
            raise NameError(
                "The lam parameter must be set where dist is 'Poisson'"
            )

        # Raise a warning if irrelevent parameters are provided
        elif (
            (mean is not None) or (sd is not None) or
            (trials is not None) or (prob is not None)
        ):
            warnings.warn(
                'The mean, sd, trials and prob parameters are not used in the '
                'selection of a poisson distribution. These parameters will be'
                ' ignored.'
            )

    if dist == 'Binomial':
        # Raise an error if the trials or prob parameters aren't set
        if (trials is None) or (prob is None):
            raise NameError(
                "The trials and prob parameters must be set where dist is "
                " 'Binomial'"
            )

        # Raise a warning if irrelevent parameters are provided
        elif (mean is not None) or (sd is not None) or (lam is not None):
            warnings.warn(
                'The mean, sd and lam parameters are not used in the selection'
                ' of a binomial distribution. These parameters will be '
                'ignored.'
            )


def _generate_normal(size, mean, sd):
    '''
    Sub function for the distribution_sampler function. Generates samples from
    a normal distribution based upon the size, mean and sd parameters.

    Returns the generated sample as s.
    '''
    s = np.random.normal(mean, sd, size)
    return s


def _generate_poisson(size, lam):
    '''
    Sub function for the distribution_sampler function. Generates samples from
    a poisson distribution based upon the size and lam parameters.

    Returns the generated sample as s.
    '''
    s = np.random.poisson(lam, size)
    return s


def _generate_binomial(size, trials, prob):
    '''
    Sub function for the distribution_sampler function. Generates samples from
    a binomial distribution based upon the size, trials and prob parameters.

    Returns the generated sample as s.
    '''
    s = np.random.binomial(trials, prob, size)
    return s


def distribution_sampler(
    size, dist, mean=None, sd=None, lam=None, trials=None, prob=None
):

    '''

    Selects a random sample from a given distribution, based upon the input
    parameters, and returns a numpy array object.

    Parameters
    ----------
    size : integer

    The number of samples to be selected from the distribution.

    distribution : string

    The type of distribution to be created. Applicable values are 'Normal',
    'Poisson' or 'Binomial'.

    mean : float / int , optional

    Applicable to Normal distributions only. The mean value will dictate the
    centre of the distribution.

    sd: float / int , optional

    Applicable to Normal distributions only. The sd (Standard Deviation) will
    dictate the spread or width of the distribution.

    lam : float / int , optional

    Applicable to Poisson distributions only. The lam (lambda) controls the
    mean and variance of the sample.

    trials: float / int , optional

    Applicable to Binomial distributions only. The trials parameter is used to
    dictate the number of trials to run in generating the sample

    prob: float / int , optional

    Applicable to Binomial distributions only. The prob parameter is used to
    dicitate the probability of a trial being successful.


    Returns
    -------

    s : A numpy array of samples based upon the input parameters.

    Notes
    -----

    The samples are generated using the numpy library, v1.15. For more details,
    check the API Reference material here:
    https://docs.scipy.org/doc/numpy-1.15.1/reference/

    Examples
    --------
    s = distribution_sampler(1000, 'Normal', mean=0, sd = 5)
    s = distribution_sampler(1000, 'Poisson', lam=5)
    s = distribution_sampler(1000, 'Binomial', trials=5, prob=0.5)
    '''

    # Validate the parameters
    _validate_params(size, dist, mean, sd, lam, trials, prob)

    # Generate the appropriate distribution sample
    if dist == 'Normal':
        s = _generate_normal(size, mean, sd)

    elif dist == 'Poisson':
        s = _generate_poisson(size, lam)

    elif dist == 'Binomial':
        s = _generate_binomial(size, trials, prob)

    return s
