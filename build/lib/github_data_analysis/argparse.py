import argparse

def setup_arguments():
    """Setup arguments used for program logic. """
    parser = argparse.ArgumentParser(description='GitHub Data Analysis')
    parser.add_argument('--token', required=True, help='GitHub token')
    parser.add_argument('--log-to-file', action='store_true', help='Log to file instead of stdout')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--branch', help='Choose a branch to create commit graph', default='mark-3.7.3')

    return parser.parse_args()