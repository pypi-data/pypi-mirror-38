import setuptools

description = "BananaPY - BananAPI Lib for Python"
long_description = open("README.md").read()
version="1.1.0"

packages = ['bananapy']

setuptools.setup(
    name='BananaPY',
    version=version,
    description=description,
    long_description=long_description,
    url='https://github.com/bananaboy21/bananapy',
    author='dat banana boi',
    author_email='kang.eric.hi@gmail.com',
    license='MIT',
    packages=packages,
    include_package_data=True,
    install_requires=['aiohttp>=2.0.0']
)