from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed ... fail
    raise


def prybahr_dummy_func(p):
    print('in prybahr_dummy_func(%s)' % (p,))
