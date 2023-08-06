# -*- coding: utf-8 -*-

from ee import Filter as FilterEE
from ee import Image as ImageEE
from ee import ImageCollection as ImageCollectionEE
from ee import EEException
import daiquiri
from exception import GEEException
from filters import (
    PHEStartSeason,
    PHEEndSeason,
    GrowingSeasonDate
)
from util.dekad2millis import PHEDekad2Millis


class Phenology(object):
    """ Calculate GEE phenology metrics for each record
    GEE phenology metrics describe the general season start and end
    using an algorithm by Livia Peiser from FAO, 2017 based
    on dekads.
    Attributes:
        self.pheno (xarray.Dataset): Xarray structured dataset containing
            phenology metrics. These metrics include:
            * PHEsos_img: annual time series of the start of season (ee.Image)
            * PHEeos_img: annual time series of the end of season (ee.Image)
            * ini_date: filter start date around target year (ee.Date)
            * end_date: filter end date around target year (ee.Date)
            * PHEstart: start date expressed in millis from phenology dekad
                number (ee.Image)
            * PHEend: end date expressed in millis from phenology dekad
                number (ee.Image)
            * season_s: season start expressed in millis from phenology
                dekad number (ee.Image)
            * season_e: season end expressed in millis from phenology
                dekad number (ee.Image)

    Args:
        PHE_coll (ee.ImageCollection, mandatory): multi-dimensional raster of
            Phenology data
        year (string, mandatory): target year of interest
        season (int, mandatory): season of interest

    """

    def __init__(self, **kwargs):
        logger = daiquiri.getLogger(__name__, subsystem="pheno")
        self.logger = logger
        self.logger.info("==========INIT Phenology===========")
        super(Phenology, self).__init__()
        self.logger.debug("===phe_coll====> {0}".format(
            kwargs.get("phe_coll")
        ))
        self.PHE_coll = self._phecoll(kwargs.get("phe_coll"))
        self.logger.debug("===year====> {0}".format(
            kwargs.get("year")
        ))
        self.year = kwargs.get("year")
        self.logger.debug("===season====> {0}".format(
            kwargs.get("season")
        ))
        self.season = kwargs.get("season")
        if "area_code" in kwargs:
            self.area = kwargs["area_code"]

    def _phecoll(self, asset_id):
        try:
            imgColl = ImageCollectionEE(asset_id)
            return imgColl
        except EEException as e:
            raise GEEException(e.message)

    @property
    def start_year(self):
        try:
            starty = self.PHE_coll.sort('system:time_start', True).first().get(
                'time_extent'
            ).getInfo()[5:9]
            return int(starty)
        except EEException as e:
            raise GEEException(e.message)

    @property
    def end_year(self):
        try:
            endy = self.PHE_coll.sort('system:time_start', False).first().get(
                'time_extent'
            ).getInfo()[5:9]
            return int(endy)
        except EEException as e:
            raise GEEException(e.message)

    @property
    def PHEsos_img(self):
        kw_soy = {
            "year": self.year,
            "season": self.season
        }
        if self.area:
            kw_soy.update(area_code=self.area)
        return PHEStartSeason(**kw_soy).apply(self.PHE_coll)

    @property
    def PHEeos_img(self):
        kw_soy = {
            "year": self.year,
            "season": self.season
        }
        if self.area:
            kw_soy.update(area_code=self.area)
        return PHEEndSeason(**kw_soy).apply(self.PHE_coll)

    @property
    def ini_date(self):
        kw_soy = {
            "year": self.year
        }
        return GrowingSeasonDate(**kw_soy).apply()[0]

    @property
    def end_date(self):
        kw_soy = {
            "year": self.year
        }
        return GrowingSeasonDate(**kw_soy).apply()[1]

    @property
    def PHEstart(self):
        kw_phety = {
            "phe_img": self.PHEsos_img,
            "tyear": self.year
        }
        return PHEDekad2Millis(**kw_phety).apply(
            self.start_year,
            self.end_year
        )

    @property
    def PHEend(self):
        kw_phety = {
            "phe_img": self.PHEeos_img,
            "tyear": self.year
        }
        return PHEDekad2Millis(**kw_phety).apply(
            self.start_year,
            self.end_year
        )

    @property
    def season_s(self):
        return self.PHEstart.select([4])

    @property
    def season_e(self):
        return self.PHEend.select([4])
