from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='TimedDict',
    version='0.2.1',
    packages=['TimedDict'],
    url='https://github.com/hjortlund/TimedDict',
    license='MIT',
    author='Christoffer Hjortlund',
    author_email='hjortlund@gmail.com',
    description='Extending the dict data type, with a rolling window feature, that automatically purge elements falling outside the defined window.',
    long_description=readme(),
    long_description_content_type="text/markdown",
)
