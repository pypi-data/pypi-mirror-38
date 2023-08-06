from setuptools import setup

with open('requirements.txt') as f:
    requires = list(filter(lambda x: bool(x), map(lambda x: x.strip(), f.readlines())))

setup(
    name='volcano-arch',
    version='1.1',
    description='Archiver satellite for Volcano',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.arch'],
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
