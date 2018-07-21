from random import randint, uniform

from aecSpace.aecColor import aecColor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

def beyondTower():
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """
    origin = aecPoint(0, 0, 0)
    spacer = aecSpacer()
    shaper = aecShaper()
    
    def full(point, xWidth, yDepth, zHeight, level):
        floor = aecSpace()
        floor.boundary = shaper.makeBox(point, xWidth, yDepth)
        floor.height = zHeight
        floor.level = level
        setColors([floor])
        return [floor]
    
    def halfDepth(point, xWidth, yDepth, zHeight, level):
        depth = yDepth * 0.5
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, xWidth, depth)
        half1.height = zHeight
        half1.level = level
        halfSpaces = [half1] + spacer.row(half1, xAxis = False)
        setColors(halfSpaces)
        return halfSpaces
    
    def halfWidth(point, xWidth, yDepth, zHeight, level):
        width = xWidth * 0.5
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, width, yDepth)
        half1.height = zHeight
        half1.level = level
        halfSpaces = [half1] + spacer.row(half1)
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterDepth(point, xWidth, yDepth, zHeight, level):
        if randint(0, 1) == 0:
            depth = yDepth * 0.25
            scale = 3
        else:
            depth = yDepth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, xWidth, depth)
        half1.height = zHeight
        half1.level = level        
        halfSpaces = [half1] + spacer.row(half1, xAxis = False)
        halfSpaces[1].scale(1, scale, 1, halfSpaces[1].points_floor[0])
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterWidth(point, xWidth, yDepth, zHeight, level):
        if randint(0, 1) == 0:
            width = xWidth * 0.25
            scale = 3
        else:
            width = xWidth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, width, yDepth)
        half1.height = zHeight
        half1.level = level        
        halfSpaces = [half1] + spacer.row(half1)
        halfSpaces[1].scale(scale, 1, 1, halfSpaces[1].points_floor[0])
        setColors(halfSpaces)
        return halfSpaces
    
    def setColors(halfSpaces):
        colors = [aecColor.blue, aecColor.orange, aecColor.purple, aecColor.yellow]
        colorPick = randint(0, 3)
        halfSpaces[0].color = colors[colorPick]
        if len(halfSpaces) == 1: return
        colors.reverse()
        halfSpaces[1].color = colors[colorPick]
    
    def makeFloor(point, xWidth, yDepth, zHeight, level):
        floorType = randint(0, 4)
        if floorType == 0: floorSpaces = full(point, xWidth, yDepth, zHeight, level)
        if floorType == 1: floorSpaces = halfDepth(point, xWidth, yDepth, zHeight, level)
        if floorType == 2: floorSpaces = halfWidth(point, xWidth, yDepth, zHeight, level)
        if floorType == 3: floorSpaces = quarterDepth(point, xWidth, yDepth, zHeight, level)
        if floorType == 4: floorSpaces = quarterWidth(point, xWidth, yDepth, zHeight, level)
        return floorSpaces
    
    def makeCore(point, xWidth, yDepth, zHeight): 
        xCoord = (point.x - 5) + (xWidth * 0.5)
        yCoord = point.y + yDepth
        point = aecPoint(xCoord, yCoord, point.z)
        core = aecSpace()
        core.boundary = shaper.makeBox(point, 10, 20)
        core.height = zHeight
        core.color = aecColor.gray
        return [core]
    
    def makeTower(point):
        floors = []
        xWidth = uniform(20, 60)
        yDepth = uniform(20, 60)
        levels = randint(5, 50)
        zHeight = uniform(3, 6)
        plinth = aecSpace()
        plinth.boundary = shaper.makeBox(point, xWidth, yDepth)
        plinthScaleX = (uniform(1, 2.5))
        plinthScaleY = (uniform(1, 2.5))
        plinth.scale(plinthScaleX, plinthScaleY, 2, plinth.centroid_floor)
        plinth.height = (zHeight * 2)
        plinth.color = aecColor.green
        floors.append(plinth)
        floors = floors + makeCore(point, xWidth, yDepth, zHeight * (levels + 3))
        level = (zHeight * 2)
        x = 0
        while x < levels:
            floors = floors + makeFloor(point, xWidth, yDepth, zHeight, level)
            level += zHeight
            x += 1       
        return floors
        
    tower = aecSpaceGroup()
    tower.add(makeTower(origin))
    return tower

# end aecSpaceDistributionExample

spaces = beyondTower()
spaceDrawer = aecSpaceDrawOCC()
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.

