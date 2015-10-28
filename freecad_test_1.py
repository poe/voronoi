
doc = FreeCAD.newDocument()
import random

points = []
for i in range(0,100):
  x = random.random() * 100
  y = random.random() * 100
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
    if abs(p1.x) < 100 and abs(p1.y) < 100 and abs(p2.x) < 100 and abs(p2.y) < 100:
      edge = Part.makeLine(p1,p2)
      tube = Part.makeTube(edge,0.5,"test_name")
      Part.show(tube)

doc.recompute()
Gui.SendMsgToActiveView("ViewFit")


