"""Project packaging configuration."""

from setuptools import find_packages, setup


def get_requirements() -> list[str]:
    requirements_list: list[str] = []
    try:
        with open("requirements.txt", "r", encoding="utf-8") as file:
            for line in file:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt not found")
    return requirements_list


setup(
    name="heart_disease",
    version="0.0.1",
    author="zaid",
    author_email="zaidbichu@4gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
        
        
        


