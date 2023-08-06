from setuptools import setup

setup(
    name='aat_poc',
    version='0.1',
    description='AAT proof of concept',
    author='Debo Akeredolu',
    author_email='debola31@gmail.com',
    license='MIT',
    packages=['aat_poc'],
    install_requires=[
        'requests',
        'cryptography',
        'datetime',
        'flask'
    ],
    zip_safe=True
)