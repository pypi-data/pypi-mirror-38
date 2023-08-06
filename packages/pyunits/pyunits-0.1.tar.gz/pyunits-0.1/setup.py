from distutils.core import setup

PACKAGE = ""
NAME = ""
DESCRIPTION = ""
AUTHOR = ""
AUTHOR_EMAIL = ""
URL = ""
#VERSION = __import__(PACKAGE).__version__
 
setup(
    name="pyunits",
    py_modules=['pyunits'],
    version="0.1",
    description="capcity units convert",
    long_description="",
    author="PoplarYang",
    author_email="echohiyang@gmail.com",
    license="BSD",
    url="https://github.com/PoplarYang",
    #packages=find_packages(exclude=["tests.*", "tests"]),
    #package_data=find_package_data(
    #        PACKAGE,
    #        only_in_packages=False
    #      ),
#    classifiers=[
#        "Development Status :: 3 - Alpha",
#        "Environment :: Web Environment",
#        "Intended Audience :: Developers",
#        "License :: OSI Approved :: BSD License",
#        "Operating System :: OS Independent",
#        "Programming Language :: Python",
#        "Framework :: Django",
#    ],
#    zip_safe=False,
)
