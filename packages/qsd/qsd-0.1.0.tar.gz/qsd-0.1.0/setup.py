from setuptools import setup, find_packages
#from setuptools.command.develop import develop
#from setuptools.command.install import install

setup(
        name="qsd",
        version="0.1.0",
        packages=find_packages(exclude=['*test']),
        author="Gareth Sion Jones",
        author_email="garethsion@googlemail.com",
        project_urls={
            'Documentation': 'https://qsd.readthedocs.io/',
            'Source': 'https://github.com/garethsion/qsd.git',
            },
        python_requires='>3.4.0',
        install_requires=['numpy','scipy']
    )
