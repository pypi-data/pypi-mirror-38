from setuptools import find_packages, setup

setup(
    name="annotateme",
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    license="MIT License",
    description="A simple annotation server",
    url="https://github.com/kfdm/annotateme",
    author="Paul Traylor",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
    ],
    install_requires=["Django==2.1.3"],
    extras_require={"standalone": []},
    entry_points={
        "console_scripts": [
            "annotateme = annotateme.standalone.manage:main[standalone]"
        ],
        "annotateme.drivers.read": ["local = annotateme.drivers.local:Local"],
        "annotateme.drivers.write": ["local = annotateme.drivers.local:Local"],
    },
)
