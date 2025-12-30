from setuptools import setup, find_packages

setup(
    name="FourCutPhoto",
    version="0.1.0",
    description="takes FourCut Photo",
    author="ehrl1234",
    author_email="wjdwntls1225@naver.com",
    packages=find_packages(include=["FourCutPhoto", "FourCutPhoto.*"]),
    install_requires=[
        "PyQt6",
        "opencv-python",
        "pillow",
        "win32printing"
    ],
    entry_points={
        'console_scripts': [
            "FourCutPhoto=FourCutPhoto.src.main:qt_main"
        ]
    }
)

