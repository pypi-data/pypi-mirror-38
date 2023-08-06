from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='pyort',
    url='https://github.com/Gananath/Pyort',
    author='Gananath R',
    author_email='nomail@nomail.com',
    # Needed to actually package something
    packages=['pyort'],
    # Needed for dependencies
    install_requires=['psutil','argparse','pysqlite ;python_version<"3.0"','pysqlite3 ;python_version>"3.0"'],
    # *strongly* suggested for sharing
    version='0.1.7.5',
    
    entry_points = {
        'console_scripts': [
            'pyort=pyort.pyort:main',
        ],
    },
    # The license can be anything you like
    license='MIT',
    description='Command line tool for monitoring all network connections',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
