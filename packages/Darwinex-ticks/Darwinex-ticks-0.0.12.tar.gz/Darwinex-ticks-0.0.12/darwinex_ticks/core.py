# -*- coding: utf-8 -*-

from __future__ import print_function

# __all__ = ['download', 'darwinex', 'parse_ticker_csv', 'pdr_override']

from ftplib import FTP as _FTP
from io import BytesIO as _BytesIO
import sys as _sys

import pandas as _pd
from pandas.core.base import PandasObject


class DarwinexTicksConnection:
    """
    Object to connect with Darwinex Ticks Data Servers.
    """

    def __init__(self, dwx_ftp_user='<insert your Darwinex username>',
                 dwx_ftp_pass='<insert your Darwinex password>',
                 dwx_ftp_hostname='<insert Darwinex Tick Data FTP host>',
                 dwx_ftp_port=21):

        if dwx_ftp_hostname[:6] == 'ftp://':
            dwx_ftp_hostname = dwx_ftp_hostname[6:]

        # # Dictionary DB to hold dictionary objects in FX/Hour format
        # self._asset_db = {}

        self._ftpObj = _FTP(dwx_ftp_hostname)
        self._ftpObj.login(dwx_ftp_user, dwx_ftp_pass)
        self._virtual_dl = None
        self.available_assets = self._dir('')
        self._widgets_available = True
        print('Connected Darwinex Ticks Data Server')

    def close(self):
        try:
            msg = self._ftpObj.quit()
        except:
            msg = self._ftpObj.close()
        return msg

    def list_of_files(self, asset='EURUSD'):
        """Return a dataframe with the files on server for a asset.
        :param asset: str, a Darwinex asset
        :return: pandas.core.frame.DataFrame with asset files at Darwinex
        servers
        """

        _dir = _pd.DataFrame(self._ftpObj.nlst(asset)[2:])
        _dir['file'] = _dir[0]
        _dir[['asset', 'pos', 'date', 'hour']] = _dir[0].str.split('_',
                                                                   expand=True)
        _dir.drop(0, axis=1, inplace=True)
        _dir.hour = _dir.hour.str[:2]
        _dir['time'] = _pd.to_datetime(_dir.date + ' ' + _dir.hour)
        _dir.set_index('time', drop=True, inplace=True)
        return _dir

    def _dir(self, folder=None):
        return self._ftpObj.nlst(folder)[2:]

    def _get_file(self, _file):
        self._virtual_dl = _BytesIO()
        self._ftpObj.retrbinary("RETR {}".format(_file), self._virtual_dl.write)
        self._virtual_dl.seek(0)

    @staticmethod
    def _parser(_data):
        return _pd.to_datetime(_data, unit='ms', utc=False)

    def _get_ticks(self, asset='EURUSD', start=None, end=None,
                   cond=None, verbose=False, side='both',
                   separated=False, fill=True):

        if asset not in self.available_assets:
            raise KeyError('Asset {} not available'.format(asset))

        if cond is None:
            _files_df = self.list_of_files(asset)[start: end]
        else:
            _files_df = self.list_of_files(asset)[cond]

        if verbose is True:
            print("\n[INFO] Retrieving data from Darwinex Tick Data "
                  "Server..")

        side = side.upper()
        posits = ['ASK', 'BID']
        max_bar = _files_df.shape[0]
        if side in posits:
            posits = [side]
            max_bar /= 2

        data = {}

        if 'ipywidgets' in _sys.modules:
            from ipywidgets import FloatProgress as _FloatProgress
            from IPython.display import display as _display
            progressbar = _FloatProgress(min=0, max=max_bar)
            if max_bar > 1:
                _display(progressbar)
        elif self._widgets_available:
            print('You must install ipywidgets module to display progress bar '
                  'for notebooks.  Use "pip install ipywidgets"')
            self._widgets_available = False

        right_download = 0
        wrong_download = 0

        for posit in posits:
            _files = _files_df[_files_df.pos == posit]['file'].values
            _files = ['{}/{}'.format(asset, f) for f in _files]
            data_rec = []
            #             print(_files)
            for _file in _files:

                try:
                    self._get_file(_file)

                    # Construct DataFrame
                    pos = 'Ask' if 'ASK' in _file else 'Bid'

                    data_rec += [
                        _pd.read_table(self._virtual_dl, compression='gzip',
                                       sep=',', header=None,
                                       lineterminator='\n',
                                       names=['Time', pos, pos + '_size'],
                                       index_col='Time', parse_dates=[0],
                                       date_parser=self._parser)]
                    right_download += 1

                    if verbose is True:
                        print('Downloaded file {}'.format(_file))

                # Case: if file not found
                except Exception as ex:
                    _exstr = "\nException Type {0}. Args:\n{1!r}"
                    _msg = _exstr.format(type(ex).__name__, ex.args)
                    print(_msg)
                    wrong_download += 1

                if self._widgets_available:
                    progressbar.value += 1

            data[posit] = _pd.concat(data_rec, sort=True, axis=0,
                                     verify_integrity=False)

        if len(posits) == 2:
            if not separated:
                data = _pd.concat([data[posit] for posit in posits], axis=1)
                if fill:
                    data = data.ffill()

        else:
            data = data[posits[0]]

        print('Process completed. {} files downloaded'.format(right_download))
        if wrong_download > 0:
            print('{} files could not be downloaded.'.format(wrong_download))

        return data

    def ticks_from_darwinex(self, assets, start=None, end=None,
                            cond=None, verbose=False, side='both',
                            separated=False, fill=True):
        """

        :param assets: str with asset or list str assets to download data
        :param start: str datetime to start ticks data, if cond is not None
        start is ignored
        :param end: str datetime to end ticks data, if cond is not None
        end is ignored
        :param cond: str valid datetime value, eg '2017-12-24 12'. '2018-08'
        :param verbose: str display information of the process
        :param side: str 'ask', 'bid' or 'both'
        :param separated: True to return a dict with ask and bid separated,
        just available for one asset.
        :param fill: True, fill side gaps when both side are return. False,
        return NaN when one side don't change at this moment.
        :return: pandas.core.frame.DataFrame with ticks data for assets and
        conditions asked, or a dict of dataframe if separated is True and
        only one asset is asked.
        """

        if isinstance(assets, list):
            data_dict = {}
            for asset in assets:
                print('\n' + asset)
                data_dict[asset] = self._get_ticks(asset, start=start,
                                                   end=end, cond=cond,
                                                   verbose=verbose,
                                                   side=side,
                                                   separated=False, fill=fill)
            data = _pd.concat(data_dict, keys=data_dict.keys())
        else:
            data = self._get_ticks(assets, start=start,
                                   end=end, cond=cond,
                                   verbose=verbose, side=side,
                                   separated=separated, fill=fill)
        return data


# TOOLS

def spread(data, ask='Ask', bid='Bid', pip=None):
    if not all([_ in data.columns for _ in [ask, bid]]):
        raise KeyError('Parameters ask and bid must be column names')
    spreads = data[ask].sub(data[bid])
    if pip is not None:
        spreads = spreads.div(pip)
    return spreads


def to_mtcsv(data, path=None, decimals=5):
    csv = data[['Ask', 'Bid']].to_csv(path, header=False,
                                      float_format='%.{}f'.format(decimals))
    return csv


def price(data, method='midpoint', ask='Ask', bid='Bid', ask_size='Ask_size',
          bid_size='Bid_size'):
    if method == 'midpoint':
        price = data[[ask, bid]].mean(axis=1)
    elif method == 'weighted':
        price = (data[ask].mul(data[ask_size]).add(
            data[bid].mul(data[bid_size]))).div(
            data[ask_size].add(data[bid_size]))
    else:
        raise KeyError('Valid param method must be passed')
    return price


PandasObject.spread = spread
PandasObject.to_mtcsv = to_mtcsv
PandasObject.price = price
