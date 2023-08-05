import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Emotion_recognition",
    version="1.0.2",
    author="Iván Opitz, Diego Lazcano, Nicolas Fredes",
    author_email="ivan.opitz.13@sansano.usm.cl",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/opitz94/Emotion_recognition",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)