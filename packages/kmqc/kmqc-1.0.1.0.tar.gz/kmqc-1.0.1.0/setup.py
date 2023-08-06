import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='kmqc',
    version='1.0.1.0',
    author='Rustam Sayfutdinov',
    author_email='rstm-sf@gmail.com',
    description='A package for client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/rstm-sf/pykmqc',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
