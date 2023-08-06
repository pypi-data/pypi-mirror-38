import setuptools

setuptools.setup(
    name="pytest-libnotify",
    version="1.0.0",
    url="https://github.com/moser/pytest-libnotify",

    author="Martin Vielsmaier",
    author_email="moser@moserei.de",

    description="Pytest plugin that shows notifications about the test run",
    long_description=open('README.md').read(),
    keywords=[],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    setup_requires=['pytest-runner'],
    tests_require=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'pytest11': ['notifier = pytest_libnotify'],
    },
)
