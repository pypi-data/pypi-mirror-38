from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='test_nid',
    version='1.0.0',
    description='A tiny, secure, URL-friendly, unique string ID generator for Python.',
    url='https://github.com/aidarkhanov/py-nanoid2',
    author='Dair Aidarkhanov',
    author_email='dairaidarkhanov@gmail.com',
    license='MIT',
    packages=['nanoid', 'dictionary'],
    install_requires=['pytest'],
    include_package_data=True,
    zip_safe=False
)
