from setuptools import setup
from setuptools import find_packages

setup(name="mambas",
      version="0.1.2",
      description="Mambas is a web based visualization tool to manage your Keras projects and monitor your training sessions.",
      author="Kevin Beck",
      author_email="misterkevinski@gmail.com",
      url="https://github.com/misterkevinski/mambas",
      license="MIT",
      include_package_data=True,
      install_requires=["bottle", "paste", "keras"],
      packages=find_packages(),
      entry_points={"console_scripts": ["mambas = mambas.server.__main__:main"]}
)