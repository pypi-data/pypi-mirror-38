# -*- coding: utf-8 -*-

""" Module holding custom filters for image collections """

from abc import ABCMeta, abstractmethod
from ee import Filter as FilterEE
from ee import Image as ImageEE
from ee import Date as DateEE
import daiquiri
from registry_decorator import register, register_all
from exception import GEEException

__all__ = []
factory = {}


class Filter(object):
    """ Abstract Base class for filters """

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def apply(self, coll_ee, *args, **kwargs):
        pass

@register(factory)
@register_all(__all__)
class PHESeason(Filter):
    """ Generic growing season filter

    :param season: all images within this will be filtered. Goes from 1
        to 2
    :type season: int
    :param year: all images over this will be filtered. Goes from 1970
        to now
    :type year: str
    :param kwargs:
    """

    def __init__(self, filters=None, *args, **kwargs):

        logger = daiquiri.getLogger(__name__, subsystem="filters")
        self.logger = logger

        super(PHESeason, self).__init__(filters=None, **kwargs)

        if not filters:
            self.filters = []
            self.logger.info("Filters are empty so they will be populated")
            self.logger.debug("Kwargs are: {0}".format(
                kwargs.items()
            ))
            for k, v in kwargs.items():
                logger.debug("key/value pair of filter is {0},{1}".format(
                    k, v
                ))
                # workaround because the property "year"
                # is not presente anymore
                if k == "year":
                    k = "time_extent"
                    v = "from {0}-01-01 to {0}-12-31".format(v)
                self.filters.append(
                    FilterEE.eq(k, v)
                )
        else:
            self.filters = filters

        self.logger.info("Filters are populated".format(
            self.filters
        ))
        for filter in self.filters:
            self.logger.debug("=== filter is ====> {0}".format(
                filter.getInfo()
            ))

    def apply(self, coll_ee, *args, **kwargs):
        """ Apply the filter

        :param col_ee: the image collection to apply the filter
        :type col_ee: ee.ImageCollection
        :param kwargs:
        :return:
        """

        reduxFirstImg = ImageEE(
            coll_ee.filter(
                self.filters
            ).first()
        )
        return reduxFirstImg


@register(factory)
@register_all(__all__)
class PHEStartSeason(PHESeason):
    """ Start growing season filter

    :param stage: starting time placeholder 's'
    :type stage: str

    """
    def __init__(self, **kwargs):

        if kwargs.has_key("stage"):
            if not kwargs["stage"] == "s":
                kwargs["stage"] = "s"
        else:
            kwargs["stage"] = "s"

        super(PHEStartSeason, self).__init__(**kwargs)


@register(factory)
@register_all(__all__)
class PHEEndSeason(PHESeason):
    """ End growing season filter

    :param stage: ending time placeholder 'e'
    :type stage: str

    """
    def __init__(self, **kwargs):

        if kwargs.has_key("stage"):
            if not kwargs["stage"] == "e":
                kwargs["stage"] = "e"
        else:
            kwargs["stage"] = "e"

        super(PHEEndSeason, self).__init__(**kwargs)


@register(factory)
@register_all(__all__)
class GrowingSeasonDate(PHESeason):
    """ Growing season start/end can span over three years

    """
    def __init__(self, **kwargs):

        if 'year' in kwargs.keys():
            self.year = kwargs.get("year")
        elif self.filters:
            for filter in self.filters:
                if 'time_extent' in filter["leftField"]:
                    self.year = filter["rightValue"][5:9]
        else:
            pass
        if not self.year:
            raise GEEException("Year is not defined")

        super(GrowingSeasonDate, self).__init__(**kwargs)

    def apply(self):
        """ Apply the filter

        :param year: define filter dates around target year. Goes from 1970
        to now. Growing season start/end can span over three years
        :type year: str
        :param kwargs:
        :return:
        """
        self.logger.debug("The target year for growing season is {0}".format(
            self.year
        ))
        GEE_dates = (
            DateEE.fromYMD(int(self.year) - 1, 1, 1),
            DateEE.fromYMD(int(self.year) + 1, 12, 31)
        )
        return GEE_dates
