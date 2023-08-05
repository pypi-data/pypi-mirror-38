import csv
from lxml import html
import requests
import pkg_resources

SOURCES_LIST = pkg_resources.resource_filename('satellite_tle', 'sources.csv')


def get_tle_sources():
    '''
    Returns a list of (source, url)-tuples for well-known TLE sources.
    '''

    sources = []

    with open(SOURCES_LIST) as csvfile:
        csv_reader = csv.reader(csvfile,
                                delimiter=',',
                                quotechar='\'',
                                quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            source, url = row
            sources.append((source, url))

    return sources


def fetch_tle_from_celestrak(norad_cat_id):
    '''
    Returns the TLE for a given norad_cat_id as currently available from CelesTrak.
    Raises IndexError if no data is available for the given norad_cat_id.
    '''

    r = requests.get('https://www.celestrak.com/satcat/tle.php?CATNR={}'.format(norad_cat_id))
    page = html.fromstring(r.text)

    tle = page.xpath('//pre/text()')[0].split('\n')
    if tle[1].strip() == 'No TLE found':
        raise LookupError

    return tle[1].strip(), tle[2].strip(), tle[3].strip()


def fetch_tles_from_url(url):
    '''
    Downloads the TLE set from the given url.
    Returns a dictionary of the form {norad_id1: tle1, norad_id2: tle2} for all TLEs found.
    tleN is returned as list of three strings: [satellite_name, line1, line2].
    '''

    r = requests.get(url)

    tles = dict()
    lines = r.text.splitlines()
    assert(len(lines) % 3 == 0)

    # Group every three lines
    line_groups = zip(*(iter(lines),) * 3)

    for group in line_groups:
        print(group)
        assert(group[1][0] == '1')
        assert(group[2][0] == '2')

        norad_cat_id = int(group[1][2:7].encode('ascii'))
        tles[norad_cat_id] = (group[0].strip(), group[1], group[2])

    return tles
