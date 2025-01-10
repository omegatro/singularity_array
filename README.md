# EDR

### Introduction
- This repository serves as a registry for external dependencies (EDR) included in bioinformatics pipelines.
- Anyone intending to add a tool to a pipeline or alter the state of an included tool should document the procedure in this repository by submitting a pull request.
- The information in EDR is used for automatic building, testing, and deployment of images on compute resources running the local pipelines, as well as the ground truth for tool version information in the data warehouse.

### Dependencies
- python>=3.12
- conda
- mamba
- singularity
- pip:
  - pyyaml

### Usage
- `global_tool_registry.yaml` is used to manage tool metadata.
- Every tool in the registry is defined with the following attributes:
  ```
  tool_name: <my_tool_name>
  tool_version: <my_tool_version>
  tool_source: <e.g. a GitHub repository>
  tool_hash: <SHA256> OR NULL
  tool_publication: DOI OR link
  image_reference: 
    <docker://repository/name:version> OR
    <singularity_recipes/tool_version.recipe>
  db_hash: <SHA256> OR NULL
  db_ref: <link_to_db_file(s)> OR NULL
  ```
- `NULL` values are allowed for database attributes if tools do not use stand-alone databases.
- For details on how to calculate SHA256 hash values on individual files and directories, please consult the following links:
  - [Hash on files](https://www.baeldung.com/linux/sha-256-from-command-line)
  - [Hash on directories](https://worklifenotes.com/2020/03/05/get-sha256-hash-on-a-directory/)
- **All included tools must be available as either**:
  - An official Docker image (for example [RGI](https://hub.docker.com/r/finlaymaguire/rgi)).
  - A custom Singularity recipe based on a conda environment (see `singularity_recipes` directory).
    - For details on how to pull Docker images with Singularity and how to write Singularity recipes, please consult the [Singularity documentation](https://docs.sylabs.io/guides/3.2/user-guide/index.html). Some examples are available in the `singularity_recipes` folder.

### Building Images
- Using `build_images_loop.sh`, it is possible to automatically build Singularity images from tools published as conda packages on a system with `sudo` permission level.
- The input to the script is a CSV file with no header, e.g.:
  ```
  kraken2,2.1.3
  ectyper,2.0.0
  seqsero2,1.3.1
  sistr_cmd,1.1.3
  stecfinder,1.1.2
  ```
  - **The trailing line must be left empty.**
  - It is possible to check if all requested tools are available in conda repositories before building, e.g.: 
    ```
    ./search_images_loop.sh tool_list.csv
    # The mamba_search_results.tsv file will contain information about each tool or indicate if it was not found.
    ```
  - Once the list of tools and versions is validated and refined, the build can be run with the following command:
    ```
    ./build_images_loop.sh tool_list.csv
    ```

  - **Notes & Tips**:
    - The building process requires `sudo` access and the packages mentioned in [Dependencies](#dependencies) installed.
    - It is safer to run it under a `screen` instance, as the build can take quite a bit of time.
    - The build process is RAM and CPU-intensive and can fail if resources are lacking.
    - Additional configuration is possible - see `toggles` in `build_images_loop.sh` lines 19-28.

### Adding New Images to the Registry
- `global_tool_registry.yaml` requires that tools be added in the [Form](#usage).
- If the `build_images_loop.sh` script was used to construct specific images, it is possible to generate the basic template pre-filled with some information automatically.
- The `tool_registry.py` script parses the `singularity_recipes` folder and creates a `tool_registry.yaml` file for any `sif` files found there.
  - The script pre-fills the following attributes:
    ```
    image_reference: <exact>
    tool_hash: <exact>
    tool_name: <exact>
    tool_source: <potential>
    tool_version: <exact>
    ```
  - `<exact>` values can be trusted as correct.
  - `<potential>` values require double-checking as they are the script's best attempt to find the correct GitHub repository, but they can be wrong.
  - Other fields need to be filled manually, and the resulting new registry entries can then be appended to `global_tool_registry.yaml`.
  - Updates must be submitted as a pull request.
  - Custom-built images can and should be added as well.
