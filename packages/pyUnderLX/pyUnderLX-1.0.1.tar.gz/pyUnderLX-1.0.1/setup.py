from setuptools import setup, find_packages


long_description = open('README.md').read()

setup(
    name='pyUnderLX',
    version='1.0.1',
    license='MIT License',
    url='https://github.com/dpjrodrigues/pyUnderLX',
    author='Diogo Rodrigues',
    author_email='dpjrodrigues@gmail.com',
    description='Python library to retrieve information from UnderLX',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pyUnderLX'],
    zip_safe=True,
    platforms='any',
    install_requires=[
        'aiohttp',
      ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
