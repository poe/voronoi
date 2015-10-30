
doc = FreeCAD.newDocument()
import random
from FreeCAD import Base
import Part

points = []
for i in range(0,30):
  x = random.random() * 200 - 100
  y = random.random() * 200 - 100
  points.append(FreeCAD.Base.Vector(x,y,0))

boxes = []
points_xy = []
for point in points:
  box = FreeCAD.ActiveDocument.addObject("Part::Box", "myBox")
  box.Length = 1
  box.Height = 1
  box.Width = 1
  rot = FreeCAD.Rotation(point,0)
  center = point
  pos = point
  newplace = FreeCAD.Placement(pos,rot,center)
  box.Placement = newplace
  boxes.append(box)
  points_xy.append([point.x,point.y])

from pyhull.voronoi import VoronoiTess
v = VoronoiTess(points_xy)
vertices =  v.vertices
floor_corner = FreeCAD.Base.Vector(-150,-150,0)
floor = Part.makeBox(250,250,1,floor_corner)
#Part.show(floor)

regions = v.regions
for region in regions:
  last_r = region[-1]
  for r in region:
    x = vertices[r][0]
    y = vertices[r][1]
    p1 = FreeCAD.Base.Vector(x,y,0)
    x = vertices[last_r][0]
    y = vertices[last_r][1]
    last_r = r
    p2 = FreeCAD.Base.Vector(x,y,0)

    if abs(p1.x) < 125 and abs(p1.y) < 125 and abs(p2.x) < 125 and abs(p2.y) < 125 and p1.x != -10.101 and p2.x != -10.101:
      edge = Part.makeLine(p1,p2)
      tube = Part.makeTube(edge,3)
      sphere = Part.makeSphere(8,p1)

      floor = floor.fuse(sphere)
#      floor = floor.fuse(tube)
      Part.show(tube)
Part.show(floor)
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")



