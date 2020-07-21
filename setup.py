from setuptools import setup, find_packages


with open('requirements.txt') as reqbuf:
    requirements = reqbuf.read()


setup(
    name='WindsorCLI',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'windsor=windsor.cli:run'
        ]
    },
    install_requires=requirements,
    include_package_data=True,
    author='Westpoint'
)
