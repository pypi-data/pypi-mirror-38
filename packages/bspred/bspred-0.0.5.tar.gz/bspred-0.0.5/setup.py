import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="bspred",
                 version="0.0.5",
                 author="Yiwen Wang",
                 author_email="yiwenwang9702@gmail.com",
                 
                 description="Prediction of bike sharing usage.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/jasonyiww/bspred",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 package_data={
                 'bspred':['*.csv','*.h5','city_data/*.csv'],
                 },
                 install_requires=['keras']
                 )
