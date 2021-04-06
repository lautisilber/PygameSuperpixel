from setuptools import find_packages, setup

setup(
    name='PygameSuperpixel',
    packages=find_packages(),
    version='0.1.0',
    description='Easy use of pygame to create graphical grids of pixels',
    author='Lautaro Silbergleit',
    license='MIT',
    install_requires=['numpy']
)