from setuptools import setup, find_packages


with open('requirements.txt') as reqbuf:
    requirements = reqbuf.read()

with open('README.md') as readmebuf:
    readme = readmebuf.read()

setup(
    name='windsor',
    version='0.5',
    packages=find_packages(),
    description='Bootstrap your AWS CDK project resources by running CLI commands',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/westpoint-io/windsor',
    entry_points={
        'console_scripts': [
            'windsor=windsor.cli:run'
        ]
    },
    install_requires=requirements,
    include_package_data=True,
    author='Westpoint',
    python_requires='>=3.6'
)
