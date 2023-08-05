#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the bapsflib package, a Python toolkit for the
# BaPSF group at UCLA.
#
# http://plasma.physics.ucla.edu/
#
# Copyright 2017-2018 Erik T. Everson and contributors
#
# License: Standard 3-clause BSD; see "LICENSES/LICENSE.txt" for full
#   license terms and contributor agreement.
#
import numpy as np
import unittest as ut

from bapsflib._hdf import HDFMap
from unittest import mock

from . import TestBase
from ..lapdmap import LaPDMap


class TestLaPDMap(TestBase):
    """
    Test case for :class:`~bapsflib.lapd._hdf.lapdmap.LaPDMap`
    """

    @property
    def map(self):
        "LaPD map object"
        return LaPDMap(self.lapdf)

    def test_mapping(self):
        _lapdf = self.lapdf
        _map = self.map

        # LaPDMap subclasses HDFMap
        self.assertIsInstance(_map, HDFMap)

        # check paths
        self.assertTrue(hasattr(_map, 'DEVICE_PATHS'))
        self.assertEqual(_map.DEVICE_PATHS['control'],
                         'Raw data + config')
        self.assertEqual(_map.DEVICE_PATHS['digitizer'],
                         'Raw data + config')
        self.assertEqual(_map.DEVICE_PATHS['msi'], 'MSI')

        # additional attributes
        self.assertTrue(hasattr(_map, 'is_lapd'))
        self.assertTrue(hasattr(_map, 'lapd_version'))
        self.assertTrue(hasattr(_map, 'exp_info'))
        self.assertTrue(hasattr(_map, 'run_info'))

        self.assertIsInstance(type(_map).is_lapd, property)
        self.assertIsInstance(type(_map).lapd_version, property)
        self.assertIsInstance(type(_map).exp_info, property)
        self.assertIsInstance(type(_map).run_info, property)

        # -- examine `is_lapd` and `lapd_version`                   ----
        #
        # By defualt, FauxHDFBuilder adds the
        # 'LaPD HDF5 software version' attribute to the test file.
        lapd_version = \
            self.f.attrs['LaPD HDF5 software version'].decode('utf-8')
        self.assertTrue(_map.is_lapd)
        self.assertEqual(_map.lapd_version, lapd_version)

        # remove the LaPD version
        del self.f.attrs['LaPD HDF5 software version']
        self.assertFalse(_map.is_lapd)
        self.assertIsNone(_map.lapd_version)

        self.f.attrs['LaPD HDF5 software version'] = \
            np.bytes_(lapd_version)

        # -- examine `exp_info`                                     ----
        attrs = [
            ('Investigator', 'investigator'),
            ('Experiment name', 'exp name'),
            ('Experiment description', 'exp description'),
            ('Experiment set name', 'exp set name'),
            ('Experiment set description', 'exp set description'),
        ]
        path = 'Raw data + config'
        self.f[path].attrs['z'] = np.bytes_('z')
        for aname, iname in attrs:
            try:
                old_val = self.f[path].attrs[aname]
            except KeyError:
                old_val = 'something'
                self.f[path].attrs[aname] = old_val

            if isinstance(old_val, (np.bytes_, bytes)):
                old_val = old_val.decode('utf-8')

            # equality
            self.assertEqual(_map.exp_info[iname], old_val)

            # remove attribute
            del self.f[path].attrs[aname]
            self.assertEqual(_map.exp_info[iname], '')

            # return val
            if old_val == 'something':
                continue
            elif isinstance(old_val, str):
                old_val = np.bytes_(old_val)
            self.f[path].attrs[aname] = old_val
        del self.f[path].attrs['z']

        # -- examine `run_info`                                     ----
        attrs = [
            ('Data run', 'run name'),
            ('Description', 'run description'),
            ('Status', 'run status'),
            ('Status date', 'run date'),
        ]
        path = 'Raw data + config'
        self.f[path].attrs['z'] = np.bytes_('z')
        for aname, iname in attrs:
            try:
                old_val = self.f[path].attrs[aname]
            except KeyError:
                old_val = 'something'
                self.f[path].attrs[aname] = old_val

            if isinstance(old_val, (np.bytes_, bytes)):
                old_val = old_val.decode('utf-8')

            # equality
            self.assertEqual(_map.run_info[iname], old_val)

            # remove attribute
            del self.f[path].attrs[aname]
            self.assertEqual(_map.run_info[iname], '')

            # return val
            if old_val == 'something':
                continue
            elif isinstance(old_val, str):
                old_val = np.bytes_(old_val)
            self.f[path].attrs[aname] = old_val
        del self.f[path].attrs['z']

        # -- `__init__` waring                                      ----
        with mock.patch.object(LaPDMap, 'is_lapd',
                               new_callable=mock.PropertyMock,
                               return_value=False) as mock_il:
            with self.assertWarns(UserWarning):
                _map = self.map
                self.assertTrue(mock_il.called)


if __name__ == '__main__':
    ut.main()
