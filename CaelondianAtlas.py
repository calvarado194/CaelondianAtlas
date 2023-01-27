from struct import *
from enum import Enum
import argparse
from StreamIO import StreamIO
import plotly.express as px

# Reimplementation of the Color class, as defined in .NET
class Color:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a


# Reimplementation of Bastion's BinaryLoadData class, that reads and parses a binary stream from a file
class BinaryLoadData:
    def __init__(self, stream):
        self.stream = StreamIO(stream)

    def bool(self) -> bool:
        return self.stream.read_byte()

    def float(self) -> float:
        return self.stream.read_float32()

    def int(self) -> int:
        return self.stream.read_int32()

    def int_list(self) -> list:
        n = self.stream.read_int32()
        l = []
        for i in range(n):
            l.append(self.stream.read_int32())

        return l

    def long(self) -> int:
        return self.stream.read_int64()

    def string(self) -> str:
        s = self.stream.read_string()
        return s

    def str_list(self) -> list:
        n = self.stream.read_int32()
        l = []
        for i in range(n):
            l.append(self.stream.read_string())

        return l

    def vector(self) -> tuple:
        return (self.stream.read_float32(), self.stream.read_float32())

    def color(self) -> Color:
        b = self.stream.read_byte()
        g = self.stream.read_byte()
        r = self.stream.read_byte()
        a = self.stream.read_byte()
        return Color(
            r,
            g,
            b,
            a)
        

    def enum(self, enum_type: Enum):
        return enum_type[self.stream.read_string()]

    def position(self):
        return self.stream.tell()


# Reimplementation of the general purpose GameDataManager in Bastion
class GameDataManager:
    def getUnitData(unit_name):
        return 1

    def getObstacleData(cunit_name):
        return 2

    def getGeneratorData(unit_name):
        return 3

    def getLootTableData(unit_name):
        return 4


# Reimplementation of the GameDataType enum in Bastion
class DataType(Enum):
    UNKNOWN = 0
    OBSTACLE = 1
    GENERATOR = 2
    UNIT = 3
    PROJECTILE = 4
    DAMAGE_FIELD = 5
    SPAWN_POINT = 6
    LOOT = 7
    MAP_AREA = 8
    TERRAIN_TILE = 9
    BACKDROP_FLYER = 10
    WEAPON = 11
    ANIMATION = 12


class DrawLayer(Enum):
    BACKGROUND = 0
    BACKGROUND_HIGH = 1
    SUBTERRAIN = 2
    TERRAIN = 3
    DECAL = 4
    DECAL_HIGH = 5
    GROUND = 6
    FLYING = 7
    OVERLAY = 8
    SUBTITLES = 9
    COUNT = 10


class TerrainTileType(Enum):
    FLOATIN = 0
    HUE = 1


# Reimplementation of the MapThing class in Bastion
class MapThing:
    m_groupNames = []

    def __init__(self, loader: BinaryLoadData):
        self.m_location = (0, 0)
        self.load(loader)

    def load(self, loader):
        n = loader.int()
        if n >= 1:
            self.data_type = DataType[loader.string()]
            self.m_name = loader.string()
            self.m_location = (loader.int(), loader.int())
        if n >= 2:
            self.m_active = loader.bool()
            self.m_activateWhenSeen = loader.bool()
        if n >= 3:
            self.m_endLocation = (loader.int(), loader.int())
        if n >= 4:
            self.m_id = loader.int()
        if n >= 5:
            self.m_activateOnEnterID = loader.int()
        if n >= 6:
            self.m_activateOnEnterName = loader.string()
        if n >= 7:
            self.m_activateOnEnterNames = loader.str_list()
        if n >= 8:
            self.m_requiresSolidGround = loader.bool()
        if n >= 9:
            self.m_groupName = loader.string()
        if n >= 10:
            self.m_useTargetAI = loader.bool()
            self.m_useMoveAI = loader.bool()
            self.m_useAttackAI = loader.bool()
        if n >= 11:
            # TODO: implement sprite effects class
            # this.m_flipEffect = (SpriteEffects)loadData.loadInt();
            self.m_flipEffect = loader.int()
        if n >= 12:
            self.m_flipHorizontal = loader.bool()
            self.m_flipVertical = loader.bool()
        if n >= 13:
            self.m_activateOnEnterIDs = loader.int_list()
        if n >= 14:
            self.DropLoot = loader.bool()
        if n >= 15:
            self.SortModifier = loader.int()
        if n >= 16:
            self.Color = loader.color()
        if n >= 17:
            self.Scale = loader.float()
        if n >= 18:
            self.UseUnexploredHue = loader.bool()
        if n >= 19:
            self.HealthFraction = loader.float()
        if n >= 20:
            self.Walkable = loader.bool()
        if n >= 21:
            self.Invulnerable = loader.bool()
        if n >= 22:
            self.UseAsFx = loader.bool()
            self.RotationSpeed = loader.float()
            self.DrawLayer = DrawLayer[loader.string()]
        if n >= 23:
            self.OffsetZ = loader.float()
        if n >= 24:
            self.Angle = loader.float()
        if n >= 25:
            self.FallIn = loader.bool()
        if n >= 26:
            self.AttachToID = loader.int()
        if n >= 27:
            self.ActivationRange = loader.float()
        if n >= 28:
            self.HelpTextId = loader.string()
        if n >= 29:
            self.Flying = loader.bool()
        if n >= 30:
            self.m_groupNames = loader.str_list()
            self.addToGroup(self.m_groupName)
        if n >= 31:
            self.GiveXP = loader.bool()
        if n >= 32:
            self.Friendly = loader.bool()
        if n >= 33:
            self.Parallax = loader.bool()
        if n >= 34:
            self.IgnoreGridManager = loader.bool()
        if n >= 35:
            self.Wobble = loader.bool()

    def getFirstGroupName(self) -> str:
        if not self.m_groupNames:
            return None

        return self.m_groupNames[0]

    def setGroupName(self, name):
        self.m_groupName = name
        self.m_groupNames = []
        self.m_groupNames.append(name)

    def addToGroup(self, name):
        if not name or name in self.m_groupNames:
            return
        
        self.m_groupNames.append(name)

    def to_dict(self):
        d = self.__dict__
        d['x'] = self.m_location[0]
        d['y'] = self.m_location[1]
        return d

    def __str__(self):
        return "Thing {} ({}), located at {}".format(self.m_name, self.data_type, self.m_location)


class MapThingGroup:
    def __init__(self, loader):
        self.load(loader)

    def load(self, loader):
        num = loader.int()
        if num >= 1:
            self.name = loader.string()
            self.m_things = {}
            num2 = loader.int()
            for i in range(num2):
                mapThing = MapThing(loader)
                if mapThing.getFirstGroupName() != self.name:
                    mapThing.setGroupName(self.name)

                valid = True

                if mapThing.data_type != DataType.UNKNOWN:
                    if mapThing.data_type == DataType.UNIT:
                        unitData = GameDataManager.getUnitData(mapThing.m_name)

                        if not unitData:
                            valid = False
                    if mapThing.data_type == DataType.OBSTACLE:
                        obstacleData = GameDataManager.getObstacleData(mapThing.m_name)

                        if not obstacleData:
                            valid = False
                    if (
                        mapThing.data_type == DataType.GENERATOR
                        and not GameDataManager.getGeneratorData(mapThing.m_name)
                    ):
                        obstacleData = GameDataManager.getObstacleData(mapThing.m_name)

                        if not obstacleData:
                            valid = False
                        else:
                            mapThing.data_type = DataType.OBSTACLE
                    if mapThing.data_type == DataType.LOOT:
                        lootTableData = GameDataManager.getLootTableData(
                            mapThing.m_name
                        )

                        if not lootTableData:
                            valid = False

                if valid and mapThing.m_id not in self.m_things:
                    self.m_things[mapThing.m_id] = mapThing

        self.m_visible = loader.bool()
        self.m_selectable = loader.bool()


# Reimplementation of the BloomSettings class in Bastion, which controls bloom settings for maps
class BloomSettings:
    def __init__(self, loader: BinaryLoadData):
        self.load(loader)

    def load(self, loader: BinaryLoadData):
        self.name = loader.string()
        self.bloomThreshold = loader.float()
        self.blurAmount = loader.float()
        self.bloomIntensity = loader.float()
        self.baseIntensity = loader.float()
        self.bloomSaturation = loader.float()
        self.baseSaturation = loader.float()


class Shader(Enum):
    NONE = 0
    REFRACT = 1
    DISSOLVE = 2
    CONTRAST = 3
    SATURATE = 4
    TERRAIN = 5
    OUTLINE = 6
    GOD_RAYS = 7


class GameData:
    m_name: str

    def __init__(self, name):
        self.name = name


class SpawnData:
    def __init__(self):
        pass

    def load(self, loader: BinaryLoadData):
        num = loader.int()
        if num >= 1:
            self.m_name = loader.string()
            self.m_num = loader.int()
        if num >= 2:
            self.m_maxAttempts = loader.int()


class SpawnWaveData:
    class Scale:
        m_countScalar: float
        m_intervalScalar: float

    m_spawns = []

    def __init__(self):
        pass

    def load(self, loader: BinaryLoadData):
        num = loader.int()
        if num >= 1:
            self.m_minInterval = loader.float()
            self.m_maxInterval = loader.float()
            num2 = loader.int()
            for i in range(num2):
                spawnData = SpawnData()
                spawnData.load(loader)
                self.m_spawns.append(spawnData)

            self.m_loopToWave = loader.int()
            self.m_repeatTimes = loader.int()
            self.m_scale = self.Scale()
            self.m_scale.m_countScalar = loader.float()
            self.m_scale.m_intervalScalar = loader.float()
        if num >= 2:
            self.m_firstSpawnMinInterval = loader.float()
            self.m_firstSpawnMaxInterval = loader.float()


class SpawnPointData(GameData):
    m_spawnWaves = []

    def __init__(self, name):
        super().__init__(name)

    def load(self, loader):
        num = loader.int()
        if num >= 1:
            self.m_name = loader.string()
            self.m_xOffsetMin = loader.int()
            self.m_xOffsetMax = loader.int()
            self.m_yOffsetMin = loader.int()
            self.m_yOffsetMax = loader.int()

            num2 = loader.int()
            for i in range(num2):
                spawnWaveData = SpawnWaveData()
                spawnWaveData.load(loader)
                self.m_spawnWaves.append(spawnWaveData)
        if num >= 2:
            self.m_snapHorizontal = loader.bool()
            self.m_snapVertical = loader.bool()


class TerrainLayerData:
    class BlendFilter(Enum):
        NONE = 0
        MULTIPLY = 1
        MASK = 2

    def __init__(self, loader: BinaryLoadData):
        self.init()
        num = loader.int()
        if num >= 1:
            self.name = loader.string()
            self.color = loader.color()
        if num >= 2:
            self.m_tiles = []
            num2 = loader.int()
            for i in range(num2):
                mapThing = MapThing(loader)
                self.m_tiles.append(mapThing)
        if num >= 3:
            self.m_linkedLayers = []
            num3 = loader.int()
            for j in range(num3):
                item = TerrainLayerData(loader)
                self.m_linkedLayers.append(item)
        if num >= 4:
            self.m_mask = loader.bool()
        if num >= 5:
            self.m_blendFilter = self.BlendFilter(loader.int())
        if num >= 6:
            self.shader = Shader(loader.int())
            self.contrast = loader.float()
        if num >= 7:
            self.saturation = loader.float()

    def init(self):
        self.visible = True
        self.selectable = True
        self.color = Color(255, 255, 255, 255)
        self.shader = None
        self.contrast = 0
        self.saturation = 0.3


# Reimplementation of the MapData class in Bastion, which is a container for map data.
class MapData:
    thingGroups = []
    m_things = []

    def __init__(self, stream):
        loader = BinaryLoadData(stream)

        num = loader.int()
        if num >= 1:
            if num < 20:
                self.m_things = []
                num2 = loader.int()
                for i in range(num2):
                    map_thing = MapThing(loader)
                    valid = True

                    if map_thing.data_type != DataType.UNKNOWN:
                        if map_thing.data_type == DataType.UNIT:
                            unitData = GameDataManager.getUnitData(map_thing.m_name)

                            if not unitData:
                                valid = False
                        if map_thing.data_type == DataType.OBSTACLE:
                            obstacleData = GameDataManager.getObstacleData(
                                map_thing.m_name
                            )

                            if not obstacleData:
                                valid = False
                        if (
                            map_thing.data_type == DataType.GENERATOR
                            and not GameDataManager.getGeneratorData(map_thing.m_name)
                        ):
                            obstacleData = GameDataManager.getObstacleData(
                                map_thing.m_name
                            )

                            if not obstacleData:
                                valid = False
                            else:
                                map_thing.data_type = DataType.OBSTACLE
                        if map_thing.data_type == DataType.LOOT:
                            lootTableData = GameDataManager.getLootTableData(
                                map_thing.m_name
                            )

                            if not lootTableData:
                                valid = False

                    if valid:
                        self.m_things.append(map_thing)

            self.m_spawmPointData = []
            num3 = loader.int()
            for j in range(num3):
                print("reading spawn data...")
                spawnPointData = SpawnPointData("")
                spawnPointData.load(loader)
                self.m_spawnPointData.append(spawnPointData)

            print("Reading start data...")
            self.startingCash = loader.int()
            self.m_name = loader.string()
            self.m_lootTableName = loader.string()
        if num >= 2:
            print("Reading pathfinders...")
            self.PathfinderBonus = loader.float()
        if num >= 3:
            print("Reading scroll numbers...")
            self.scrollSpeed = loader.float()
            self.scrollAngle = loader.float()
        if num >= 4:
            print("Reading size numbers...")
            self.m_size = (loader.int(), loader.int())
        if num >= 5:
            print("Reading music...")
            self.MusicName = loader.string()
        if num >= 6:
            print("Reading ambiance...")
            self.AmbienceName = loader.string()
        if num >= 7:
            print("Reading terrain layer data...")
            self.m_terrainLayerData = []
            num4 = loader.int()
            for k in range(num4):
                terrainLayerData = TerrainLayerData(loader)
                self.m_terrainLayerData.append(terrainLayerData)
                for item in terrainLayerData.m_linkedLayers:
                    self.m_terrainLayerData.append(item)
        if num >= 8:
            self.m_scripts = loader.str_list()
        if num >= 9:
            self.backdropTiles = loader.str_list()
            self.backdropColumns = loader.int()
            self.backdropColor = loader.color()
        if num >= 10:
            self.backdropFlyers = loader.str_list()
            self.backdropFlyerIntervalMin = loader.float()
            self.backdropFlyerIntervalMax = loader.float()
            self.backdropFlyerSpeedMin = loader.float()
            self.backdropFlyerSpeedMax = loader.float()
            self.backdropFlyerColor = loader.color()
        if num >= 11:
            self.FullBlackTime = loader.float()
            self.FadeInTime = loader.float()
        if num >= 12:
            self.backdropFlyerRefractRate = loader.float()
            self.backdropFlyerRefractAmount = loader.float()
        if num >= 13:
            self.backdropRows = loader.int()
        if num >= 14:
            self.backdropTileRefractRate = loader.float()
            self.backdropTileRefractAmount = loader.float()
        if num >= 15:
            self.preplacedBackdropFlyers = []
            num5 = loader.int()
            for l in range(num5):
                mapThing2 = MapThing(loader)
                if mapThing2.data_type != DataType.UNKNOWN:
                    self.preplacedBackdropFlyers.append(mapThing2)
        if num >= 16:
            self.backgroundBloomSetting = BloomSettings(loader)
            self.terrainBloomSetting = BloomSettings(loader)
        if num >= 17:
            self.backdropFlyerParallax = loader.float()
        if num >= 18:
            self.tileAssembleSound = loader.string()
        if num >= 19:
            self.terrainType = loader.enum(TerrainTileType)
            self.unexploredColor = loader.color()
        if num >= 20:
            num6 = loader.int()
            for m in range(num6):
                self.thingGroups.append(MapThingGroup(loader))
        if num >= 21:
            self.brightness = loader.float()
        if num >= 22:
            self.playerStartFall = loader.bool()
        if num >= 23:
            self.unexploredContrast = loader.float()
            self.unexploredSaturation = loader.float()
        if num >= 24:
            self.tilePhaseInTimeMin = loader.float()
            self.tilePhaseInTimeMax = loader.float()
        if num >= 25:
            self.terrainLightTexture = loader.string()
            self.terrainLightVelocity = loader.vector()
        if num >= 26:
            self.keepWeapons = loader.bool()
        if num >= 27:
            self.canPlantSeeds = loader.bool()
        if num >= 28:
            self.titleId = loader.string()
        if num >= 29:
            self.noWeapons = loader.bool()
        if num >= 30:
            self.parallax = loader.float()
        if num >= 31:
            self.backdropSaturaton = loader.float()
        if num >= 32:
            location = loader.vector()
            zoom = loader.float()

    def __str__(self) -> str:
        r = "Map: " + self.m_name + " {}. Music: {}".format(self.m_size, self.MusicName)
        return r


# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read map data from Bastion map files."
    )
    parser.add_argument("filename")
    args = parser.parse_args()
    f = open(args.filename, "rb")
    map_data = MapData(f)

    print(map_data)
    things = []
    for thing in map_data.m_things:
        things.append(thing.to_dict())
    for group in map_data.thingGroups:
        for thing in group.m_things:
            t = group.m_things[thing]
            things.append(t.to_dict())

    for t in map_data.m_terrainLayerData:
        for thing in t.m_tiles:
            things.append(thing.to_dict())


    things = [x for x in things if x['data_type'] != DataType.BACKDROP_FLYER]

    fig = px.scatter(things, x="x", y="y", color="m_name")
    fig.update_yaxes(autorange='reversed')
    fig.show()