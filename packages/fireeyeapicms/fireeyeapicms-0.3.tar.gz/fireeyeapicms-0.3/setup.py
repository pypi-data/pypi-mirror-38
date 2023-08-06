from setuptools import setup
with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name='fireeyeapicms',
    version='0.3',
    packages=[
        "fireeyeapicms",
    ],
    license='MIT',
    long_description=long_description,
    url="https://github.com/aaronjonen/fireeyeapi",
    author="aaron jonen",
    author_email="aaron.jonen@nexteraenergy.com",
    install_requires=[
       "requests",
        "urllib3"
    ],
    include_package_data=True,
    zip_safe=False
)