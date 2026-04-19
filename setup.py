'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
    of your project, such as its metadata, dependencies, and more
    '''
from setuptools import find_packages,setup
from typing import List
def get_requirements()->list[str]:
    requirements_list:list[str]=[]
    try:
        with open('requirements.txt','r') as file:
            readlines=file.readlines()
            for line in readlines:
                requirements=line.strip()
                    ##basically strip function removes all the spaces
                if requirements and requirements!="-e .":
                    requirements_list.append(requirements)
    except FileNotFoundError:
         print('requirements not found error')
    return requirements_list


    setup(
     name="Heart disease prediction",
     version="0.0.1",
     author='zaid',
     author_email='zaidbichu@4gmail.com',
     packages=find_packages(),
     install_requirements=get_requirements()
    )
        
        
        



