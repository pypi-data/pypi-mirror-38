import numpy as np
import matplotlib.pyplot as plt
import warnings


class DistributionSampler:
    def __init__(
        self, size=None, dist=None, mean=None, sd=None, lam=None, trials=None,
        prob=None
    ):
        '''

        Overview
        --------

        Selects a random sample from a given distribution, based upon the input
        parameters, and returns a numpy array object.

        You can set the parameters either upon creation of the instance or by
        using the set_parameters() method.

        Note that if you set the parameters upon creation of the instance, the
        class will attempt to create ths distribution immediately.

        If you change or create the parameters at a later time, you can create
        the sample using the draw() method.

        Attributes
        ----------

        size : integer

        The number of samples to be selected from the distribution.

        distribution : string

        The type of distribution to be created. Applicable values are 'Normal',
        'Poisson' or 'Binomial'.

        mean : float / int , optional

        Applicable to Normal distributions only. The mean value will dictate
        the centre of the distribution.

        sd: float / int , optional

        Applicable to Normal distributions only. The sd (Standard Deviation)
        will dictate the spread or width of the distribution.

        lam : float / int , optional

        Applicable to Poisson distributions only. The lam (lambda) controls the
        mean and variance of the sample.

        trials: float / int , optional

        Applicable to Binomial distributions only. The trials parameter is used
        to dictate the number of trials to run in generating the sample

        prob: float / int , optional

        Applicable to Binomial distributions only. The prob parameter is used
        to dicitate the probability of a trial being successful.

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details, check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------

        Instance = DistributionSampler(1000, 'Normal', mean=0, sd = 5)
        s = Instance.draw()

        Instance = DistributionSampler()
        Instance.set_parameters(size=1000, dist='Poisson', lam=5)
        s = Instance.draw()

        Instance = DistributionSampler()
        Instance.size = 1000
        Instance.dist = 'Binomial'
        Instance.trials = 5
        Instance.prob = 0.5
        s = Instance.draw()

        '''

        self.size = size
        self.dist = dist
        self.mean = mean
        self.sd = sd
        self.lam = lam
        self.trials = trials
        self.prob = prob
        self.sample = None
        self.sample_parameters = {}

        # If the parameters are filled upon creation of the instance, run the
        # draw method.
        if (size is not None) and (dist is not None):
            if (mean is not None) and (sd is not None):
                self.draw()

            elif (lam is not None):
                self.draw()

            elif (trials is not None) and (prob is not None):
                self.draw()

    def print_parameters(self):
        '''

        Overview
        --------

        Prints the current parameter values to the console. You can update the
        parameters using the set_parameters() method.

        Parameters
        ----------

        None

        Returns
        -------

        No values are returned, instead the parameters are printed to the
        console

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details, check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------

        Instance.print_parameters()

        '''
        print('Parameters')
        print('-----------')
        print('size: {}'.format(self.size))
        print('dist: {}'.format(self.dist))
        print('mean: {}'.format(self.mean))
        print('sd: {}'.format(self.sd))
        print('lam: {}'.format(self.lam))
        print('trials: {}'.format(self.trials))
        print('prob: {}'.format(self.prob))

    def print_sample(self):
        '''

        Overview
        --------

        Prints the current sample to the console. In the event that there is no
        sample to print, instructions on how to set the parameters and create
        the sample are given.

        Parameters
        ----------

        None

        Returns
        -------

        No values are returned, instead the parameters are printed to the
        console

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details, check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------

        Instance.print_sample()

        '''
        if self.sample is None:
            print(
                'No Sample to print. Use the .set_parameters() method to set '
                'appropriate parameters and then run the .draw() method to '
                'create a sample.'
            )

        else:
            print(self.sample)

    def set_parameters(
        self, size='', dist='', mean='', sd='', lam='', trials='', prob=''
    ):
        '''

        Overview
        --------

        Sets the parameters for the selection of the distribution. Multiple
        parameters can be passed in a single call to the function.

        Parameters
        ----------
        size : integer

        The number of samples to be selected from the distribution.

        distribution : string

        The type of distribution to be created. Applicable values are 'Normal',
        'Poisson' or 'Binomial'.

        mean : float / int , optional

        Applicable to Normal distributions only. The mean value will dictate t
        he centre of the distribution.

        sd: float / int , optional

        Applicable to Normal distributions only. The sd (Standard Deviation)
        will dictate the spread or width of the distribution.

        lam : float / int , optional

        Applicable to Poisson distributions only. The lam (lambda) controls
        the mean and variance of the sample.

        trials: float / int , optional

        Applicable to Binomial distributions only. The trials parameter is
        used to dictate the number of trials to run in generating the sample

        prob: float / int , optional

        Applicable to Binomial distributions only. The prob parameter is used
        to dicitate the probability of a trial being successful.


        Returns
        -------

        None

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details,check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------
        s = distribution_sampler(1000, 'Normal', mean=0, sd = 5)
        s = distribution_sampler(1000, 'Poisson', lam=5)
        s = distribution_sampler(1000, 'Binomial', trials=5, prob=0.5)
        '''

        local_data = locals()

        params = dict(local_data)
        del params['self']

        for key, value in params.items():
            if value == '':
                pass
            else:
                # This is a hack to get around exec not resolving quotes.
                if key == 'dist':
                    self.dist = value

                else:
                    exec('self.{} = {}'.format(key, value))

    def _validate_parameters(self):
        '''
        Private function to validate the input parameters, called during the
        draw() method. If the parameters are not valid, an error message will
        display with instructions on how to input valid parameters
        '''

        # Mandatory parameter error handling

        if self.dist not in ['Normal', 'Poisson', 'Binomial']:
            raise ValueError(
                "The dist parameter is mandatory and  must equal 'Normal', "
                "'Poisson', or 'Binomial'"
            )

        if not isinstance(self.size, int):
            raise ValueError(
                'The size parameter is mandatory and  must be an integer.'
            )

        # Distribution Specific Error Handling

        if self.size is None:
            raise ValueError(
                'You need to set a sample size prior to '
                '. calling the draw method. This must be an integer. E.g. '
                '10000. Parameters can be input either using the '
                'set_parameters() method, by manually updating the instance.'
                ' E.g. Instance.size = 10000 or by passing parameters to the '
                'draw() method. E.g. Instance.draw(size=10000)'
            )

        if self.dist is None:
            raise ValueError(
                'You need to set a dist parameter to specify the type of '
                'distribution prior to calling the draw method. Available '
                'parameters are as follows:\n\n'
                "'Normal'\n'Poisson'\n'Binomial'"
                'Parameters can be input either using the set_parameters()'
                ' method, by manually updating the instance. E.g. '
                'Instance.dist = "Normal" or by passing parameters to the '
                'draw() method. E.g. Instance.draw(dist="Normal")'
            )

        if self.dist == 'Normal':
            # Raise an error if the mean or sd parameters aren't set
            if (self.mean is None) or (self.sd is None):
                raise NameError(
                    "The mean and sd parameters must be set where the dist is"
                    "set to 'Normal'.  Parameters can be input either using "
                    "the set_parameters() method, by manually updating the "
                    "instance (e.g. Instance.mean=1) or by passing parameters "
                    "to the draw() method. E.g. Instance.draw(mean=q)"
                )

            # Raise a warning if irrelevent parameters are provided
            elif (
                (self.lam is not None) or (self.trials is not None) or
                (self.prob is not None)
            ):
                warnings.warn(
                    'The lam, trials and prob parameters are not used in the'
                    ' selection of a normal distribution. These parameters '
                    'will be ignored.\n'
                )

        if self.dist == 'Poisson':
            # Raise an error if the lam parameter isn't set
            if self.lam is None:
                raise NameError(
                    "The lam parameter must be set where dist is set to "
                    "'Poisson'. 'Parameters can be input either using the "
                    "set_parameters() method, by manually updating the "
                    "instance. (e.g. Instance.lam=5), or by passing parameters"
                    " to the draw() method. E.g. Instance.draw(lam=5)"

                )

            # Raise a warning if irrelevent parameters are provided
            elif (
                (self.mean is not None) or (self.sd is not None) or
                (self.trials is not None) or (self.prob is not None)
            ):
                warnings.warn(
                    'The mean, sd, trials and prob parameters are not used in '
                    'the selection of a ' 
                    'poisson distribution. These parameters will be ignored.\n'
                )

        if self.dist == 'Binomial':
            # Raise an error if the trials or prob parameters aren't set
            if (self.trials is None) or (self.prob is None):
                raise NameError(
                    "The trials and prob parameters must be set where dist is"
                    " 'Binomial'. 'Parameters can be input either using the "
                    "set_parameters() method, by manually updating the "
                    "instance (e.g. Instance.lam = 5) or by passing parameters"
                    " to the draw() method. E.g. Instance.draw(lam=5)"
                )

            # Raise a warning if irrelevent parameters are provided
            elif (
                (self.mean is not None) or (self.sd is not None)
                or (self.lam is not None)
            ):
                warnings.warn(
                    "The mean, sd and lam parameters are not used in the "
                    "selection of a binomial distribution. These parameters "
                    "will be ignored.\n"
                ) 

    def draw(
        self, size='', dist='', mean='', sd='', lam='', trials='', prob=''
    ):
        '''

        Overview
        --------

        Creates a sample based upon the input parameters. If there have been
        parameters passed to the function, the method will first run the
        set_parameters() method to update the parameters before validating
        these using the private method.

        Parameters
        ----------

        None


        Returns
        -------

        s : A numpy array of samples based upon the input parameters.

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details, check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------
        s = Instance.draw()
        s = Instance.draw(size=1000, dist='Normal', mean=1, sd=2)
        '''
        self.set_parameters(
            size=size, dist=dist, mean=mean, sd=sd, lam=lam, trials=trials,
            prob=prob
        )
        self._validate_parameters()

        if self.dist == 'Normal':
            self.sample = np.random.normal(self.mean, self.sd, self.size)
            self.sample_parameters['Distribution'] = self.dist
            self.sample_parameters['Sample Size'] = self.size
            self.sample_parameters['Mean'] = self.mean
            self.sample_parameters['Standard Deviation'] = self.sd
            self.sample_parameters['Minimum Value'] = self.sample.min()
            self.sample_parameters['Maximum Value'] = self.sample.max()
            self.sample_parameters['graph_string'] = (
                '{} Distribution, Mean: {}, Standard Deviation: {}'.format(
                    self.dist, self.mean, self.sd
                )
            )
            print('Normal Distribution Created')
            print('')

        if self.dist == 'Poisson':
            self.sample = np.random.poisson(self.lam, self.size)
            self.sample_parameters['Distribution'] = self.dist
            self.sample_parameters['Sample Size'] = self.size
            self.sample_parameters['Lambda'] = self.lam
            self.sample_parameters['Mean'] = self.sample.mean()
            self.sample_parameters['Standard Deviation'] = self.sample.std()
            self.sample_parameters['Minimum Value'] = self.sample.min()
            self.sample_parameters['Maximum Value'] = self.sample.max()
            self.sample_parameters['graph_string'] = (
                 '{} Distribution, Mean: {}, Standard Deviation: {}'.format(
                     self.dist, self.sample.mean(), self.sample.std()
                 )
            )
            print('Poisson Distribution Created')
            print('')

        if self.dist == 'Binomial':
            self.sample = np.random.binomial(self.trials, self.prob, self.size)
            self.sample_parameters['Distribution'] = self.dist
            self.sample_parameters['Sample Size'] = self.size
            self.sample_parameters['Trial Size'] = self.trials
            self.sample_parameters['Probability'] = self.prob
            self.sample_parameters['Mean'] = self.sample.mean()
            self.sample_parameters['Standard Deviation'] = self.sample.std()
            self.sample_parameters['Minimum Value'] = self.sample.min()
            self.sample_parameters['Maximum Value'] = self.sample.max()
            self.sample_parameters['graph_string'] = (
                 '{} Distribution, Mean: {}, Standard Deviation: {}'.format(
                     self.dist, self.sample.mean(), self.sample.std()
                 )
            )
            print('Binomial Distribution Created')
            print('')

        return self.sample

    def summarise(self, graph=True):   

        
        ''' 
        Overview
        --------

        Creates a summary, showing the parameters of the distribution alongside
        the mean, standard deviation, minimum value and maximum of the
        currently held sample for the instance.

        It will additionally display a seaborn chart for the distribution,
        which can be turned off by setting the graph option to False.

        Parameters
        ----------

        graph , bool , optional

        Defaults to True. Setting this to False will result in no graph being
        created.


        Returns
        -------

        None

        Notes
        -----

        The samples are generated using the numpy library, v1.15. For more
        details,check the API Reference material here:
        https://docs.scipy.org/doc/numpy-1.15.1/reference/

        Examples
        --------
        s = Instance.summarise()
        s = Instance.summarise(graph=False)
        '''
        if isinstance(self.sample, np.ndarray):
            print('Summary')
            print('-------')
            for key, value in self.sample_parameters.items():
                if key != 'graph_string':
                    print('{}: {}'.format(key, value))

        else:
            raise ValueError(
                'You have not created a sample to summarise. You can create'
                ' a sample by calling the draw() method with appropriate '
                'parameters e.g. Instance.draw(5000, "Normal", mean=2, sd=5) '
                'or of you have already input the parameters, simple call the '
                'draw method to create the sample e.g. Instance.draw()'
            )
