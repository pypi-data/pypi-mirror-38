from setuptools import setup

setup(
    name="brevis",
    version="0.5.2",
    description="Python client for the Brevis URL shortener API",
    url="http://github.com/admiralobvious/brevis-python-client",
    author="Alexandre Ferland",
    author_email="aferlandqc@gmail.com",
    license="MIT",
    packages=["brevis"],
    zip_safe=False,
    install_requires=["requests>=2.12"],
    tests_require=[
        "pytest>=4.0.0",
        "requests-mock>=1.5.2"
    ],
    setup_requires=["pytest-runner>=4.2"],
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
