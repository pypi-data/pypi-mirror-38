INSTALL_REQUIRES = [
    'numpy>=1.9.3',
    'pandas>=0.15.2',
    'matplotlib>=1.4.3']

long_description = "Welcome to Periscopy - a home for beautiful visualizations."

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup


if __name__ == "__main__":
    setup(
        name="periscopy",
        version="0.0.87",
        author="Christine Quan",
        author_email="christine.quan11@gmail.com",
        description="periscopy: business data visualization",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/christinequan/periscopy",
        install_requires=INSTALL_REQUIRES,
        packages=['periscopy'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
