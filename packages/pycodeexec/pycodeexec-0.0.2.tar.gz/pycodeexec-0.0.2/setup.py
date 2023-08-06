from setuptools import setup

try:
    long_description = open("README.md").read()
except:
    long_description = ""

setup(
    name='pycodeexec',
    version='0.0.2',
    description='Execute arbitrary code from a multitude of supported languages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/3jackdaws/pycodeexec',
    author='Ian Murphy',
    author_email='3jackdaws@gmail.com',
    license='MIT',
    packages=['pycodeexec'],
    python_requires='>=3.6',
    install_requires=['docker', 'asgiref'],
    test_suite='nose.collector',
    tests_require=['asynctest', 'nose'],
)