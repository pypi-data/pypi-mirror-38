import setuptools

with open('README', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='uniflash',
    version='1.0',
    description='Reflash Logitech Unifying Receivers easily',
    long_description=long_description,
    author='athn',
    author_email='jem@seethis.link',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyusb',
        'intelhex',
        'hexdump'
    ]
)
