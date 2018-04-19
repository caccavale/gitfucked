import logging
import sys

import github
github.Repository.Repository.__hash__ = lambda self: hash(self.full_name)
github.Repository.Repository.__eg__ = lambda self, other: self.full_name == other.full_name

logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 2:
    exit()

with open('token', 'r') as f:
    g = github.Github(f.read().strip('\n'))

dst = g.get_user()
logging.info('Getting stars...')
stars = set(dst.get_starred())
logging.info('...stars got.')

for user in sys.argv[1:]:
    logging.info('Stealing stars from %s' % user)
    src = g.get_user(user)

    logging.info('    precompute boy...')
    diff = set(src.get_starred()) - stars
    logging.info('    ...is done now, diff size is %d.' % len(diff))

    # If you want, filter here. Ex:
    # diff = set(filter(lambda x: x.name.startswith('py'), diff))

    for repo in diff:
        logging.info('      starring %s' % repo.full_name)
        try:
            dst.add_to_starred(repo)
            stars.add(repo)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.warning('      ^ failed on %s with error: %s' % (repo.full_name, e.data.get('message', e)))
