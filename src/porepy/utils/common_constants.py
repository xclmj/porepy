"""
The module is intended to give access to a set of unified keywords, units etc.

To access the quantities, invoke pp.KEY.

IMPLEMENTATION NOTE: This module may in the future be moved to an appropriate
submodule. The access via pp.will remain.

"""

""" Global keywords

Define unified keywords used throughout the software.
"""
DISCRETIZATION = "discretization"

COUPLING_DISCRETIZATION = "coupling_discretization"

PRIMARY_VARIABLES = "primary_variables"

PARAMETERS = "parameters"

DISCRETIZATION_MATRICES = "discretization_matrices"


""" Units """
# SI Prefixes
NANO = 1e-9
MICRO = 1e-6
MILLI = 1e-3
CENTI = 1e-2
DECI = 1e-1
KILO = 1e3
MEGA = 1e6
GIGA = 1e9

# Time
SECOND = 1.0
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365 * DAY

# Weight
KILOGRAM = 1.0
GRAM = 1e-3 * KILOGRAM

# Length
METER = 1.0
CENTIMETER = CENTI * METER
MILLIMETER = MILLI * METER
KILOMETER = KILO * METER

# Pressure related quantities
DARCY = 9.869233e-13
MILLIDARCY = MILLI * DARCY

PASCAL = 1.0
BAR = 101325 * PASCAL
ATMOSPHERIC_PRESSURE = BAR


GRAVITY_ACCELERATION = 9.80665 * METER / SECOND ** 2

# Temperature
CELSIUS = 1.0


def CELSIUS_to_KELVIN(celsius):
    return celsius + 273.15


def KELKIN_to_CELSIUS(kelvin):
    return kelvin - 273.15


# Force
NEWTON = KILOGRAM * METER / SECOND ** 2
