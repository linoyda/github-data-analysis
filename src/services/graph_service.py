import pydot
import logging

from services.github_service import get_repo_from_token, check_if_branch_merged

def create_branch_graph_from_github(token, branch_name):
    repo = get_repo_from_token(token)
    if repo is None:
        logging.error("Failed to get repo, aborting graph creation")
        return
    
    # Fetch all pull requests
    pull_requests = repo.get_pulls(state='all')
    branch_prs = []

    # Identify pull requests that involve the desired branch
    for pr in pull_requests:
        if pr.head.ref == branch_name:
            branch_prs.append(pr)

    if not branch_prs:
        logging.warning("No pull requests found.")
        return

    # Create the graph
    graph = pydot.Dot(graph_type="digraph")

    for pr in branch_prs:
        # Fetch all commits in the pull request
        commits = list(pr.get_commits())

        # Add PR commits to the graph
        nodes = {}
        for commit in commits:
            node = pydot.Node(f"{commit.sha[:7]}\n{commit.commit.message.splitlines()[0]}",
                              shape="circle", style="filled", fillcolor="lightblue")
            nodes[commit.sha] = node
            graph.add_node(node)

        # Connect PR commits
        for i in range(len(commits) - 1):
            graph.add_edge(pydot.Edge(nodes[commits[i].sha], nodes[commits[i + 1].sha]))

        # Retrieve and add the merge commit node
        pr_merge_commit_sha = pr.merge_commit_sha
        if pr_merge_commit_sha:
            try:
                merge_commit = repo.get_commit(pr_merge_commit_sha)
                merge_node = pydot.Node(f"{merge_commit.sha[:7]}\n{merge_commit.commit.message.splitlines()[0]}",
                                        shape="ellipse", style="filled", fillcolor="lightgreen")
                graph.add_node(merge_node)
                if commits:
                    graph.add_edge(pydot.Edge(nodes[commits[-1].sha], merge_node))
            except Exception as e:
                logging.error(f"Failed to fetch merge commit details for SHA {pr_merge_commit_sha}: {e}")

    # Save the graph to a .dot file
    graph.write_dot(f"{branch_name}_commit_graph.dot")
