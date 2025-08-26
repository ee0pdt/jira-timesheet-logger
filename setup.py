#!/usr/bin/env python3

from setuptools import setup

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jira-timesheet-logger",
    version="1.0.0",
    author="Pete Thorne",
    author_email="your-email@example.com",
    description="A Python tool for logging timesheet data to Jira via REST API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/petethorne/jira-timesheet-logger",
    py_modules=["log-timesheet"],
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "jira-timesheet-logger=log-timesheet:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Tools",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.6",
    keywords="jira timesheet logging api automation",
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", ".env.example"],
    },
)