"""Get data from the CSV and produce lists of jobs."""

from pandas import read_csv


class CsvDataFilterer:
    """Object which reads a CSV and then does stuff with its entries."""

    def __init__(self, csv_path, encoding="ISO-8859-1"):
        """Read CSV at `csv_path` and create dictionary from it."""

        try:
            data = read_csv(csv_path, encoding=encoding,
                            dtype={
                                "Job Title": str, "Location": str,
                                "Languages": str})
        except FileNotFoundError:
            raise ValueError("Couldn't open that CSV file")
        self.data = data

    def filter_proglang(self, lang: str) -> None:
        """Return only jobs for 'lang'."""
        def parse_list(list_str: str) -> list:
            """Parse a string representatin of a list into a list."""
            parsed = list_str.strip("][").split(", ")
            # Also strip the quotes from each individual string element
            parsed = [p.strip("'") for p in parsed]
            return parsed

        # j[-1] is the final column, "Language", so this should return
        # only languages where `lang` is in that column
        # Since the Languages column consists of list data written as
        # a string, to interpret it properly it needs parsing into a list,
        # which is why parse_list is used.
        self.filtered_data = [j for j in self.data.values
                              if lang in parse_list(j[-1])]
