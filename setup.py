import os
import setuptools


setuptools.setup(
    name='matplotlib_backend_ease',
    version='0.0.1',
    author='Martin Kloesch',
    author_email='martin@kmh-solutions.com',
    description='Example matplotlib backend for rendering in Eclipse EASE',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    url='https://github.com/kmhsonnenkind/ease_matplotlib_backend',
    keywords='matplotlib eclipse EASE',
    packages=['matplotlib_backend_ease'],
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    install_requires=[
        'matplotlib'
    ]
)