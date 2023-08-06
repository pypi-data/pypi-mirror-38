from setuptools import setup, find_packages

setup(
    name='wagtail-peregrine',
    version="0.2.3",
    description='Stub to alias the `peregrine` package.',
    author='Tim Allen',
    author_email='tallen@wharton.upenn.edu',
    url='https://github.com/FlipperPA/peregrine',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'peregrine',
    ],
)
