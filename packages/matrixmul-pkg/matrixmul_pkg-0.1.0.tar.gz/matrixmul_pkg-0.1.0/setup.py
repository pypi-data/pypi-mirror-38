# Date 2018/11/19
# WQ
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'matrixmul_pkg',
    version = '0.1.0',
    author = 'Qing Shen',
    author_email = 'wangqing19890117@163.com',
    description = 'An example for teaching how to publish a Python package',
    long_description = long_description,
    packages = setuptools.find_packages(),
)