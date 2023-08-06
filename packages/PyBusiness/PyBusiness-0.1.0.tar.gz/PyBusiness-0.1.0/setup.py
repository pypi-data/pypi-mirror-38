import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyBusiness",
    version="0.1.0",
    author="J. Nma",
    author_email="wooldoughnutspi@gmail.com",
    description="An easy way to use domesticated utilities for purposes such as business",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://saythanks-com-python-email.webnode.com',
    keywords='personal_use business_use multi-purpose business',
    python_requires='>=3',
    project_urls={
    'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
    'Funding': 'https://donate.pypi.org',
    'Say Thanks!': 'https://saythanks-com-python-email.webnode.com',
    'Source': 'https://saythanks-com-python-email.webnode.com',
    },
    packages=setuptools.find_packages(),
    classifiers=[
	"Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)