import setuptools

with open("README.md", "r") as f:
	setuptools.setup(
	    name="imginit",
	    version="1.0a1",
	    author="issuemeaname",
	    author_email="issuemeaname@gmail.com",
	    description="CLI application for bulk image instantiation with basic feature support",
	    long_description=f.read(),
	    long_description_content_type="text/markdown",
	    url="https://github.com/issuemeaname/imginit",
	    packages=setuptools.find_packages(),
	    classifiers=[
	        "Programming Language :: Python :: 3",
	        "License :: OSI Approved :: MIT License",
	        "Operating System :: OS Independent",
	    ],
	)
