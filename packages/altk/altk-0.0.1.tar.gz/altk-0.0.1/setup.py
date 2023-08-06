from setuptools import setup, find_packages

setup(
    name='altk',
    url='https://github.com/ancient-lives/altk',
    author='Alex Williams',
    author_email='alex.williams@uwaterloo.ca',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    keywords='ancient-lives',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'tqdm==4.28.1',
    ],
)
