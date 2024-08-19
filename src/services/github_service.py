import logging

from github import Github
from main import REPOSITORY_NAME

def get_repo_from_token(token):
    """Get user details based on provided token"""
    try:
        g = Github(token)
        user = g.get_user()
        
        logging.debug(f"Trying to get repo with token of user: {user.login}, {user.name}, {user.email}...")

        return g.get_repo(f"{user.login}/{REPOSITORY_NAME}")
    except Exception as e:
        logging.error(f"Failed to get repo from provided token: {str(e)}")
        return None


def get_github_data(token):
    """Get repository data from a provided github token"""
    try:
        repo = get_repo_from_token(token)
        if repo is None:
            return None
        
        logging.debug("Repo fetched successfully, begin to manipulate data...")

        # Get latest 3 releases, if their amount is larger than 2
        releases = repo.get_releases()
        if len(releases) < 3:
            logging.error(f"Repository {REPOSITORY_NAME} has less than 3 releases.")
        else:
            releases = releases[:3]
        
        latest_releases = [release.tag_name for release in releases]
        forks = repo.forks_count
        stars = repo.stargazers_count
        contributors = repo.get_contributors().totalCount
        prs = repo.get_pulls(state='all')
        prs_count = prs.totalCount

        logging.debug("Begin to manipulate PRs per contributor username...")

        # Get the contributor's PR count and sort them in descending order
        pr_count_dict = {}
        for pr in prs:
            user = pr.user.login
            pr_count_dict[user] = pr_count_dict.get(user, 0) + 1
        
        sorted_contributors = sorted(pr_count_dict.items(), key=lambda item: item[1], reverse=True)

        return {
            'latest_releases': latest_releases,
            'forks': forks,
            'stars': stars,
            'contributors': contributors,
            'pull_requests': prs_count,
            'sorted_contributors': sorted_contributors
        }
    except Exception as e:
        logging.error(f"Failed to get github data from token: {str(e)}")
        return None

