import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='toms-dist-sampler',
    version='0.0.1',
    description=(
        'A distribution sampler for Normal, Poisson and Binomial '
        'distributions.'
    ),
    url='https://github.com/Tommo565/distribution-sampler',
    author='Tom Ewing',
    author_email='ewingt1979@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
