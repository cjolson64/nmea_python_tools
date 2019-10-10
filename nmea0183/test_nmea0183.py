import unittest
from nmea0183 import *

class TestChecksum(unittest.TestCase):

    def test_checksum_passed(self):

        gga_string = '$GPGGA,172814.0,3723.46587704,N,12202.26957864,W,2,6,1.2,18.893,M,-25.669,M,2.0,0031*4F'

        self.assertEqual(nmea0183(gga_string).checksum_okay, True)


    def test_checksum_failed(self):

        zda_string = '$GPZDA,201530.18,04,07,2002,01,00*60'
        self.assertEqual(nmea0183(zda_string).checksum_okay, False)


# vim: set ts=4 sw=4 tw=0 et :
