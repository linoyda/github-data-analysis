import logging

from github_data_analysis.logger import setup_logging
from github_data_analysis.argparse import setup_arguments
from github_data_analysis.github_service import get_github_data
from github_data_analysis.graph_service import create_branch_graph_from_github


def main():
    """Driver logic for collecting repository data and creating a graph for a given branch"""
    try:
        args = setup_arguments()
        setup_logging(args.log_to_file, args.debug)

        logging.info("Extracting GitHub data...")

        data = get_github_data(args.token)
        if data is None:
            logging.error("Failed to fetch repository data.")
            return

        logging.info(
            f"Latest releases: {data['latest_releases']}\n"
            f"Forks: {data['forks']}\n"
            f"Stars: {data['stars']}\n"
            f"Contributors: {data['contributors']}\n"
            f"Pull Requests: {data['pull_requests']}\n"
            f"Top contributors by pull requests:\n"
        )

        for user, pr_count in data['sorted_contributors']:
            logging.info(f"{user}: {pr_count} PRs")

        logging.info(f"Creating commit graph for branch {args.branch}...")
        
        create_branch_graph_from_github(args.token, args.branch)

    except Exception as e:
        logging.critical(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    main()