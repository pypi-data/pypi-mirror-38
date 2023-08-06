import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quat_to_euler",
    version="2018.11.20",
    author="Javier Gonzalez Alonso",
    author_email="javigonzauva@gmail.com",
    description="Adds a quaternion to Euler Unity-like convention method to NumPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javigonzalo/quat_to_euler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)