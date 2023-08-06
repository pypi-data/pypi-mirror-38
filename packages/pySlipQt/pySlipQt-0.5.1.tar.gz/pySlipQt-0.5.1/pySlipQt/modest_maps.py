"""
A tile source that serves OpenStreetMap tiles from the internet.

Uses pyCacheBack to provide in-memory and on-disk caching.
"""

import math

import pySlipQt.tiles_net as tiles


# if we don't have log.py, don't crash
try:
    from pySlipQt import log
    log = log.Log('pyslip.log')
except AttributeError:
    # means log already set up
    pass
except ImportError as e:
    # if we don't have log.py, don't crash
    # fake all log(), log.debug(), ... calls
    def logit(*args, **kwargs):
        pass
    log = logit
    log.debug = logit
    log.info = logit
    log.warn = logit
    log.error = logit
    log.critical = logit


###############################################################################
# Change values below here to configure an internet tile source.
###############################################################################

# attributes used for tileset introspection
# names must be unique amongst tile modules
TilesetName = 'ModestMaps Tiles'
TilesetShortName = 'MM Tiles'
TilesetVersion = '1.0'

# the pool of tile servers used
TileServers = ['http://c.tiles.mapbox.com',
              ]

# the path on the server to a tile
# {} params are Z=level, X=column, Y=row, origin at map top-left
TileURLPath = '/v3/examples.map-szwdot65/{Z}/{X}/{Y}.png'

# tile levels to be used
TileLevels = range(17)

# maximum pending requests for each tile server
MaxServerRequests = 2

# set maximum number of in-memory tiles for each level
MaxLRU = 10000

# size of tiles
TileWidth = 256
TileHeight = 256

# where earlier-cached tiles will be
# this can be overridden in the __init__ method
TilesDir = 'modest_maps_tiles'

################################################################################
# Class for these tiles.   Builds on tiles.BaseTiles.
################################################################################

class Tiles(tiles.Tiles):
    """An object to source internet tiles for pySlip."""

    def __init__(self, tiles_dir=TilesDir, http_proxy=None):
        """Override the base class for these tiles.

        Basically, just fill in the BaseTiles class with values from above
        and provide the Geo2Tile() and Tile2Geo() methods.
        """

#        super(Tiles, self).__init__(TileLevels, TileWidth, TileHeight,
#                                    servers=TileServers, url_path=TileURLPath,
#                                    max_server_requests=MaxServerRequests,
#                                    max_lru=MaxLRU, tiles_dir=tiles_dir,
#                                    http_proxy=http_proxy)
        super(Tiles, self).__init__(levels=TileLevels,
                                    tile_width=TileWidth, tile_height=TileHeight,
                                    tiles_dir=tiles_dir, max_lru=MaxLRU,
                                    servers=TileServers, url_path=TileURLPath,
                                    max_server_requests=MaxServerRequests,
                                    http_proxy=http_proxy)


    def Geo2Tile(self, geo):
        """Convert geo to tile fractional coordinates for level in use.

        geo  tuple of geo coordinates (xgeo, ygeo)

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """

        (xgeo, ygeo) = geo
        lat_rad = math.radians(ygeo)
        n = 2.0 ** self.level
        xtile = (xgeo + 180.0) / 360.0 * n
        ytile = ((1.0 - math.log(math.tan(lat_rad) + (1.0/math.cos(lat_rad))) / math.pi) / 2.0) * n

        return (xtile, ytile)

    def Tile2Geo(self, tile):
        """Convert tile fractional coordinates to geo for level in use.

        tile  a tupl;e (xtile,ytile) of tile fractional coordinates

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """

        (xtile, ytile) = tile
        n = 2.0 ** self.level
        xgeo = xtile / n * 360.0 - 180.0
        yrad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        ygeo = math.degrees(yrad)

        return (xgeo, ygeo)
