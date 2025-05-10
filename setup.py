from setuptools import setup, find_packages

setup(
    name="FourCutPhoto",
    version="0.1.0",
    description="takes FourCut Photo",
    author="ehrl1234",
    author_email="wjdwntls1225@naver.com",
    packages=find_packages(include=["FourCutPhoto", "FourCutPhoto.*"]),
    include_requires=[
        "PyQt6",
        "opencv-python",
        "numpy"
    ],
    entry_points={
        'console_scripts': [

        ]
    }
)

