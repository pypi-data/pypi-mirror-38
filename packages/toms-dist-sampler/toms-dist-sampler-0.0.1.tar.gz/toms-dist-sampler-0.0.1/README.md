# toms_dist_sampler

## Introduction

Tom's Distribution Sampler makes creating Normal, Poisson and Binomial samples and getting the summary statistics on these in Python easy! I created the sampler as a bit of a pet project to get used to writing OOP and also releasing Python packages. This is my first attempt at it and whilst it was great fun, I learned a lot also! If anyone finds an actual use for it (possibly unlikely?) please let me know. Or buy me a beer. I'd rather the beer in all honesty.


## Installation

Presently toms_dist_sampler is only available for Python3. Sorry about that Python2 users. But it's probably as good an opportunity as any to upgrade!

### Installation via pip

I highly reccomend you install the package with `pip`:

`pip install toms-dist-sampler`

or alternatively if you have multple version of Python on your system:

`pip3 install toms-dist-sampler`

### Installation via Github

You can also install via github is as follows:

```
git clone https://github.com/Tommo565/toms_dist_sampler
cd toms_dist_sampler
python setup.py install
```

If the last line fails, it may be because you have multiple versions of Python installed on your system. So, you might also want to try:
`python3 setup.py install`


## Examples

The sampler itself is available both as a set of functions and also as a class. The base sample selection functionality within these is identical, however there are a few more options available in the Class which I'll cover below. which you use should be down to your own personal preference. 

If you use this package you'll probably want to understand a bit about the underlying distributions as well. You can find a great in depth resource at [Minitab Express](https://support.minitab.com/en-us/minitab-express/1/help-and-how-to/basic-statistics/probability-distributions/supporting-topics/distributions/binomial-distribution/) or alternatively a cheat-sheet at [Cloudera](http://blog.cloudera.com/blog/2015/12/common-probability-distributions-the-data-scientists-crib-sheet/)

### distribution_sampler Function

I reccomend that you use the following convention to import:

`from toms_dist_sampler.distribution_sampler import distribution_sampler as ds`

From there you can run a sample for a Normal distribution like so:

`norm = ds(dist='Normal', size=1000, mean=2, sd=5)`

Or a Poisson distribution like so:

`poisson = ds(dist='Poisson', size=5000, lam=3)`

And finally a Binomial distribution like so:

`binomial = ds(dist='Binomial', size=2500, trials=20, prob=0.2)`

You can also call the help function for a more detailed overview of the functionality and parameters:

`help(ds)`

All samples are created in [numpy array](https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.array.html) format. You can convert them to a more traditional python list as follows:

```
norm = ds(dist='Normal', size=1000, mean=2, sd=5)`
norm_list = norm.tolist()
```

Note that only the `size=` and `dist=` parameters are applicable to all distribution types. Depending upon the distribution that you choose, you will have to specify the right parameters for that distribution in the examples above. If you select an incorrect combination of parameters, you will receive an error message with further guidance on how to select the correct parameters.

### DistributionSampler Class

As with functions I reccomend that you use the following convention to import the Class:

`from toms_dist_sampler.DistributionSampler import DistributionSampler as DS`

The class is flexible and when creating the instance you can either do so with parameters:

`my_instance = DS(dist='Normal', size=1000, mean=2, sd=5)`

or without:

`MyInstance = DS()`

Creating an instance with parameters will result in the sample being generated immediately. However if you create it without parameters and want to add them, you can do so with the `set_parameters()` method as follows:

`MyInstance.set_parameters(dist='Poisson', size=5000, lam=3)`

You can print the parameters at any time using the `print_parameters()` method as follows:

`MyInstance.print_parameters()`

Note that if you switch between distribution types (e.g. `dist=Normal` and `dist=Poisson`) then the previous parameters are retained. This will generate a warning, and won't affect your results but I do reccomend that if you wish to switch distribution types you create a different instance of the class as desribed above.

To create a new sample, you must use the `.draw()` method after you have set parameters as follows:

`MyInstance.draw()`

You can also use the `.draw()` method at any time to create a new sample with your existing parameters.

It you want to print your sample you can use th `.print_sample()` method as follows:

`MyInstance.print_sample()`

This prints your sample to the console.

Finally the `.summarise()` method will print some summary statistics to the console, including minimum and maximum values as well as standard deviation and mean average:

`MyInstance.summarise()`

You can also call the help function for a more detailed overview of the functionality and parameters:

`help(DS)`

All samples are created in [numpy array](https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.array.html) format. You can convert them to a more traditional python list as follows:

```
MyInstance = DS(dist='Normal', size=1000, mean=2, sd=5)`
norm = MyInstance.draw()
norm_list = norm.tolist()
```

Note that only the `size=` and `dist=` parameters are applicable to all distribution types. Depending upon the distribution that you choose, you will have to specify the right parameters for that distribution in the examples above. If you select an incorrect combination of parameters, you will receive an error message with further guidance on how to select the correct parameters.


## Tests

Tests are performed using the [PyTest](https://docs.pytest.org/en/latest/) package. To run these, navigate to the `./tests/` folder in the command line and run:

`pytest -v`

## Credits

Massive thanks to [Matt Upson](https://github.com/ivyleavedtoadflax) whose help in checking this was invaluable. I probably owe him a beer! 🍺

## License

MIT © [Tom Ewing](https://github.com/Tommo565)

[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)




