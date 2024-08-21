from setuptools import setup, find_packages

setup(
    name='github_data_analysis',
    version='0.1.0',
    description='A Python package for GitHub data analysis and commit graph creation',
    author='Linoy Davari',
    author_email='linoydavari1997@gmail.com',
    url='https://github.com/linoyda/github-data-analysis',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
        'pydot',
        'graphviz',
    ],
    python_requires='>=3.6',
)