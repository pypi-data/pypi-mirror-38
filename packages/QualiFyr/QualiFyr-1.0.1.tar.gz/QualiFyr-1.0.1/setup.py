import setuptools

setuptools.setup(
    name='QualiFyr',
    version='1.0.1',
    description='Package to read in output files relating to quality and assess overall pass/fail.',
    long_description='See https://gitlab.com/cgps/qualifyr for more details',
    author='Anthony Underwood',
    author_email='au3@sanger.ac.uk',
    license='MIT',
    packages=setuptools.find_packages(),
    scripts=['scripts/qualifyr'],
    install_requires=['colorlog'],
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    classifiers=[ 
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)