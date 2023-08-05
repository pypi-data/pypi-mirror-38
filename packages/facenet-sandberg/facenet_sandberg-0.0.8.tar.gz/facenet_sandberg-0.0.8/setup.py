from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='facenet_sandberg',
    version='0.0.8',
    description="Face recognition using TensorFlow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/armanrahman22/facenet',
    packages=find_packages(),
    maintainer='Arman Rahman',
    maintainer_email='armanrahman22@gmail.com',
    include_package_data=True,
    license='MIT',
    python_requires='>=3.4',
    install_requires=[
        'tensorflow>=1.7',
        'tensorlayer==1.7',
        'numpy>=1',
        'mtcnn==0.0.8',
        'pathos',
        'six>=1',
        'scipy>=1',
        'opencv_python>=3.2',
        'matplotlib>=2',
        'Pillow>=5',
        'docker_py>=1',
        'progressbar2>=3',
        'scikit_learn',
        'typing>=3',
        'dask'],
    entry_points={
        'console_scripts': [
            'align_dataset = facenet_sandberg.scripts.align_dataset:cli',
            'generate_pairs = facenet_sandberg.scripts.generate_pairs:cli',
            'validate = facenet_sandberg.scripts.validation.validate:cli',
        ],
    }
)
