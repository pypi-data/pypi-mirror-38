from setuptools import setup

setup(
    name='indexor',
    version='0.1.1',
    description='The best indexor',
    url='https://github.com/kpedrozag/myfirstpkg',
    author='Kevin Pedroza Goenaga',
    author_email='kevinpedroza26@gmail.com',
    license='GNU GPLv3',
    keywords='print indexor message',
    packages=['indexor'],
    package_dir={'indexor': 'indexor'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
