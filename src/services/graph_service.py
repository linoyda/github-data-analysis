import pydot
import logging

from services.github_service import get_repo_from_token, check_if_branch_merged

def create_branch_graph_from_github(token, branch_name):
    """Given a Github token and a branch name, fetch its prs, and create a graph based on its commits."""
    
    repo = get_repo_from_token(token)
    if repo is None:
        logging.error("Failed to get repo, aborting graph creation")
        return
    
    branch_prs = []
    try:
        # Identify pull requests that involve the desired branch
        for pr in repo.get_pulls(state='all'):
            if pr.head.ref == branch_name:
                branch_prs.append(pr)

        if not branch_prs:
            logging.warning("No pull requests found.")
            return
        
        # Find the common ancestor between the branch and master
        master_commit = repo.get_branch("master").commit
        branch_commit = repo.get_branch(branch_name).commit
        comparison = repo.compare(base=master_commit.sha, head=branch_commit.sha)
        common_ancestor_sha = comparison.merge_base_commit.sha
        common_ancestor_message = comparison.merge_base_commit.commit.message.splitlines()[0]

        graph = pydot.Dot(graph_type="digraph")

        for pr in branch_prs:
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

            common_ancestor_node = pydot.Node(f"{common_ancestor_sha[:7]}\n{common_ancestor_message}",
                                shape="ellipse", style="filled", fillcolor="pink")
            graph.add_node(common_ancestor_node)

            # Connect the common ancestor (pink node) to the first commit in the branch
            if commits:
                graph.add_edge(pydot.Edge(common_ancestor_node, nodes[commits[0].sha]))
            
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
                    
                    # Connect the common ancestor (pink node) to the merge node
                    graph.add_edge(pydot.Edge(common_ancestor_node, merge_node))
                except Exception as e:
                    logging.error(f"Failed to fetch merge commit details for SHA {pr_merge_commit_sha}: {e}")

        graph.write_dot(f"{branch_name}_commit_graph.dot")
    
    except Exception as e:
        logging.error(f"Failed to create commit graph")


