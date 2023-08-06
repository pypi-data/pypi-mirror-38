import pandas as pd
import numpy as np
from .general import pyrolite_datafolder
from .pd import to_frame, to_numeric
from .text import titlecase, string_variations


__DATA__ = pyrolite_datafolder(subfolder='timescale') / \
            'geotimescale_spans.csv'


def listify(df, axis=1):
    """
    Consdense text information across columns into a single list.

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe (or slice of dataframe) to condense along axis.
    axis: {1, 0}
        Axis to condense along.
    """
    return df.copy().apply(list, axis=axis)


def age_name(agenamelist,
             prefixes=['Lower', 'Middle', 'Upper'],
             suffixes=['Stage', 'Series']
             ):
    """
    Condenses an agename list to a specific agename, given a subset of
    ambiguous_names.

    Parameters
    ----------
    agenamelist: list
        List of name components (i.e. [Eon, Era, Period, Epoch])
    prefixes: list
        Name components which occur prior to the higher order classification
        (e.g. Upper Triassic).
    suffixes: list
        Name components which occur after the higher order classification
        (e.g. Cambrian Series 2).
    """
    ambiguous_names= prefixes + suffixes

    nameguess = agenamelist[-1]
    nn_nameguess = ''.join([i for i in nameguess if not i.isdigit()]).strip()
    hit = [s for s in ambiguous_names
           if any(i == nn_nameguess for i in string_variations(s))][0:1]

    if hit:
        indexstart = len(agenamelist)-1
        outname = [agenamelist[indexstart]]
        out_index_previous = 0
        ambiguous_name = True
        while ambiguous_name:
            hitphrase = hit[0]
            indexstart -=1
            nextup = agenamelist[indexstart]
            if hitphrase in prefixes:
                # insert the higher order component after the previous one
                outname.insert(out_index_previous+1, nextup)
                out_index_previous += 1
            else:
                # insert the higher order component before the previous one
                outname.insert(out_index_previous-1, nextup)
                out_index_previous -= 1

            _nn_nextupguess = ''.join([i for i in nextup if not i.isdigit()]
                                      ).strip()
            hit = [s for s in ambiguous_names
                   if any(i == _nn_nextupguess for i in string_variations(s))
                   ][0:1]
            if not hit:
                ambiguous_name = False
        return " ".join(outname)
    else:
        return nameguess


def timescale_reference_frame(filename=__DATA__,
                              info_cols=['Start', 'End', 'Aliases']
                              ):
    """
    Rearrange the text-based timescale dataframe. Utility function for
    timescale class.

    Parameters
    ----------
    filename: {str, pathlib.Path}
        File from which to generate the timescale information.
    info_cols: list
        List of columns beyond hierarchial group labels (e.g. Eon, Era..).

    Returns
    -------
    pd.DataFrame
        Dataframe containing timescale information.
    """

    df =  pd.read_csv(filename)
    df.loc[:, ['Start', 'End']] = to_numeric(df.loc[:, ['Start', 'End']])
    _df = df.copy()
    grps = [i for i in _df.columns if not i in info_cols]
    condensed = _df.loc[:,
                        [i for i in _df.columns if not i in info_cols]
                         ].applymap(lambda x: x if not pd.isnull(x) else '')

    level = condensed.apply(lambda x: grps[[ix for ix, v in enumerate(x)
                                             if v][-1]],
                                  axis=1)
    _df['Level'] = level

    condensed = listify(condensed).apply(lambda x: [i for i in x if i])
    _df['Name'] = condensed.apply(age_name)
    _df['Ident'] = condensed.apply('-'.join)
    _df['MeanAge'] = _df.apply(lambda x:(x.Start + x.End)/2, axis=1)
    _df['Unc'] = _df.apply(lambda x:(x.Start - x.End)/2, axis=1)

    # Aliases
    _df['Aliases'] = _df['Aliases'].apply(lambda x:
                                        [] if pd.isnull(x)
                                        else x.split(';'))
    _df['Aliases'] = _df.apply(lambda x: string_variations([x.Name, x.Ident] + \
                                                         x.Aliases),
                                         axis=1)

    col_order = ['Ident', 'Name', 'Level',
                 'Start', 'End', 'MeanAge', 'Unc'] + grps + ['Aliases']



    return _df.loc[:, col_order]


class Timescale(object):
    """
    Geological Timescale class to provide time-focused utility functions.
    """

    def __init__(self,
                filename=None):
        if filename is None:
            self.data = timescale_reference_frame()
        else:
            self.data = timescale_reference_frame(filename)
        self.levels = [i for i in self.data.Level.unique() if not pd.isnull(i)]
        self.levels = [i for i in self.data.columns if i in self.levels]
        self.build()

    def build(self):
        for ix, g in enumerate(self.levels):
            others = self.levels[ix+1:]
            fltr = (self.data.loc[:, others].isnull().all(axis=1) &
                    ~self.data.loc[:, g].isnull())
            setattr(self, g+'s',  self.data.loc[fltr, :])

    def text2age(self, entry):
        """
        Converts a text-based age to the corresponding age range (in Ma).

        Parameters
        ------------
        entry: str
            String name for geological age range.


        Returns
        ------------
        tuple
            Tuple representation of min_age, max_age for the entry.
        """

        indexer = self.data.Aliases.apply(lambda x: entry in x)

        return tuple(self.data.loc[indexer, ['Start', 'End']].values[0])


    def named_age(self, age, level='Period'):
        """
        Converts a numeric age (in Ma) to named age at a specific level.

        Parameters
        ------------
        age: float
            Numeric age in Ma.
        level: {'Eon', 'Era', 'Period', 'Superepoch',
                'Epoch', 'Age', 'Specific'}
            Level of specificity.

        Returns
        ------------
        str
            String representation for the entry.
        """

        level = titlecase(level)
        wthn_rng = lambda x: (age <= x.Start) & (age >= x.End)
        relevant = self.data.loc[self.data.apply(wthn_rng, axis=1).values, :]
        if level == 'Specific': # take the rightmost grouping
            relevant = relevant[self.levels]
            idx_rel_row = (~pd.isnull(relevant)).count(axis=1).idxmax()
            rel_row = relevant.iloc[idx_rel_row, :]
            spec = rel_row[~pd.isnull(rel_row)].values[-1]
            return spec
        else:
            relevant = relevant[level]
            return relevant.unique()[~pd.isnull(relevant.unique())][0]
