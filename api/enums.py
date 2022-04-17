from enum import Enum


class Region(Enum):
    US_EAST_COAST     = 0x00
    US_WEST_COAST     = 0x01
    SOUTH_AMERICA     = 0x02
    EUROPE            = 0x03
    ASIA              = 0x04
    AUSTRALIA         = 0x05
    MIDDLE_EAST       = 0x06
    AFRICA            = 0x07
    REST_OF_THE_WORLD = 0xFF # Note, this actually selects EVERY REGION


class ServerGroupFilterType(str, Enum):
    IP = "ip"
    HOSTNAME = "hostname"
    

