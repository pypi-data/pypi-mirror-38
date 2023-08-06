from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(
    name='dvtDecimal',
    version='0.8.4',
    description='Repeating digits of rational numbers',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://twitter.com/davidequantique',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC',
    packages=find_packages()
)
