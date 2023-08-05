import setuptools
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
    use_cython = True
except ImportError:
    use_cython = False


if use_cython:
    ext_modules = cythonize(['hmm_kit/_hmmc.pyx'])
else:
    ext_modules = [Extension("hmm_kit._hmmc",
                         ["hmm_kit/_hmmc.c"],
                         language='c',
                         library_dirs=['/usr/local/lib'],
                         include_dirs=['/usr/local/include']
                         )]

setuptools.setup(
    name='hmm_kit',
    ext_modules=ext_modules,
    version='0.1',
    description='Python toolkit for unsupervised learning of sequences of observations using HMM',
    author='Eran Rosenthal',
    author_email='eranroz@cs.huji.ac.il',
    url='https://github.com/eranroz/hmm',
    license='MIT License',
    packages=['hmm_kit'],
    install_requires=['matplotlib', 'numpy'],
    scripts=['scripts/simple_hmm.py'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research'
    ]
)
