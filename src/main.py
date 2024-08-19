import logging

from config.logger import setup_logging
from config.argparse import setup_arguments
from services.github_service import get_github_data
from services.graph_service import create_commit_graph


def main():
    """Driver function logic for collecting repository data and creating a graph for a given branch"""
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
        create_commit_graph(args.token, args.branch)

    except Exception as e:
        logging.critical(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    main()