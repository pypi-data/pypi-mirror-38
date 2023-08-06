import pandas as pd
import numpy as np
from functools import partial
import requests
import re
import logging

from .pd import *
from .text import titlecase, parse_entry, split_records
from .general import temp_path, urlify, pyrolite_datafolder, pathify, iscollection
from ..geochem import tochem, check_multiple_cation_inclusion, aggregate_cation
from ..norm import scale_multiplier

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

# -----------------------------
# GEOROC INFO
# -----------------------------
__value_rx__ = r"(\s)*?(?P<value>[\.,\s\w]+\b)((\s)*?\[)?(?P<key>\w*)(\])?(\s)*?"
__cit_rx__ = r"(\s)*?(\[)?(?P<key>\w*)(\])?(\s)*?(?P<value>[\.\w]+)(\s)*?"
__full_cit_rx__ = r"(\s)*?\[(?P<key>\w*)\](\s)*(?P<value>.+)$"
__doi_rx__ = r"(.)*(doi(\s)*?:*)(\s)*(?P<value>\S*)"

__CONTENTS__ = {
    "CFB": dict(
        url_suffix=r"Continental_Flood_Basalts_comp",
        list_file="GEOROC_CFB_Dataset_List.csv",
    ),
    "ConvergentMargins": dict(
        url_suffix=r"Convergent_Margins_comp",
        list_file="GEOROC_Convergent_Dataset_List.csv",
    ),
    "OceanicPlateaus": dict(
        url_suffix=r"Oceanic_Plateaus_comp",
        list_file="GEOROC_OceanicPlateau_Dataset_List.csv",
    ),
    "OIB": dict(
        url_suffix=r"Ocean_Island_Groups_comp", list_file="GEOROC_OIB_Dataset_List.csv"
    ),
    "OBFB": dict(
        url_suffix=r"Ocean_Basin_Flood_Basalts_comp",
        list_file="GEOROC_OBFB_Dataset_List.csv",
    ),
}


__COMP_LISTS__ = pyrolite_datafolder(subfolder="georoc")


# -----------------------------


def subsitute_commas(entry):
    if iscollection(entry):
        return [x.replace(",", ";") for x in entry]
    else:
        return entry.replace(",", ";")


def parse_values(entry, sub=subsitute_commas, **kwargs):
    """
    Wrapper for parse_entry for GEOROC formatted values.

    Parameters
    -------------
    entry: pd.Series | str
        String series formated as sequences of 'VALUE [NUMERIC_CITATION]'
        separated by '/'. Else a string entry itself.
    sub: function
        Secondary subsitution function, here used for subsitution
        (e.g. of commas).
    """
    f = partial(parse_entry, regex=__value_rx__, delimiter="/", **kwargs)
    if isinstance(entry, pd.Series):
        return entry.apply(f).apply(sub)
    else:
        return sub(f(entry))


def parse_citations(entry, **kwargs):
    """
    Wrapper for parse_entry for GEOROC formatted citations.

    Parameters
    -------------
    ser: pd.Series
        String series formated as sequences of '[NUMERIC_CITATION] Citation'.
    """
    f = partial(
        parse_entry, regex=__full_cit_rx__, values_only=False, delimiter=None, **kwargs
    )
    if isinstance(entry, pd.Series):
        return entry.apply(f)
    else:
        return f(entry)


def parse_DOI(entry, link=True, **kwargs):
    """
    Wrapper for parse_entry for GEOROC formatted dois.

    Parameters
    -------------
    ser: pd.Series
        String series formated as sequences of 'Citation doi: DOI'.
    """
    f = partial(
        parse_entry,
        regex=__doi_rx__,
        values_only=True,
        delimiter=None,
        first_only=True,
        replace_nan="",
        **kwargs
    )
    if isinstance(entry, pd.Series):
        return entry.apply(lambda x: r"{}{}".format(["", "dx.doi.org/"][link], f(x)))
    else:
        return r"{}{}".format(["", "dx.doi.org/"][link], f(entry))


def bulk_GEOROC_download(
    output_folder=Path("~/Downloads/GEOROC"),
    reservoirs=None,
    redownload: bool = False,
    write_hdf=False,
):
    """
    Download utility for GEOROC data. Facilitates incremental and resumed
    downloadsself. Output data will be organised into folders by reservoir, and
    stored as both i) individual CSVs and ii) a picked pd.DataFrame.

    Notes
    -----
        Chemical abundance data are output as Wt% by default.


    Parameters
    ----------
    output_folder: {pathlib.Path('~/Downloads/GEOROC'), :obj:`str`}
        Path to folder to store output data.
    reservoirs: {None, :obj:`list` of :obj:`str`}
        Dictionaries containing named reservoirs to download, defualting to a
        subset  form name: dict(url_suffix=r'X', list_file="Y.csv")
        Each dictionary needs to specifiy the GEOROC url_suffix and contain
        a list of valid sub-reservoirs (e.g. locations).
    redownload: {True, False}
        Whether to redownload prevoiusly downloaded compilations.
    write_hdf: {False, True}
        Whether to also create HDF5 files.
    """
    output_folder = output_folder or temp_path()
    output_folder = pathify(output_folder)
    output_folder = output_folder.expanduser()

    reservoirs = reservoirs or __CONTENTS__.keys()

    for res in reservoirs:
        resdir = output_folder / res
        out_aggfile = output_folder / ("GEOROC_" + res)
        v = __CONTENTS__[res]

        if not resdir.exists():
            resdir.mkdir(parents=True)

        # Compilation List of Targets
        list_file = __COMP_LISTS__ / v["list_file"]
        filenames = [i.split(",")[0].strip() for i in open(str(list_file)).readlines()]

        # URL target
        host = r"http://georoc.mpch-mainz.gwdg.de/georoc/Csv_Downloads"
        base_url = host + "/" + v["url_suffix"]

        # Files yet to download, continuing from last 'save'
        dwnld_fns = filenames
        if not redownload:
            logger.info("Fetching only undownloaded files.")
            # Just get the ones we don't have,
            dwnld_stems = [(resdir / urlify(f)).stem for f in dwnld_fns]
            current_files = [f.stem for f in resdir.iterdir() if f.is_file()]
            dwnld_fns = [
                f for f, s in zip(dwnld_fns, dwnld_stems) if not s in current_files
            ]

        dataseturls = [
            (urlify(d), base_url + r"/" + urlify(d))
            for d in dwnld_fns
            if d
            if d.strip()
        ]

        for name, url in dataseturls:
            outfile = (resdir / name).with_suffix("")
            msg = "Downloading {} {} dataset to {}.".format(res, name, outfile)
            logger.info(msg)
            try:
                df = download_GEOROC_compilation(url)
                df.to_csv(outfile.with_suffix(".csv"))
                # df.to_parquet(outfile.with_suffix('.pk'))

                if write_hdf:
                    with pd.HDFStore(out_aggfile.with_suffix(".h5"), mode="w") as store:
                        min_itemsize = {
                            c: 100 for c in df.columns[df.dtypes == "object"]
                        }
                        min_itemsize.update({"Citations": 1200})
                        store.append(
                            name, df, format="table", min_itemsize=min_itemsize
                        )
            except requests.exceptions.HTTPError as e:
                pass

        # Compile CSVs
        aggdf = df_from_csvs(resdir.glob("*.csv"), ignore_index=True)
        msg = "Aggregated {} datasets ({} records).".format(res, aggdf.index.size)
        logger.info(msg)

        # Save the compilation
        sparse_pickle_df(aggdf, out_aggfile)

    logger.info("Download and aggregation for {} finished.".format(res))


def download_GEOROC_compilation(url: str):
    """
    Downloads a specific GEOROC compilation and returns a cleaned and formatted
    pd.DataFrame.

    Parameters
    ----------
    url: str
        URL of specific compilation to download as a csv.

    Returns
    -------
    pd.DataFrame
        Dataframe representation of the GEOROC data.
    """
    with requests.Session() as s:
        response = s.get(url)
        if response.status_code == requests.codes.ok:
            logger.debug("Response recieved from {}.".format(url))
            return format_GEOROC_response(response.content.decode("latin-1"))
        else:
            msg = "Failed download - bad status code at {}".format(url)
            logger.warning(msg)
            response.raise_for_status()


def format_GEOROC_response(content: str, start_chem="SiO2", end_chem="Nd143Nd144"):
    """
    Formats decoded content from GEOROC as a pd.DataFrame

    Parameters
    ---------
    content
        Decoded string from GEOROC response.

    Returns
    -------
    pd.DataFrame
    """
    # GEOROC Specific Data Working
    data, ref = re.split("\s?References:\s+", content)
    datalines = [re.split(r'"\s?,\s?"', line) for line in re.split(r",\r", data)]
    cols = [i.replace('"', "").replace(",", "") for i in datalines[0]]
    cols = [titlecase(h, abbrv=["ID"]) for h in cols]
    start = 1
    finish = len(datalines)
    if datalines[-1][0].strip().startswith("Abbreviations"):
        finish -= 1
    df = pd.DataFrame(datalines[start:finish], columns=cols)
    cols = list(df.columns)
    df = df.applymap(lambda x: str(x).replace('"', ""))

    # Location names are extended with newlines
    df.Location = df.Location.apply(lambda x: str(x).replace("\r\n", " / "))

    df.Citations = df.Citations.apply(lambda x: re.findall(r"[\d]+", x))
    # df = df.drop(index=df.index[~df.Citations.apply(lambda x: len(x))])
    # Drop Empty Rows
    df = df.dropna(how="all", axis=0)
    df = df.set_index("UniqueID", drop=True)
    df = df.apply(parse_values, axis=1)

    # Translate headers and data units
    cols = tochem([c.replace("(wt%)", "").replace("(ppm)", "") for c in df.columns])
    start = cols.index("SiO2")
    end = cols.index("Nd143Nd144")
    where_ppm = [
        (("ppm" in t) and (ix >= start and ix <= end))
        for ix, t in enumerate(df.columns)
    ]

    # Rename columns
    df.columns = cols
    headercols = list(df.columns[:start])
    chemcols = list(df.columns[start:end])
    trailingcols = list(df.columns[end:])  # trailing are generally isotope ratios
    # Numeric data

    numheaders = [
        "ElevationMin",
        "ElevationMax",
        "LatitudeMin",
        "LatitudeMax",
        "LongitudeMin",
        "LongitudeMax",
        "Min.Age(yrs.)",
        "Max.Age(yrs.)",
    ]

    numeric_cols = numheaders + chemcols + trailingcols
    # can include duplicates at this stage.
    numeric_cols = [i for i in df.columns if i in numeric_cols]
    numeric_ixs = [ix for ix, i in enumerate(df.columns) if i in numeric_cols]
    df[numeric_cols] = df.iloc[:, numeric_ixs].apply(
        pd.to_numeric, errors="coerce", axis=1
    )
    # remove <0.
    chem_ixs = [ix for ix, i in enumerate(df.columns) if i in chemcols]
    df.iloc[:, chem_ixs] = df.iloc[:, chem_ixs].mask(
        df.iloc[:, chem_ixs] <= 0.0, other=np.nan
    )

    # units conversion -- convert to Wt%
    df.iloc[:, where_ppm] *= scale_multiplier("ppm", "Wt%")

    # deal with duplicate columns
    collist = list(df.columns)
    dup_chemcols = df.columns[
        df.columns.duplicated() & [i in chemcols for i in collist]
    ]
    for chem in dup_chemcols:
        # replace the first (non-duplicated) column with the sum
        ix = collist.index(chem)
        df.iloc[:, ix] = df.loc[:, chem].apply(np.nansum, axis=1)

    df = df.iloc[:, ~df.columns.duplicated()]

    # Process the reference data.
    reflines = split_records(ref)
    reflines = [line.replace('"', "") for line in reflines]
    reflines = [line.replace("\r\n", "") for line in reflines]
    reflines = [parse_citations(i) for i in reflines if i]
    refdf = pd.DataFrame.from_records(reflines).set_index("key", drop=True)
    # Replace the reference indexes with references.
    df.Citations = df.Citations.apply(
        lambda lst: "; ".join([refdf.loc[x, "value"] for x in lst])
    )
    df["doi"] = df.Citations.apply(parse_DOI)
    return df


def load_georoc_frame(path):
    """
    Munge GEOROC Data from pickle
    Data should be converted to numeric and units already.
    """
    df = load_sparse_pickle_df(path)
    return df


def georoc_munge(df):
    """
    Collection of munging and feature adding functions for GEROROC data.

    Todo: GEOL + AGE = AGE
    """
    mulitiple_cations = check_multiple_cation_inclusion(df)
    df = aggregate_cation(df, "Ti", form="element")
    df.loc[:, "GeolAge"] = df.loc[:, "Geol."].replace("None", "") + df.Age

    df.loc[:, "Lat"] = (df.LatitudeMax + df.LatitudeMin) / 2.0
    df.loc[:, "Long"] = (df.LongitudeMax + df.LongitudeMin) / 2.0
    return df
