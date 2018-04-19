import logging
import sys

import github

logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 2:
    exit()

with open('token', 'r') as f:
    g = github.Github(f.read().strip('\n'))

dst = g.get_user()
logging.info('Getting stars...')
stars = {repo.full_name for repo in dst.get_starred()}
logging.info('...stars got.')


# Define the qualifications upon which to filter here.
def is_interesting(repo):
    return repo not in stars


for user in sys.argv[1:]:
    logging.info('Stealing stars from %s' % user)
    src = g.get_user(user)

    # Misuse of a generator to make this a one liner:
    for repo in filter(is_interesting, src.get_starred()):
        logging.info('      starring %s' % repo.full_name)
        try:
            dst.add_to_starred(repo)
            stars.add(repo)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.warning('      ^ failed on %s with error: %s' % (repo.full_name, e.data.get('message', e)))
