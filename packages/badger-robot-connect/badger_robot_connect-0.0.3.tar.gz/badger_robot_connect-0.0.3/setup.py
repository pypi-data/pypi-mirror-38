import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='badger_robot_connect',
    version='0.0.3',
    author='Tommy Vandermolen',
    author_email='tommy.vandermolen@gmail.com',
    description='Wireless Control Client for BADGER Robot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
