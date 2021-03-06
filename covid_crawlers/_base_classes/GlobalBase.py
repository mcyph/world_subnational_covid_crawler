from os import listdir, makedirs
from os.path import exists
import datetime
from pathlib import Path
from abc import ABC, abstractmethod


_DEFAULT_DATE_FORMATS = (
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%Y_%m_%d',
    '%d-%m-%Y',
    '%d/%m/%Y',
    '%d_%m_%Y',
    '%d %B %Y',
    '%d %b %Y',
    '%d %B, %Y',
    '%d %b, %Y',
    '%d-%b-%y',
)


class GlobalBase(ABC):
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def iter_nonempty_dirs(self, p,
                           name_only=True,
                           newest_revision_only=False):
        p = Path(p)
        out = []

        for i in p.iterdir():
            if not i.is_dir():
                continue
            elif not any(p.iterdir()):
                continue
            out.append(i)

        # Sort so newer dates in format YYYY_MM_DD are first
        # TODO: Make it so that revisions are in order, too!
        out.sort(key=lambda x: x.name)

        if newest_revision_only:
            # TODO!!
            raise NotImplementedError()

        # Most of the time, we're only interested in the name (usually a date)
        if name_only:
            out = [i.name for i in out]
        return out

    #=============================================================#
    #                        Miscellaneous                        #
    #=============================================================#

    def _set_output_dir(self, dir_):
        """
        Update output dir after revision change
        """
        if isinstance(dir_, str):
            dir_ = Path(dir_)
        self.output_dir = dir_

    def convert_date(self, date, formats=_DEFAULT_DATE_FORMATS):
        if isinstance(formats, str):
            formats = (formats,)

        for format in formats:
            try:
                return datetime.datetime.strptime(date, format) \
                    .strftime('%Y_%m_%d')
            except:
                pass
        raise

    #=============================================================#
    #                            Paths                            #
    #=============================================================#

    def get_current_revision_dir(self, include_subid=False):
        if include_subid:
            raise NotImplementedError  # MAKE SURE to pad when implementing to allow binary sort!!
        else:
            return self.output_dir / sorted(listdir(self.output_dir))[-1]

    def get_today_revision_dir(self, include_subid=False):
        if include_subid:
            raise NotImplementedError
        else:
            new_dir = self.output_dir / datetime.datetime.now().strftime('%Y_%m_%d')
            if not exists(new_dir):
                makedirs(new_dir)
            return new_dir

    def get_path_in_dir(self, path):
        return self.output_dir / path

    #=============================================================#
    #                    Files and text data                      #
    #=============================================================#

    def get_text(self, path,
                 include_revision=False,
                 include_subid=False,
                 mode='r', encoding='utf-8', errors='replace'):

        if include_revision:
            path = self.get_current_revision_dir(include_subid) / path
        elif include_subid:
            raise Exception()
        else:
            path = self.output_dir / path

        try:
            with open(path, mode=mode, encoding=encoding, errors=errors) as f:
                return f.read()
        except UnicodeDecodeError:
            import brotli
            with open(path, mode=mode+'b') as f:
                return brotli.decompress(f.read()).decode(encoding, errors=errors)

    def get_file(self, path,
                 include_revision=False,
                 include_subid=False,
                 mode='r', encoding='utf-8', errors='replace'):

        if include_revision:
            path = self.get_current_revision_dir(include_subid) / path
        elif include_subid:
            raise Exception()
        else:
            path = self.output_dir / path

        return open(path, mode=mode, encoding=encoding, errors=errors)

    #=============================================================#
    #              Methods which must be overridden               #
    #=============================================================#

    @abstractmethod
    def update(self):
        # Should return the the current revision (if relevant)
        pass

    @abstractmethod
    def get_datapoints(self):
        pass
