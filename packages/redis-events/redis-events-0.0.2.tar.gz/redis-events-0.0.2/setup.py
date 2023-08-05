from setuptools import setup

try:
    long_description = open("README.md").read()
except:
    long_description = ""


setup(
    name='redis-events',
    description="Event based distributed computing using Redis and asyncio",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/3jackdaws/redis-events",
    author="Ian Murphy",
    author_email="3jackdaws@gmail.com",
    version='0.0.2',
    packages=['redis_events',],
    license='MIT',
    install_requires=[
        "aioredis",
    ],
    tests_require=[
        "pytest",
        "pytest-asyncio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)