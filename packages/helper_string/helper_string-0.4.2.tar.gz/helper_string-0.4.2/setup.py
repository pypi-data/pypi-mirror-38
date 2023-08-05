try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='helper_string',
    version='0.4.2',
    url='https://github.com/OpenGroper/helper_string',
    license='MIT License',
    author='Shuge Lee',
    author_email='shuge.lee@gmail.com',
    description='String Helper',

    packages = [
        "helper_string",
    ],
    test_suite ="helper_string.tests",
)
