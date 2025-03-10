import os
from pathlib import Path

project_name='src'
list_folders=[
    f"{project_name}/exception/exception.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logging/logger.py",
    f"{project_name}/logging/__init__.py",
    f"{project_name}/Model/model.py",
    f"{project_name}/Model/__init__.py",
]

for path in list_folders:
    folder_path = Path(path)
    
    folder , file = os.path.split(path)
    
    if folder != "":
        os.makedirs(folder , exist_ok=True)
        
    if (not os.path.exists(folder_path)) or (os.path.getsize(folder_path)==0):
        with open(folder_path, 'w') as f:
            pass
    