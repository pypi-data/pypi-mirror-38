import setuptools
f = open("README.txt", "r")
setuptools.setup(name="hfble", version="2.0", 
packages=["hfble"], license="MIT License", long_description=(f.read(), f.close())[0])
