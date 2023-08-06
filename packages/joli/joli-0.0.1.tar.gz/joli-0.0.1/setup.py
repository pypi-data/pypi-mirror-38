from distutils.core import setup

setup(
    name="joli",
    version="0.0.1",
    description="Joli notebooks",
    author="Tim Head",
    author_email="betatim@gmail.com",
    packages=["joli"],
    install_requires=["black"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["joli = joli.app:main"]},
)
