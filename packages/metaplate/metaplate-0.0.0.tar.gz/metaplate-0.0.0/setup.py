from setuptools import find_packages, setup

setup(
    name='metaplate',
    version='0.0.0',
    description='Automatic generation of metaformat templates.',
    url='https://gitlab.com/wefindx/metaplate',
    author='Mindey',
    author_email='mindey@qq.com',
    license='ASK FOR PERMISSIONS',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False
)
