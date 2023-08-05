import setuptools

VERSION = "0.0.4"

setuptools.setup(
    name="allintrophy",
    packages=setuptools.find_packages(),
    package_data={"allintrophy": ["static/*"]},
    version=VERSION,
    description="Trophy Case App for All-Inspiration",
    author="Hugo Wainwright",
    author_email="wainwrighthugo@gmail.com",
    keywords=["sc2", "trophy"],
    classifiers=[],
    install_requires=["flask"],
)
