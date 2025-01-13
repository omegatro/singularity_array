import os
import yaml
import hashlib
import glob
import sys
import requests

def get_tool_info(sif_path):
    # Extract tool name and version from the file name
    file_name = os.path.basename(sif_path).replace('.sif', '')
    parts = file_name.split('_')
    tool_name = parts[0]
    tool_version = parts[-1]

    tool_info = {
        'tool_name': tool_name,
        'tool_version': tool_version,
        'tool_source': 'https://github.com/example/repo',
        'tool_hash': hashlib.sha256(open(sif_path, 'rb').read()).hexdigest(),
        'tool_publication': None,
        'image_reference': 'conda_based',
        'db_hash': None,
        'db_ref': None
    }

    # Attempt to find the tool's repository on GitHub
    try:
        search_url = f"https://api.github.com/search/repositories?q={tool_name}"
        response = requests.get(search_url)
        if response.status_code == 200:
            search_results = response.json()
            if search_results['total_count'] > 0:
                for item in search_results['items']:
                    if tool_name.lower() in item['name'].lower():
                        tool_info['tool_source'] = item['html_url']
                        break
    except Exception as e:
        print(f"Error occurred while searching for tool repository: {e}")

    return tool_info

def update_tool_registry(singularity_recipes_path, tool_registry_path):
    """
    Updates the tool registry file with information about tools found in the Singularity recipes directory.
    This function traverses the specified Singularity recipes directory to find all `.sif` files,
    extracts tool information from each file, and updates the tool registry file with this information.
    The tool registry is ordered alphabetically by tool name.
    Args:
        singularity_recipes_path (str): The path to the directory containing Singularity recipes.
        tool_registry_path (str): The path to the tool registry file to be updated.
    Raises:
        FileNotFoundError: If the specified Singularity recipes directory does not exist.
        IOError: If there is an error reading from or writing to the tool registry file.
    Example:
        update_tool_registry('/path/to/singularity_recipes', '/path/to/tool_registry.yaml')
    """

    tool_registry = {}

    # Overwrite anything in current file
    open(tool_registry_path, 'w').close()

    # Traverse the singularity_recipes directory using glob
    sif_files = glob.glob(os.path.join(singularity_recipes_path, '**/*.sif'), recursive=True)
    for sif_path in sif_files:
        tool_info = get_tool_info(sif_path)
        tool_registry[tool_info['tool_name']] = tool_info
        
    # Order the tool registry by tool name alphabetically
    ordered_tool_registry = {'tools': sorted(list(tool_registry.values()), key=lambda x: x['tool_name'])}

    header = '''
# This file is used to capture state of external open-source dependencies,
# which are used in bioinformatics pipelines as singularity image files.
# For detailed use instructions see README.md file in this repository.

### Example
# tool_name: <my_tool_name>
# tool_version: <my_tool_version>
# tool_source: <e.g. a github repository>
# tool_hash: <SHA256> OR NULL
# tool_publication: NULL
# image_reference: 
#   <docker://repository/name:version> OR
#   <conda_based> - created from conda definition file using inhouse-adopted procedure
# db_hash: <SHA256> OR NULL
# db_ref: <link_to_db_file(s)> OR NULL

# Description
# This file is used to capture the state of external open-source dependencies,
# which are used in NMRL bioinformatics pipelines as singularity image files.
# For detailed use instructions see README.md file in this repository.
    '''
    
    # Write the updated tool registry to the file
    with open(tool_registry_path, 'w') as file:
        file.write(header)
        file.write('\n')
        yaml.dump(ordered_tool_registry, file, default_flow_style=False)

def create_registry():
    singularity_recipes_path = '../singularity_recipes'
    tool_registry_path = '../tool_registry.yaml'
    update_tool_registry(singularity_recipes_path, tool_registry_path)

if __name__ == "__main__":
    create_registry()
