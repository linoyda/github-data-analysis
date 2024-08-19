import pydot
import logging

from services.github_service import get_repo_from_token

def create_commit_graph(token, branch_name):
    """Given a token and a branch name, check if it was merged to master. If so, create a graph from it"""
    repo = get_repo_from_token(token)
    if repo is None:
        logging.error("Failed to get repo, aborting graph creation")
        return
    
    logging.debug("Repo fetched successfully, begin to create graph...")
    branch = repo.get_branch(branch_name)
    # TODO: check if that branch was merged to master. if not, fallback to default?
    
    # Create a graph for commits in the branch
    graph = pydot.Dot(graph_type='digraph')
    commits = repo.get_commits(sha=branch.commit.sha)

    prev_node = None
    for commit in commits:
        node = pydot.Node(commit.sha[:7], label=commit.commit.message[:20])
        graph.add_node(node)
        if prev_node:
            graph.add_edge(pydot.Edge(prev_node, node))
        prev_node = node

    # Write to .dot file
    graph.write_dot(f'{branch_name}_commit_graph.dot')
