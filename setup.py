from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    
    requirement_list: List[str]=[]
    try:
        with open("requirements.txt","r") as f:
            lines = f.readlines()
            
            for line in lines:
                requirement = line.strip()
                
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except Exception as e:
        print(str(e))
        

    return requirement_list

get_requirements()

setup(
    name='Stock Market Prediction',
    version='1.0.0',
    description='A simple stock market prediction model',
    author='Prem Raj',
    author_email="rajp37590@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)