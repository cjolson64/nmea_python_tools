class nmea0183:

    def __init__(self, sentence):

        checksum_parts = sentence.split('*')
        self.data = checksum_parts[0]
        self.computed_checksum = compute_nmea_checksum(self.data)
        # checksum is not required
        if (len(checksum_parts) == 2):
            self.checksum = checksum_parts[1]
            if (self.computed_checksum == self.checksum):
                self.checksum_okay = True
            else:
                self.checksum_okay = False

        else:
            self.checkum = None
            self.checksum_okay = None

        self.fields = self.data.split(',')
        label = self.fields[0]
        if (label[:1] != '$'):
            # Probably not a complete sentence
            pass

        self.talker = label[1:3]
        self.talker_description = self._NMEA_TALKERS[self.talker]
        self.message_type = label[3:]
        self.message_type_description = self._NMEA_MESSAGES__[self.message_type]

        if (self.message_type == 'GGA'):
            self.__class__ = gga
            self.parse_fields()
        elif (self.message_type == 'ZDA'):
            self.__class__ = zda
            self.parse_fields()


    # Shamelessly taken from https://fishandwhistle.net/post/2016/using-pyserial-pynmea2-and-raspberry-pi-to-log-nmea-output/

    _NMEA_TALKERS = {'AG': 'Autopilot(General)',
                     'AP': 'Autopilot(Magnetic)',
                     'CC': 'Programmed Calculator',
                     'CD': 'DSC (Digital Selective Calling)',
                     'CM': 'Memory Data',
                     'CS': 'Satellite Communications',
                     'CT': 'Radio-Telephone (MF/HF)',
                     'CV': 'Radio-Telephone (VHF)',
                     'CX': 'Scanning Receiver',
                     'DE': 'DECCA Navigation',
                     'DF': 'Direction Finder',
                     'DM': 'Magnetic Water Velocity Sensor',
                     'EC': 'ECDIS (Electronic Chart Display & Information System)',
                     'EP': 'EPIRB (Emergency Position Indicating Beacon)',
                     'ER': 'Engine Room Monitoring Systems',
                     'GP': 'GPS',
                     'HC': 'Magnetic Compass',
                     'HE': 'North Seeking Gyro',
                     'HN': 'Non-North Seeking Gyro',
                     'II': 'Integrated Instrumentation',
                     'IN': 'Integrated Navigation',
                     'LA': 'Loran A',
                     'LC': 'Loran C',
                     'MP': 'Microwave Positioning System',
                     'OM': 'OMEGA Navigation System',
                     'OS': 'Distress Alarm System',
                     'RA': 'RADAR and/or ARPA',
                     'SD': 'Depth Sounder',
                     'SN': 'Electronic Positioning System',
                     'SS': 'Scanning Sounder',
                     'TI': 'Turn Rate Indicator',
                     'TR': 'TRANSIT Navigation System',
                     'VD': 'Doppler Velocity Sensor',
                     'VW': 'Mechanical Water Velocity Sensor',
                     'WI': 'Weather Instruments',
                     'YC': 'Temperature Transducer',
                     'YD': 'Displacement Transducer',
                     'YF': 'Frequency Transducer',
                     'YL': 'Level Transducer',
                     'YP': 'Pressure Transducer',
                     'YR': 'Flow Rate Transducer',
                     'YT': 'Tachometer Transducer',
                     'YV': 'Volume Transducer',
                     'YX': 'Transducer',
                     'ZA': 'Atomic Clock Timekeeper',
                     'ZC': 'Chronometer Timekeeper',
                     'ZQ': 'Quartz Clock Timekeeper',
                     'ZV': 'Radio Update Timekeeper',
    }
    
    _NMEA_MESSAGES__ = {'GNS': 'Fix data',
                        'DPT': 'Depth of Water',
                        'GST': 'GPS Pseudorange Noise Statistics',
                        'DTM': 'Datum Reference',
                        'GSV': 'Satellites in view',
                        'AAM': 'Waypoint Arrival Alarm',
                        'FSI': 'Frequency Set Information',
                        'VHW': 'Water speed and heading',
                        'GLC': 'Geographic Position, Loran-C',
                        'MSS': 'Beacon Receiver Status',
                        'PASHR': 'RT300 proprietary roll and pitch sentence',
                        'GSA': 'GPS DOP and active satellites',
                        'VDR': 'Set and Drift',
                        'MSK': 'Control for a Beacon Receiver',
                        'GBS': 'GPS Satellite Fault Detection',
                        'TPC': 'Trawl Position Cartesian Coordinates',
                        'HFB': 'Trawl Headrope to Footrope and Bottom',
                        'ZTG': 'UTC & Time to Destination Waypoint',
                        'MWV': 'Wind Speed and Angle',
                        'DCN': 'Decca Position',
                        'HSC': 'Heading Steering Command',
                        'PUBX 00': 'uBlox Lat/Long Position Data',
                        'PRWIZCH': 'Rockwell Channel Status',
                        'OLN': 'Omega Lane Numbers',
                        'RMB': 'Recommended Minimum Navigation Information',
                        'RMC': 'Recommended Minimum Navigation Information',
                        'RMA': 'Recommended Minimum Navigation Information',
                        'GGA': 'Global Positioning System Fix Data',
                        'TTM': 'Tracked Target Message',
                        'PGRME': 'Garmin Estimated Error',
                        'ROT': 'Rate Of Turn',
                        'OSD': 'Own Ship Data',
                        'VLW': 'Distance Traveled through Water',
                        'WPL': 'Waypoint Location',
                        'PUBX 01': 'uBlox UTM Position Data',
                        'RTE': 'Routes',
                        'GTD': 'Geographic Location in Time Differences',
                        'GRS': 'GPS Range Residuals',
                        'VTG': 'Track made good and Ground speed',
                        'WCV': 'Waypoint Closure Velocity',
                        'PMGNST': 'Magellan Status',
                        'STN': 'Multiple Data ID',
                        'MTW': 'Mean Temperature of Water',
                        'TRF': 'TRANSIT Fix Data',
                        'TDS': 'Trawl Door Spread Distance',
                        'XTE': 'Cross-Track Error, Measured',
                        'TPT': 'Trawl Position True',
                        'TPR': 'Trawl Position Relative Vessel',
                        'PUBX 03': 'uBlox Satellite Status',
                        'R00': 'Waypoints in active route',
                        'DBK': 'Depth Below Keel',
                        'ALM': 'GPS Almanac Data',
                        'TFI': 'Trawl Filling Indicator',
                        'PUBX 04': 'uBlox Time of Day and Clock Information',
                        'RSD': 'RADAR System Data',
                        'RPM': 'Revolutions',
                        'RSA': 'Rudder Sensor Angle',
                        'VWR': 'Relative Wind Speed and Angle',
                        'ITS': 'Trawl Door Spread 2 Distance',
                        'LCD': 'Loran-C Signal Data',
                        'SFI': 'Scanning Frequency Information',
                        'APB': 'Autopilot Sentence "B"',
                        'VBW': 'Dual Ground/Water Speed',
                        'DBS': 'Depth Below Surface',
                        'APA': 'Autopilot Sentence "A"',
                        'DBT': 'Depth below transducer',
                        'ZFO': 'UTC & Time from origin Waypoint',
                        'ZDA': '',
    }


class gga(nmea0183):

    def __init__(self, sentence):

        super().__init__(sentence)
        self.parse_fields

    def parse_fields(self):
        self.time = float(self.fields[1])
        self.lat = latdm2dd(self.fields[2], self.fields[3])
        self.lon = londm2dd(self.fields[4], self.fields[5])
        self.quality = int(self.fields[6])
        self.number_of_satellites = int(self.fields[7])
        self.hdop = float(self.fields[8])
        self.altitude_above_mean_sea_level = altitude2meters(self.fields[9], self.fields[10])
        self.altitude_above_mean_geoid = altitude2meters(self.fields[11], self.fields[12])
        try:
            self.seconds_since_dgps_update = float(self.fields[13])
        except ValueError:
            self.seconds_since_dgps_update = None

        try:
            self.dgps_station_id = int(self.fields[14])
        except ValueError:
            self.dgps_station_id = None



    def print_help(self):

        example = """ 
gga_string = '$GPGGA,172814.0,3723.46587704,N,12202.26957864,W,2,6,1.2,18.893,M,-25.669,M,2.0,0031*4F'

$GPGGA,hhmmss.ss,ddmm.mmmm,n,dddmm.mmmm,e,q,ss,y.y,a.a,z,g.g,z,t.t,iiii*CC


    GGA           Global Positioning System Fix Data
    123519        Fix taken at 12:35:19 UTC
    4807.038,N    Latitude 48 degrees 07.038 minutes North
    01131.000,E   Longitude 11 degrees 31.000 minutes East
    1             Fix quality: 0 = fix not available or invalid
                               1 = GPS Standard Positioning Service (SPS) mode, fix valid
                               2 = differential GPS (DGPS), SPS mode, fix valid
                               3 = GPS Precise Point Positioning (PPS) mode, fix valid
                               4 = Real Time Kinematic (RTK). Satellite system used in
                                   RTK mode with fixed integers.
                               5 = Float RTK.  Satellite system used in RTK mode with
                                   floating integers.
                               6 = Estimated (dead reckoning) mode
                               7 = Manual input mode
                               8 = Simulator mode
    08            Number of satellites being tracked
    0.9           Horizontal dilution of precision (HDOP)
    545.4,M       Altitude above mean sea level [meters]
    46.9,M        Height of geoid (mean sea level) above WGS84 ellipsoid [meters]
    (empty field) Time in seconds since last DGPS update
    (empty field) DGPS station ID number
    *47           Checksum, always begins with *    

"""

        print(example)


class zda(nmea0183):

    def __init__(self, sentence):

        super().__init__(sentence)
        self.parse_fields

    def parse_fields(self):
        self.time = float(self.fields[1])
        self.day = int(self.fields[2])
        self.month = int(self.fields[3])
        self.year = int(self.fields[4])
        self.timezone_offset_hours = int(self.fields[5])
        self.timezone_offset_minutes = int(self.fields[6])


    def print_help(self):

        example = """ 
ZDA - Date and Time

Example Record: $GPZDA,201530.18,04,07,2002,01,00*60

where:
     201530.18  hours, minutes, and seconds expressed as hhmmss.ss
                 20       2-digit hour [24 hour clock]
                 15       2-digit minute 
                 30.18    decimal seconds
     04         2-digit day, 
     07         2-digit month
     2002       4-digit year
     01         2-digit local timezone hours: -13 to 13
     00         2-digit local timezone minutes: 0 to 59
     *60        Checksum, begins with *
"""

        print(example)



def latdm2dd(latdm, hemi):
    degrees = float(latdm[:2])
    minutes = float(latdm[3:])
    dd = degrees + (minutes/60)

    if (hemi == 'S'):
        dd = -1 * dd

    return dd


def londm2dd(londm, hemi):
    degrees = float(londm[:3])
    minutes = float(londm[4:])
    dd = degrees + (minutes/60)

    if (hemi == 'W'):
        dd = -1 * dd

    return dd


def altitude2meters(altitude, units):
    if (units == 'M'):
        try:
            alt = float(altitude)
        except ValueError:
            alt = None
    else:
        alt = None

        return alt


def compute_nmea_checksum(string):

    csum = 0
    for elem in string.lstrip('$'):
        csum ^= ord(elem)

    computed_checksum = format(csum, 'X')

    return computed_checksum


# vim: set ts=4 sw=4 tw=0 et :
