from setuptools import find_packages, setup

setup(
    name="exportme",
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    license="MIT License",
    description="Miscellaneous exporters",
    url="https://github.com/kfdm/misc-exporters",
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
    install_requires=[
        "dj_database_url",
        "Django==2.1.3",
        "envdir",
        "prometheus_client==0.4.2",
        "python-dateutil",
        "pytz",
        "raven",
        "requests",
    ],
    extras_require={"dev": ["unittest-xml-reporting"], "postgres": ["psycopg2"]},
    entry_points={
        "console_scripts": ["exportme = exportme.standalone.manage:main"],
        "exportme.exporters": [
            "currency = exportme.exporters.currency:Currency",
            "rescuetime = exportme.exporters.rescuetime:RescueTime",
            "wanikani = exportme.exporters.wanikani:VersionOne",
        ],
    },
)
