from setuptools import setup

setup(
    name = "npgamma",
    version = "0.8.2",
    author = "Simon Biggs",
    author_email = "me@simonbiggs.net",
    description = "`npgamma` is deprecated. Please use `gamma` module within the `pymedphys` package instead.",
    long_description = """
`npgamma` is deprecated. A known bug in this version
of `npgamma` is that the evaluation and reference grid
definitions are flipped. This has flow on effects
to parameters such as the `lower_dose_threshold` and
simply swapping evaluation and reference grids may
not achieve the desired results.

`npgamma` is superceded by `pymedphys.gamma`.

To install `pymedphys` see https://pymedphys.com/en/latest/getting-started/installation.html

On usage of the gamma function within `pymedphys` see
https://pymedphys.com/en/latest/user/gamma.html
    """,
    keywords = ["radiotherapy", "gamma evaluation", "gamma index", "distance to agreement", "medical physics"],
    url = "https://github.com/SimonBiggs/npgamma/",
    packages = ["npgamma"],
    license='AGPL3+',
    classifiers = [],
)
