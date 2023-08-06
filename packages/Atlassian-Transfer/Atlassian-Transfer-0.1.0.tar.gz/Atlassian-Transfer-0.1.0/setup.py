import setuptools

try:
    from atlassian_transfer import __version__ as version
except ImportError:
    import re
    pattern = re.compile(r"__version__ = '(.*)'")
    with open('atlassian_transfer.py') as f:
        version = pattern.search(f.read()).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='Atlassian-Transfer',
    version=version,
    author='Dave Chevell',
    author_email='chevell@gmail.com',
    description='An API wrapper for transfer.atlassian.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/dchevell/atlassian-transfer',
    packages=setuptools.find_packages(),
    keywords=['requests', 'transfer', 'atlassian'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=['requests-toolbelt'],
#     tests_require=[],
#     test_suite='tests',
#     cmdclass={
#         'test': pytest
#     }
)
