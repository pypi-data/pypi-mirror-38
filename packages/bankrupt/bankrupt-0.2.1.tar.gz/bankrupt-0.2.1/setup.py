from setuptools import setup


setup(
    name='bankrupt',
    version=__import__('bankrupt').__version__,
    description="Allocator of the bankruptcy problem.",
    long_description=open("README.md").read(),
    author='qx3501332',
    author_email='x.qiu@qq.com',
    license="MIT License",
    url='https://github.com/xianqiu/Bankrupt',
    packages=['bankrupt'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)