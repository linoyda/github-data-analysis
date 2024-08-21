# GitHub Data Analysis

This project is a Python-based tool that uses the GitHub API to analyze data from a GitHub repository and generate visual representations of branch commit histories. The project focuses on extracting specific information from the GitHub repository, such as the latest releases, number of forks, stars, contributors, and pull requests. It also allows you to visualize the commit history of a branch, including the point of divergence from the main branch and the merge commit, if any.

## Features
#### Data Extraction:
 * Fetch latest 3 releases of the CTFd repository.
 * Number of forks, stars, contributors, and prs in the CTFd repository.
 * List of contributors ordered by the number of pull requests in descending order.

#### Commit Graph Generation:
 * Creates a graph showing the commit history of a specified branch.
 * Visualizes the divergence point from the main branch and the merge commit.
 * Outputs the graph in .dot format for further processing or visualization. Please see the ```output_example``` directory for a visual example.

## Prerequisites
1. Python 3.x (3.12 preferred)
2. [PyGithub](https://github.com/PyGithub/PyGithub) library for GitHub API access
3. [pydot](https://github.com/pydot/pydot) and [graphviz](https://graphviz.org/download/) libraries for graph generation
4. A valid GitHub personal access token
5. [argparse](https://docs.python.org/3/library/argparse.html)
6. [logging](https://docs.python.org/3/library/logging.html)

## Usage
### Running the Script
To run the script, use the following command:

```python main.py --token="your_github_token" --branch="branch_name" --log-to-file --debug```

```--token```: (**Required**) Your GitHub personal access token.
```--branch```: (**Optional**. If not provided, will fallback to ```mark-3.7.3```) The name of the branch for which you want to generate the commit graph.
```--log-to-file```: (**Optional**) Option to log output to a file instead of stdout.
```--debug```: (**Optional**) Enable debug mode for more detailed logging.

#### Example

```python main.py --token="ghp_yourtoken" --branch="feature-branch" --log-to-file --debug```

### Viewing the Graph
After running the script, the graph will be saved as a ```.dot``` file named after the branch (e.g., {branch_name}_commit_graph.dot). You can visualize the graph using Graphviz:

```dot -Tpng {branch_name}_commit_graph.dot -o OUTPUT_FILE_NAME.png```