from setuptools import find_packages,setup
from typing import List
def getrequirements()->List[str]:
    try:
        requirement_list:List[str]=[]
        with open("requirements.txt","r") as file_obj:
            lines=file_obj.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement!="-e .":
                    requirement_list.append(requirement)           
        return requirement_list            
                
    except FileNotFoundError:
        print("requirements.txt not found")

setup(
    name="third_project",
    version="0.0.1",
    author="Shivang",
    packages=find_packages(),
    install_requires=getrequirements()
)

    