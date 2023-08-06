""" Module holding custom conversion from dedaks to millis for images """

from ee import Image, EEException, Date, List
import daiquiri
from gee_pheno.exception import GEEException

class PHEDekad2Millis(object):
    def __init__(self, phe_img=None, tyear=None, **kwargs):

        logger = daiquiri.getLogger(__name__, subsystem="dekad2millis")
        self.logger = logger

        if not phe_img and not isinstance(phe_img, Image):
            raise TypeError("Phenology image is not correct")
        else:
            self.phe_img = phe_img

        self.logger.info("Target Year will be calculated from image")
        try:
            self.tyear = Date(
                phe_img.get('system:time_start')
            ).get('year')
        except EEException as e:
            raise GEEException(e.message)

        super(PHEDekad2Millis, self).__init__()

    @property
    def phey(self):  # @TODO check if dekad.py can help more
        """ Assign Phenology year based on dekad number
            0-36 = Target year - 1
            37-72 = Target year
            73 - 108 = Target year + 1, else = 0
        """

        return self.phe_img.expression(
            "(arg >108) ? 0 \
            : (arg >72) ? Ty+1 \
            : (arg >36) ? Ty \
            : Ty-1", {
                'arg': self.phe_img.select(0),
                'Ty': self.tyear
            }
        )

    @property
    def phem(self):  # @TODO check if dekad.py can help more
        """ Assign Phenology month based on dekad number
            0-36 = dekad/3 (rounded up)
            37-72 = (dekad-36)/3 (rounded up)
            73 - 108 = (dekad-72)/3 (rounded up)
        """

        return self.phe_img.expression(
            "(arg >108) ? 0 \
            : (arg >72) ? int(round((arg-72)/3+0.2)) \
            : (arg >36) ? int(round((arg-36)/3+0.2)) \
            : int(round((arg/3)+0.2))", {
                'arg': self.phe_img.select(0)
            }
        )

    @property
    def phed(self):  # @TODO check if dekad.py can help more
        """ Assign Phenology day based on dekad number: dekad/3-int(dekad/3)
            if > 0.6 then day = 11 (8/3 = 2.66 = second dekad  = 11)
            if > 0.3 then day = 1 (7/3 = 2.33 = first dekad  = 1)
            if < 0.3 then day = 21 (9/3 = 3.0 = third dekad  = 21)
        """

        return self.phe_img.expression(
            "(arg/3-int(arg/3))>0.6 ? 11 \
            :(arg/3-int(arg/3))>0.3 ? 1 \
            : 21", {
                'arg': self.phe_img.select(0)
            }
        )

    def _phe_bands_ymd_generator(self):
        """ Add generated YMD bands to phenology image

        """

        return self.phe_img.cat(
            [self.phey, self.phem.byte(), self.phed]
        ).rename(['PHEsY', 'PHEsM', 'PHEsD'])

    def _startyear2millis(self, y):
        #  Use pendulum?
        datey = "{0}-01-01".format(
            y
        )
        return Date(datey).millis()

    def _set_ymd_out(self, startY, endY):
        ee_ymillis_list = []
        for year in range(startY, endY + 1):
            ee_ymillis_list.append(
                self._startyear2millis(year).getInfo()
            )
        ee_mmillis_list = [
            0,
            2678400000,
            5097600000,
            7776000000,
            10368000000,
            13046400000,
            15638400000,
            18316800000,
            20995200000,
            23587200000,
            26265600000,
            28857600000
        ]
        ee_dmillis_list = [0, 864000000, 1728000000]
        return ee_ymillis_list, ee_mmillis_list, ee_dmillis_list

    def _datemillis(self, syear, eyear):
        dekads = [1, 11, 21]

        # yearly millis
        ymillis = self._phe_bands_ymd_generator().select(
            "PHEsY"
        ).interpolate(
            List.sequence(
                syear - 1,
                eyear + 1,
                1
            ),
            self._set_ymd_out(syear - 1, eyear + 1)[0],
            'mask'
        )
        self.logger.debug(
            "PHEsY interpolation image result {0}".format(
                ymillis.getInfo()
            )
        )
        # monthly millis
        mmillis = self._phe_bands_ymd_generator().select(
            "PHEsM"
        ).interpolate(
            List.sequence(
                1,
                12,
                1
            ),
            self._set_ymd_out(syear - 1, eyear + 1)[1],
            'mask'
        )
        self.logger.debug(
            "PHEsM interpolation image result {0}".format(
                mmillis.getInfo()
            )
        )
        # daily millis
        dmillis = self._phe_bands_ymd_generator().select(
            "PHEsD"
        ).interpolate(
            dekads,
            self._set_ymd_out(syear - 1, eyear + 1)[2],
            'mask'
        )
        self.logger.debug(
            "PHEsD interpolation image result {0}".format(
                dmillis.getInfo()
            )
        )

        return self.phe_img.cat(
            self._phe_bands_ymd_generator(),
            ymillis.add(mmillis).add(dmillis)
        )

    def apply(self, yos, yoe):
        return self.phe_img.addBands(
            self._datemillis(yos, yoe)
        )
