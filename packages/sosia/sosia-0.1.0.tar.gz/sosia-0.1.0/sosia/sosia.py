#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors:   Michael E. Rose <michael.ernst.rose@gmail.com>
#            Stefano H. Baruffaldi <ste.baruffaldi@gmail.com>
"""Main class for sosia."""

from collections import Counter, defaultdict, namedtuple
from functools import partial
from math import ceil, floor, inf, log
from os.path import exists
from string import digits, punctuation, Template

import pandas as pd
import scopus as sco
from nltk import snowball, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

from sosia.utils import ASJC_2D, FIELDS_SOURCES_LIST

STOPWORDS = list(ENGLISH_STOP_WORDS)
STOPWORDS.extend(punctuation + digits)
_stemmer = snowball.SnowballStemmer('english')


class Original(object):
    @property
    def country(self):
        """Country of the scientist's most frequent affiliation
        in the most recent year (before the given year) that
        the scientist published.
        """
        return self._country

    @country.setter
    def country(self, val):
        if not isinstance(val, str):
            raise Exception("Value must be a string.")
        self._country = val

    @property
    def coauthors(self):
        """Set of coauthors of the scientist on all publications until the
        given year.
        """
        return self._coauthors

    @coauthors.setter
    def coauthors(self, val):
        if not isinstance(val, set) or len(val) == 0:
            raise Exception("Value must be a non-empty set.")
        self._coauthors = val

    @property
    def fields(self):
        """The fields of the scientist until the given year, estimated from
        the sources (journals, books, etc.) she published in.
        """
        return self._fields

    @fields.setter
    def fields(self, val):
        if not isinstance(val, list) or len(val) == 0:
            raise Exception("Value must be a non-empty list.")
        self._fields = val

    @property
    def first_year(self):
        """The scientist's year of first publication, as integer."""
        return self._first_year

    @first_year.setter
    def first_year(self, val):
        if not isinstance(val, int):
            raise Exception("Value must be an integer.")
        self._first_year = val

    @property
    def main_field(self):
        """The scientist's main field of research, as tuple in
        the form (ASJC code, general category).
        """
        return self._main_field

    @main_field.setter
    def main_field(self, val):
        if not isinstance(val, tuple) or len(val) != 2:
            raise Exception("Value must be a two-element tuple.")
        self._main_field = val

    @property
    def publications(self):
        """The publications of the scientist published until
        the given year.
        """
        return self._publications

    @publications.setter
    def publications(self, val):
        if not isinstance(val, list) or len(val) == 0:
            raise Exception("Value must be a non-empty list.")
        self._publications = val

    @property
    def search_group(self):
        """The set of authors that might be matches to the scientist.  The
        set contains the intersection of all authors publishing in the given
        year as well as authors publishing around the year of first
        publication.  Some authors with too many publications in the given
        year and authors having published too early are removed.

        Notes
        -----
        Property is initiated via .define_search_group().
        """
        try:
            return self._search_group
        except AttributeError:
            return None

    @property
    def search_sources(self):
        """The set of sources (journals, books) comparable to the sources
        the scientist published in until the given year.
        A sources is comparable if is belongs to the scientist's main field
        but not to fields alien to the scientist, and if the types of the
        sources are the same as the types of the sources in the scientist's
        main field where she published in.

        Notes
        -----
        Property is initiated via .define_search_sources().
        """
        try:
            return self._search_sources
        except AttributeError:
            return None

    @search_sources.setter
    def search_sources(self, val):
        if not isinstance(val, list) or len(val) == 0:
            raise Exception("Value must be a non-empty list.")
        self._search_sources = val

    @property
    def sources(self):
        """The Scopus IDs of sources (journals, books) in which the
        scientist published until the given year.
        """
        return self._sources

    @sources.setter
    def sources(self, val):
        if not isinstance(val, set) or len(val) == 0:
            raise Exception("Value must be a non-empty set.")
        self._sources = val

    def __init__(self, scientist, year, year_margin=1, pub_margin=0.1,
                 coauth_margin=0.1, refresh=False):
        """Class to represent a scientist for which we want to find a control
        group.

        Parameters
        ----------
        scientist : str or int
            Scopus Author ID of the scientist you want to find control
            groups for.

        year : str or numeric
            Year of the event.  Control groups will be matched on trends and
            characteristics of the scientist up to this year.

        year_margin : numeric (optional, default=1)
            Number of years by which the search for authors publishing around
            the year of the focal scientist's year of first publication should
            be extend in both directions.

        pub_margin : numeric (optional, default=0.1)
            The left and right margin for the number of publications to match
            possible matches and the scientist on.  If the value is a float,
            it is interpreted as percentage of the scientists number of
            publications and the resulting value is rounded up.  If the value
            is an integer it is interpreted as fixed number of publications.

        coauth_margin : numeric (optional, default=0.1)
            The left and right margin for the number of coauthors to match
            possible matches and the scientist on.  If the value is a float,
            it is interpreted as percentage of the scientists number of
            coauthors and the resulting value is rounded up.  If the value
            is an integer it is interpreted as fixed number of coauthors.

        refresh : boolean (optional, default=False)
            Whether to refresh all cached files or not.
        """
        # Check for existence of fields-sources list
        try:
            self.field_source = pd.read_csv(FIELDS_SOURCES_LIST)
            df = self.field_source
        except FileNotFoundError:
            text = "Fields-Sources list not found, but required for sosia "\
                   "to match authors' publications to fields.  Please run "\
                   "sosia.create_fields_sources_list() and initiate "\
                   "the class again."
            raise Exception(text)

        # Internal checks
        if not isinstance(year, int):
            raise Exception("Argument year must be an integer.")
        if not isinstance(year_margin, (int, float)):
            raise Exception("Argument year_margin must be float or integer.")
        if not isinstance(pub_margin, (int, float)):
            raise Exception("Argument pub_margin must be float or integer.")
        if not isinstance(coauth_margin, (int, float)):
            raise Exception("Argument coauth_margin must be float or integer.")

        # Variables
        self.id = str(scientist)
        self.year = int(year)
        self.year_margin = year_margin
        self.pub_margin = pub_margin
        self.coauth_margin = coauth_margin
        self.refresh = refresh

        # Own information
        res = _query_docs('AU-ID({})'.format(self.id), refresh=self.refresh)
        self._publications = [p for p in res if int(p.coverDate[:4]) < self.year]
        if len(self._publications) == 0:
            text = "No publications for author {} until year {}".format(
                self.id, self.year)
            raise Exception(text)
        self._sources = set([int(p.source_id) for p in self._publications])
        self._fields = df[df['source_id'].isin(self._sources)]['asjc'].tolist()
        main = Counter(self._fields).most_common(1)[0][0]
        code = main // 10 ** (int(log(main, 10)) - 2 + 1)
        self._main_field = (main, ASJC_2D[code])
        self._first_year = int(min([p.coverDate[:4] for p in self._publications]))
        self._coauthors = set([a for p in self._publications
                              for a in p.authid.split(';')])
        self._coauthors.remove(self.id)
        self._country = _find_country(self.id, self._publications, self.year)

    def define_search_group(self, stacked=False, verbose=False, refresh=False):
        """Define search_group.

        Parameters
        ----------
        stacked : bool (optional, default=False)
            Whether to combine searches in few queries or not.  Cached
            files with most likely not be resuable.  Set to True if you
            query in distinct fields or you want to minimize API key usage.

        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.

        refresh : bool (optional, default=False)
            Whether to refresh cached search files.
        """
        # Checks
        if not self.search_sources:
            text = "No search sources defined.  Please run "\
                   ".define_search_sources() first."
            raise Exception(text)
        try:
            _npapers = _get_value_range(len(self.publications), self.pub_margin)
            max_pubs = max(_npapers)
        except TypeError:
            raise ValueError('Value pub_margin must be float or integer.')
        # Variables
        today = set()
        then = set()
        negative = set()
        auth_count = []
        _min_year = self.first_year-self.year_margin
        _years = list(range(self.first_year-self.year_margin,
                            self.first_year+self.year_margin+1))
        # Query journals
        if stacked:
            params = {"group": [str(x) for x in sorted(self.search_sources)],
                      "joiner": ") OR SOURCE-ID(", "refresh": refresh,
                      "func": partial(_query_docs)}
            if verbose:
                n = len(self.search_sources)
                params.update({"i": 0, "total": n})
                print("Searching authors in {} sources in {}...".format(
                        len(self.search_sources), self.year))
            # Today
            query = Template("SOURCE-ID($fill) AND PUBYEAR IS {}".format(self.year))
            params.update({'query': query, "res": []})
            pubs, _ = _stacked_query(**params)
            today.update([au for sl in _get_authors(pubs) for au in sl])
            # Then
            if len(_years) == 1:
                query = Template("SOURCE-ID($fill) AND PUBYEAR IS {}".format(
                    _years[0]))
                if verbose:
                    print("Searching authors in {} sources in {}...".format(
                        len(self.search_sources), _years[0]))
            else:
                _min = min(_years)-1
                _max = max(_years)+1
                query = Template("SOURCE-ID($fill) AND PUBYEAR AFT {} AND "
                                 "PUBYEAR BEF {}".format(_min, _max))
                if verbose:
                    print("Searching authors in {} sources in {}-{}...".format(
                        len(self.search_sources), _min+1, _max-1))
            params.update({'query': query, "res": []})
            pubs, _ = _stacked_query(**params)
            then.update([au for sl in _get_authors(pubs) for au in sl])
            # Negative
            if verbose:
                print("Searching authors in {} sources in {}...".format(
                        len(self.search_sources), _min_year-1))
            query = Template("SOURCE-ID($fill) AND PUBYEAR IS {}".format(_min_year-1))
            params.update({'query': query, "res": []})
            pubs, _ = _stacked_query(**params)
            negative.update([au for sl in _get_authors(pubs) for au in sl])
        else:
            if verbose:
                n = len(self.search_sources)
                print("Searching authors for search_group in {} "
                      "sources...".format(len(self.search_sources)))
                _print_progress(0, n)
            for i, s in enumerate(self.search_sources):
                try:  # Try complete publication list first
                    res = _query_docs('SOURCE-ID({})'.format(s), refresh)
                    # Today
                    pubs = [p for p in res if int(p.coverDate[:4]) == self.year]
                    today.update([au for sl in _get_authors(pubs) for au in sl])
                    # Then
                    pubs = [p for p in res if int(p.coverDate[:4]) in _years]
                    then.update([au for sl in _get_authors(pubs) for au in sl])
                    # Publications before
                    res1 = [p for p in res if int(p.coverDate[:4]) < _min_year]
                    negative.update([au for sl in _get_authors(res1) for au in sl])
                    # Author count (for excess publication count)
                    res2 = [p for p in res if int(p.coverDate[:4]) < self.year+1]
                    auth_count.extend([au for sl in _get_authors(res2) for au in sl])
                except:  # Fall back to year-wise queries
                    q = 'SOURCE-ID({}) AND PUBYEAR IS {}'.format(s, self.year)
                    res = _query_docs(q, refresh)
                    today.update([au for sl in _get_authors(res) for au in sl])
                    for y in _years:
                        q = 'SOURCE-ID({}) AND PUBYEAR IS {}'.format(s, y)
                        res = _query_docs(q, refresh)
                        new = [x.authid.split(';') for x in pubs
                               if isinstance(x.authid, str)]
                        then.update([au for sl in new for au in sl])
                if verbose:
                    _print_progress(i+1, n)
        # Finalize
        group = today.intersection(then)
        negative.update({a for a, npubs in Counter(auth_count).items()
                         if npubs > max_pubs})
        self._search_group = sorted(list(group - negative))
        if verbose:
            print("Found {:,} authors for search_group".format(
                len(self._search_group)))

    def define_search_sources(self, verbose=False):
        """Define .search_sources.

        Parameters
        ----------
        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.
        """
        df = self.field_source
        # Select types of sources of scientist's publications in main field
        mask = (df['source_id'].isin(self.sources)) &\
               (df['asjc'] == self.main_field[0])
        main_types = set(df[mask]['type'])
        # Select sources in scientist's main field
        mask = (df['asjc'] == self.main_field[0]) & (df['type'].isin(main_types))
        sources = df[mask]['source_id'].tolist()
        sel = df[df['source_id'].isin(sources)].copy()
        sel['asjc'] = sel['asjc'].astype(str) + " "
        grouped = sel.groupby('source_id').sum()['asjc'].to_frame()
        # Deselect sources with alien fields
        grouped['drop'] = grouped['asjc'].apply(
            lambda s: any(x for x in s.split() if int(x) not in self.fields))
        # Add own sources
        sources = set(grouped[~grouped['drop']].index.tolist())
        sources.update(set(self.sources))
        self._search_sources = sorted(list(sources))
        if verbose:
            types = "; ".join(list(main_types))
            print("Found {} sources for main field {} and source "
                  "type(s) {}".format(len(self._search_sources),
                                      self.main_field[0], types))

    def find_matches(self, stacked=False, verbose=False, refresh=False):
        """Find matches within search_group based on three criteria:
        1. Started publishing in about the same year
        2. Has about the same number of publications in the year of treatment
        3. Has about the same number of coauthors in the year of treatment
        4. Affiliation was in the same country in the year of treatment

        Parameters
        ----------
        stacked : bool (optional, default=False)
            Whether to combine searches in few queries or not.  Cached
            files with most likely not be resuable.  Set to True if you
            query in distinct fields or you want to minimize API key usage.

        verbose : bool (optional, default=False)
            Whether to report on the progress of the process.

        refresh : bool (optional, default=False)
            Whether to refresh cached search files.
        """
        # Variables
        _years = range(self.first_year-self.year_margin,
                       self.first_year-self.year_margin+1)
        _npapers = _get_value_range(len(self.publications), self.pub_margin)
        _ncoauth = _get_value_range(len(self.coauthors), self.coauth_margin)

        # Define search group
        group = sorted(self.search_group)
        n = len(group)
        if verbose:
            print("Searching through characteristics of {:,} authors".format(n))

        # First stage of filtering: minimum publications and main field
        params = {"group": group, "res": [], "refresh": refresh,
                  "joiner": ") OR AU-ID(", "func": partial(_query_author),
                  "query": Template("AU-ID($fill)")}
        if verbose:
            print("Pre-filtering...")
            _print_progress(0, n)
            params.update({'i': 0, 'total': n})
        res, _ = _stacked_query(**params)
        df = pd.DataFrame(res)
        df = df[df['areas'].str.startswith(self.main_field[1])]
        df['documents'] = pd.to_numeric(df['documents'], errors='coerce').fillna(0)
        df = df[df['documents'].astype(int) >= min(_npapers)]
        n = df.shape[0]
        if verbose:
            print("Left with {} authors".format(n))

        # Second round of filtering
        df['id'] = df['eid'].str.split('-').str[-1]
        group = sorted(df['id'].tolist())
        if verbose:
            print("Filtering based on provided conditions...")
            i = 0
            _print_progress(0, n)
        keep = defaultdict(list)
        if stacked:  # Combine searches
            query = Template("AU-ID($fill) AND PUBYEAR BEF {}".format(self.year+1))
            params = {"group": group, "res": [], "query": query,
                      "joiner": ") OR AU-ID(", "func": partial(_query_docs),
                      "refresh": refresh}
            if verbose:
                params.update({"i": 0, "total": n})
            res, _ = _stacked_query(**params)
            container = _build_dict(res, group)
            # Iterate through container in order to filter results
            for auth, dat in container.items():
                dat['n_coauth'] = len(dat['coauth'])
                dat['n_pubs'] = len(dat['pubs'])
                if (dat['first_year'] in _years and dat['n_pubs'] in
                        _npapers and dat['n_coauth'] in _ncoauth):
                    keep['ID'].append(auth)
                    for key, val in dat.items():
                        keep[key].append(val)
        else:  # Query each author individually
            for i, au in enumerate(group):
                if verbose:
                    _print_progress(i+1, n)
                res = _query_docs('AU-ID({})'.format(au), refresh)
                res = [p for p in res if int(p.coverDate[:4]) < self.year+1]
                # Filter
                if len(res) not in _npapers:
                    continue
                min_year = int(min([p.coverDate[:4] for p in res]))
                if min_year not in _years:
                    continue
                coauth = set([a for p in res for a in p.authid.split(';')])
                coauth.remove(au)
                if len(coauth) not in _ncoauth:
                    continue
                # Collect information
                keep['ID'].append(au)
                keep['first_year'].append(min_year)
                keep['n_pubs'].append(len(res))
                keep['n_coauth'].append(len(coauth))
        if verbose:
            print("Found {:,} author(s) matching all criteria\nAdding "
                  "other information...".format(len(keep['ID'])))
        profiles = [sco.AuthorRetrieval(auth, refresh) for auth in keep['ID']]
        # Add name
        names = [", ".join([p.surname, p.given_name]) for p in profiles]
        # Add country
        countries = [_find_country(
                        au, _query_docs('AU-ID({})'.format(au), refresh),
                        self.year)
                     for au in keep['ID']]
        # Add abstract and reference cosine similarity
        tokens = [_get_refs(au, self.year, refresh, verbose) for au in keep['ID']]
        tokens.append(_get_refs(self.id, self.year, refresh, verbose))
        ref_m = TfidfVectorizer().fit_transform([t['refs'] for t in tokens])
        ref_cos = (ref_m * ref_m.T).toarray().round(4)[-1]
        vectorizer = TfidfVectorizer(
            min_df=0.05, max_df=0.8, max_features=200000, ngram_range=(1, 3),
            stop_words=STOPWORDS, tokenizer=_tokenize_and_stem)
        tfidf = vectorizer.fit_transform([t['abstracts'] for t in tokens])
        abs_cos = (tfidf * tfidf.T).toarray().round(4)[-1]

        # Merge information into namedtuple
        t = list(zip(keep['ID'], names, keep['first_year'], keep['n_coauth'],
                     keep['n_pubs'], countries, ref_cos, abs_cos))
        fields = "ID name first_year num_coauthors num_publications country "\
                 "reference_sim abstract_sim"
        match = namedtuple("Match", fields)
        return [match(*tup) for tup in t]


def _build_dict(results, chunk):
    """Create dictionary assigning publication information to authors we
    are looking for.
    """
    d = defaultdict(lambda: {'first_year': inf, 'pubs': set(), 'coauth': set()})
    for pub in results:
        authors = set(pub.authid.split(';'))
        for focal in authors.intersection(chunk):
            d[focal]['coauth'].update(authors)
            d[focal]['coauth'].remove(focal)
            d[focal]['pubs'].add(pub.eid)
            first_year = min(d[focal]['first_year'], int(pub.coverDate[:4]))
            d[focal]['first_year'] = first_year
    return d


def _run(op, *args):
    """Auxiliary function to call a function passed by partial()."""
    return op(*args)


def _stacked_query(group, res, query, joiner, func, refresh, i=None, total=None):
    """Auxiliary function to recursively perform queries until they work.

    Results of each successful query are appended to ´res´.
    """
    try:
        q = query.substitute(fill=joiner.join(group))
        res.extend(_run(func, q, refresh))
        if total:  # Equivalent of verbose
            i += len(group)
            _print_progress(i, total)
    except Exception as e:  # Catches two exceptions (long URL + many results)
        mid = len(group) // 2
        params = {"group": group[:mid], "res": res, "query": query, "i": i,
                  "joiner": joiner, "func": func, "total": total,
                  "refresh": refresh}
        res, i = _stacked_query(**params)
        params.update({"group": group[mid:], "i": i})
        res, i = _stacked_query(**params)
    return res, i


def _get_authors(pubs):
    """Auxiliary function to get author IDs from string concatenated by ;,
    which are embedded in a list of namedtuples.
    """
    return [x.authid.split(';') for x in pubs if isinstance(x.authid, str)]


def _get_refs(auth, year, refresh, verbose):
    """Auxiliary function to return abstract and references of articles
    published up until the given year, both as continuous string.
    """
    res = _query_docs("AU-ID({})".format(auth), refresh)
    eids = [p.eid for p in res if int(p.coverDate[:4]) <= year]
    abstracts = ""
    refs = ""
    missing = {'abs': 0, 'refs': 0}
    for eid in eids:
        ab = sco.AbstractRetrieval(eid, view='FULL', refresh=refresh)
        try:
            abstracts += ab.abstract.rsplit("©", 1)[0]
        except AttributeError:  # No abstract present
            missing['abs'] += 1
            continue
        try:
            refs += " ".join([ref.id for ref in ab.references])
        except TypeError:  # No references present (consider refreshing)
            missing['refs'] += 1
            continue
    if verbose:
        print("For researcher {}, {} abstract(s) and {} reference list(s) out "
              "of {} documents are missing".format(auth, missing['abs'],
                                                   missing['refs'], len(eids)))
    return {"abstracts": abstracts, "refs": refs}


def _get_value_range(base, val):
    """Auxiliary function to create a range of margins around a base value."""
    if isinstance(val, float):
        margin = ceil(val*base)
        r = range(base-margin, base+margin+1)
    elif isinstance(val, int):
        r = range(base-margin, base+margin+1)
    return r


def _find_country(auth_id, pubs, year):
    """Auxiliary function to find the country of the most recent affiliation
    of a scientist.
    """
    # Available papers of most recent year with publications
    papers = []
    i = 0
    while len(papers) == 0 & i <= len(pubs):
        papers = [p for p in pubs if int(p.coverDate[:4]) == year-i]
        i += 1
    if len(papers) == 0:
        return None
    # List of affiliations on these papers belonging to the actual author
    affs = []
    for p in papers:
        authors = p.authid.split(';')
        idx = authors.index(str(auth_id))
        aff = p.afid.split(';')[idx].split('-')
        affs.extend(aff)
    affs = [a for a in affs if a != '']
    # Find most often listed country of affiliations
    countries = [sco.ContentAffiliationRetrieval(afid).country
                 for afid in affs]
    return Counter(countries).most_common(1)[0][0]


def _print_progress(iteration, total, prefix='Progress:', suffix='Complete',
                    decimals=2, length=50, fill='█'):
    """Print terminal progress bar."""
    percent = round(100 * (iteration / float(total)), decimals)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    if iteration == total:
        print()


def _tokenize_and_stem(text):
    """Auxiliary funtion to return stemmed tokens of document"""
    return [_stemmer.stem(t) for t in word_tokenize(text.lower())]


def _query_author(q, refresh=False):
    """Auxiliary function to perform a search query for authors."""
    try:
        return sco.AuthorSearch(q, refresh=refresh).authors
    except KeyError:
        return sco.AuthorSearch(q, refresh=True).authors


def _query_docs(q, refresh=False):
    """Auxiliary function to perform a search query for documents."""
    try:
        return sco.ScopusSearch(q, refresh=refresh).results
    except KeyError:
        return sco.ScopusSearch(q, refresh=True).results
