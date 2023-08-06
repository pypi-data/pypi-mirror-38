import setuptools


setuptools.setup(
    name="ctrlf",
    version="0.0.2",
    author="theunderdog",
    author_email="ahmedbonumstelio@gmail.com",
    packages=setuptools.find_packages(),
    description="A better solution to find files/directories on your computer uesing their name or regular expression",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts':['ctrlf=ctrlf.command:command_main']
        }
)
