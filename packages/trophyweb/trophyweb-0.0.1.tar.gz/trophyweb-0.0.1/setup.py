import setuptools

VERSION = "0.0.1"

setuptools.setup(
    name="trophyweb",
    packages=setuptools.find_packages(),
    package_data={"trophyweb": ["static/*"]},
    version=VERSION,
    description="Trophy Case App for All-Inspiration",
    author="Hugo Wainwright",
    author_email="wainwrighthugo@gmail.com",
    url="https://github.com/frugs/allin-web",
    keywords=["sc2", "trophy"],
    classifiers=[],
    install_requires=["flask"],
)
