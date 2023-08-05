from setuptools import setup, find_packages


requirements = [
    "umihico",
    "lxml",
]


def _version_increment():
    with open('version.txt', 'r') as f:
        version = int(float(f.read()))
    version += 1
    version = str(version)
    with open('version.txt', 'w') as f:
        f.write(version)
    version = '.'.join(str(version).zfill(3))
    return version


setup(
    name='minigun',
    version=_version_increment(),
    description="Web scraping API to outsource tons of GET & xpath to cloud computing",
    url='https://github.com/umihico/minigun-requests',
    author='umihico',
    author_email='umihico_dummy@users.noreply.github.com',
    license='MIT',
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='umihico minigun web scraping requests lxml proxy threading multiprocessing aws cloud lambda',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
