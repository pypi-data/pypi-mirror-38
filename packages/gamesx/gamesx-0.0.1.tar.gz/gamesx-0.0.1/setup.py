import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name="gamesx",
	version="0.0.1",
	author="mat",
	author_email="fake@email.lol",
	description="Engine for terminal games",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://repl.it/@mat1/gamesX",
	packages=setuptools.find_packages('xterm'),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)