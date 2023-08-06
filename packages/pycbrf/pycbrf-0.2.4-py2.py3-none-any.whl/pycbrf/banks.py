# -*- encoding: utf8 -*-
from __future__ import unicode_literals

import re
from collections import namedtuple, OrderedDict
from datetime import datetime
from logging import getLogger

import requests
from dbf_light import Dbf

from .exceptions import PycbrfException
from .utils import string_types, BytesIO

LOG = getLogger(__name__)


Bank = namedtuple(
    'Bank',
    [
        'bic',
        'name',
        'name_full',
        'region_code',
        'region',
        'zip',
        'place_type',
        'place',
        'address',
        'rkc_bic',
        'term',
        'date_added',
        'date_updated',
        'date_change',
        'mfo',
        'corr',
        'corr_bik',
        'phone',
        'telegraph',
        'commutator',
        'okpo',
        'regnum',
        'type',
        'pay_type',
        'control_code',
        'control_date',
        'swift',
    ]
)
"""Represents a bank.

Such objects will populate Banks().banks

"""


class Banks(object):

    def __init__(self, on_date=None, require_swift=False):
        """Fetches BIC data.

        :param datetime|str on_date: Date to get data for.
            Python date objects and ISO date string are supported.
            If not set data for today will be fetched.

        :param bool require_swift: Whether SWIFT data is required.

        """
        self.banks = self._get_data(on_date, require_swift=require_swift)

    def __getitem__(self, item):
        """
        :param str item:
        :rtype: Bank
        """
        if len(item) in [8, 11]:
            key = 'swift'
        else:
            key = 'bic'

        indexed = {getattr(bank, key): bank for bank in self.banks}

        return indexed[item]

    @classmethod
    def get_titles(cls):
        """Returns fields titles.

        :rtype: OrderedDict
        """
        titles = OrderedDict((
            ('bic', 'БИК'),  # Банковский идентификационный код
            ('swift', 'Код SWIFT'),
            ('name', 'Название'),
            ('name_full', 'Полное название'),

            ('date_added', 'Дата добавления записи'),
            ('date_updated', 'Дата обновления записи'),
            ('date_change', 'Дата изменения реквизитов'),

            ('control_code', 'Код контроля'),
            ('control_date', 'Дата контроля'),

            ('corr', 'Кор. счёт'),
            ('corr_bik', 'Кор. счёт (расчёты с БИК)'),

            ('regnum', 'Регистрационный номер'),
            ('mfo', 'Номер МФО'),
            ('okpo', 'Номер ОКПО'),  # Классификатор предприятий и организаций
            ('type', 'Тип'),
            ('pay_type', 'Тип расчётов'),

            ('region_code', 'Код региона ОКАТО'),  # Классификатор объектов административно-территориального деления
            ('region', 'Регион'),
            ('zip', 'Индекс'),
            ('place_type', 'Тип населённого пункта'),
            ('place', 'Населённый пункт'),
            ('address', 'Адрес'),

            ('phone', 'Телефон'),
            ('telegraph', 'Телеграф'),
            ('commutator', 'Коммутатор'),

            ('rkc_bic', 'БИК РКЦ'),  # Рассчётно-кассовый центр
            ('term', 'Срок проведения расчётов (дней)'),
        ))
        return titles

    @classmethod
    def annotate(cls, banks):
        """Annotates bank objects with titles.

        :param list[Bank] banks: A list of Bank objects to annotate.

        :rtype: list

        """
        titles = cls.get_titles()
        annotated = []

        def pick_value(in_dict):
            for key in ['name', 'fullname', 'uername']:
                val = in_dict.get(key)
                if val:
                    return val
            return '<no name>'

        for bank in banks:
            bank_dict = OrderedDict()
            bank = bank._asdict()

            for alias, title in titles.items():
                value = bank[alias]

                if isinstance(value, tuple):
                    value = pick_value(value._asdict())

                bank_dict[title] = value or ''

            annotated.append(bank_dict)

        return annotated

    @classmethod
    def _get_archive(cls, url):
        LOG.debug('Fetching data from %s ...', url)

        response = requests.get(url, stream=True, timeout=10)
        return BytesIO(response.content)

    @classmethod
    def _read_zipped_db(cls, zipped, filename):
        with Dbf.open_zip(filename, zipped, case_sensitive=False) as dbf:
            for row in dbf:
                yield row

    @classmethod
    def _get_data(cls, on_date=None, require_swift=False):

        if isinstance(on_date, string_types):
            on_date = datetime.strptime(on_date, '%Y-%m-%d')

        on_date = on_date or datetime.now()

        try:
            swifts = cls._get_data_swift()

        except PycbrfException:

            if require_swift:
                raise

            swifts = {}

        url = 'http://www.cbr.ru/vfs/mcirabis/BIK/bik_db_%s.zip' % on_date.strftime('%d%m%Y')
        zip = cls._get_archive(url)

        def get_indexed(dbname, index):
            return {getattr(region, index): region for region in cls._read_zipped_db(zip, filename=dbname)}

        regions = get_indexed('reg.dbf', 'rgn')
        types = get_indexed('pzn.dbf', 'pzn')
        place_types = get_indexed('tnp.dbf', 'tnp')
        pay_types = get_indexed('uer.dbf', 'uer')

        banks = []

        for row in cls._read_zipped_db(zip, filename='bnkseek.dbf'):
            region_code = row.rgn
            bic = row.newnum

            telegraph = []
            row.at1 and telegraph.append(row.at1)
            row.at2 and telegraph.append(row.at2)

            term = row.srok or 0

            if term:
                term = int(term)

            banks.append(Bank(
                bic=bic,
                name=row.namen,
                name_full=row.namep,
                region_code=region_code,
                region=regions.get(region_code),
                zip=row.ind,
                place_type=place_types.get(row.tnp),
                place=row.nnp,
                address=row.adr,
                rkc_bic=row.rkc,
                term=term,
                date_added=row.date_in,
                date_updated=row.dt_izm,
                date_change=row.dt_izmr,
                mfo=row.permfo,
                corr=row.ksnp,
                corr_bik=row.newks,
                phone=row.telef,
                telegraph=','.join(telegraph),
                commutator=row.cks,
                okpo=row.okpo,
                regnum=row.regn,
                type=types[row.pzn],
                pay_type=pay_types[row.uer],
                control_code=row.real,
                control_date=row.date_ch,
                swift=swifts.get(bic),
            ))

        return banks

    @classmethod
    def _get_data_swift(cls):
        # At some moment static URL has became dynamic, and now ne need to search for it every time.
        host = 'http://www.cbr.ru'
        response = requests.get('%s/analytics/digest/' % host, timeout=10)

        found = re.findall('href="([^."]+\.zip)"', response.text)

        if not found or len(found) > 1:
            raise PycbrfException('Unable to get SWIFT info archive link')

        url = host + found[0]

        items = {
            item.kod_rus: item.kod_swift for item in
            cls._read_zipped_db(cls._get_archive(url), filename='bik_swif.dbf')
        }
        return items
