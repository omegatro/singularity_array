# EDR
### Introduction
- This repository is intended to be used as a registry for external dependencies (EDR) that are included in NMRL bioinformatics pipelines.
- Anyone with intention to add a tool to a pipeline, or alter the state of an included tool, should document the procedure in this repository by submitting a pool request.
- The information in EDR is planned to be used for automatic building, testing and deployment of the images on compute resources running the NMRL pipelines, as well as the ground truth for tool version information in the data warehouse.
### Dependencies
```
- python>=3.12
- conda
- mamba
- singularity
- pip:
  - pyyaml
```
### Usage
- `global_tool_registry.yaml` is used to manage tool metadata.
- Every tool in the registry is defined with the following attributes:
```
tool_name: <my_tool_name>
tool_version: <my_tool_version>
tool_source: <e.g. a github repository>
tool_hash: <SHA256> OR NULL
tool_publication: DOI OR link
image_reference: 
  <docker://repository/name:version> OR
  <singularity_recipes/tool_version.recipe>
db_hash: <SHA256> OR NULL
db_ref: <link_to_db_file(s)> OR NULL
```
- `NULL` values are allowed for database attributes if tools do not use stand-alone databases.
- For details on how to calculate SHA256 hash value on individual files and directories, please consult the following links:
    - [Hash on files](https://www.baeldung.com/linux/sha-256-from-command-line)
    - [Hash on directories](https://worklifenotes.com/2020/03/05/get-sha256-hash-on-a-directory/)
- **All included tools  must be available as either**:
    - An official Docker image (for example [RGI](https://hub.docker.com/r/finlaymaguire/rgi)).
    - A custom singularity recipe based on conda environment 
    (see `singularity_recipes` directory).
        - For details on how to pull docker images with singularity, and on how to write singularity recipes,
        please consult [singularity documentation](https://docs.sylabs.io/guides/3.2/user-guide/index.html) and GPT4. Some examples are available in `singularity_recipes` folder.
- **Building images**
  - Using `build_images_loop.sh` it is possible to automatically build `singularity images` from tools published as `conda` packages, on a system with `sudo` permission level.
  - The input to the script is a `csv` file with no header, e.g.:
```
kraken2,2.1.3
ectyper,2.0.0
seqsero2,1.3.1
sistr_cmd,1.1.3
stecfinder,1.1.2

```
  - **Trailing line must be left empty.**
  - It is possible to check if all requested tools are available in conda repositories before building, e.g.: 
  ```
  ./search_images_loop.sh tool_list.csv
  # mamba_search_results.tsv file will contain information about each 
  # tool, or if it was not possible to find it.
  ```
 
  - Once the list of tools and versions was validated and refined, build can be run with the following command:
  ```
  ./build_images_loop.sh tool_list.csv
  ``` 

  - **Notes & tips**:
    - The building process requires `sudo` access, and packages mentioned in [Dependencies](#dependencies) installed.
    - It is safer to run it under `screen` instance, as build can take quite a bit of time.
    - Build process is RAM&CPU-intensive, and can fail if resources are lacking.

  - **Adding new images to the registry**
    - `global_tool_registry.yaml` requires that tools to be added in the [Form](#usage). 
    - If the `build_images_loop.sh` script was used to construct specific images, it is possible to generate the basic template pre-filled with some information automatically.
    - `tool_registry.py` script parses `singularity_recipes` folder and creates `tool_registry.yaml` file for any `sif` files found there.
      - The script pre-fills the following attributes:
      ```
        image_reference: <exact>
        tool_hash: <exact>
        tool_name: <exact>
        tool_source: <potential>
        tool_version: <exact>
      ```
      - `<exact>` - values `can be trusted as correct`
      - `<potential>` - `double-check is required` - values are script's best attempt to find the correct github repository, but it can be wrong
      - Other fields need to be filled manually and the resulting new registry entires can then be appended to global_tool_registry.yaml.
      - `Update must be submitted as Pool Request`.