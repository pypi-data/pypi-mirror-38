from setuptools import setup


setup(
    name='lightnimage',
    version='0.0.0.3',
    description='A library to analyze images of lightning strikes',
    url='https://github.com/the16thpythonist/lightnimage',
    author='the16thplayer',
    author_email='jonseb1998@gmail.com',
    license='MIT',
    packages=[
        'lightnimage'
    ],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'jupyter',
        'pillow'
    ],
    python_requires='~=3.6',
    zip_safe=False
)
