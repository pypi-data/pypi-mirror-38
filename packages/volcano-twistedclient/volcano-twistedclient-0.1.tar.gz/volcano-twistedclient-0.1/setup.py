from setuptools import setup

with open('requirements.txt') as f:
    requires = list(filter(lambda x: not not x, map(lambda x: x.strip(), f.readlines())))

setup(
    name='volcano-twistedclient',
    version='0.1',
    description='Volcano client for Twisted',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.twistedclient'],
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
