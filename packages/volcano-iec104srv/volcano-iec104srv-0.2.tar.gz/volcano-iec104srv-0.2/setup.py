from setuptools import setup

with open('requirements.txt') as f:
    requires = list(filter(lambda x: not not x, map(lambda x: x.strip(), f.readlines())))

setup(
    name='volcano-iec104srv',
    version='0.2',
    description='IEC60870-5-104 server for Volcano',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.iec104srv'],
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
