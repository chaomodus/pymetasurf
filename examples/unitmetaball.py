# An example of using pymetasurf to create objects in Panda3d
# Written by Cas Rusnov <rusnovn@gmail.com>

import pymetasurf

from pandac.PandaModules import loadPrcFile
configfiles = ["./Config.prc",]
for prc in configfiles:
    loadPrcFile(prc)


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomNode, GeomTriangles
from math import pi, sin, cos


um = pymetasurf.UnitMetaball()
um.set_resolution(40,40,40)
um.set_bounds(-3, -3, -3, 3, 3, 3)
um.polygonize()
format=GeomVertexFormat.getV3n3c4()
vdata=GeomVertexData("vertices", format, Geom.UHStatic)
vertexWriter=GeomVertexWriter(vdata, "vertex")
for p in um.tri_list:
    vertexWriter.addData3f(p[0],p[1],p[2])
normalWriter=GeomVertexWriter(vdata, "normal")
for p in um.normal_list:
    normalWriter.addData3f(p[0],p[1],p[2])

colorWriter=GeomVertexWriter(vdata, "color")
for p in um.tri_list:
    colorWriter.addData4f(1.0 - (p[0] * 0.1),1.0 - (p[1] * 0.1), 1.0 - (p[2] * 0.1),1.0)

tris = GeomTriangles(Geom.UHStatic)
tris.addConsecutiveVertices(0, len(um.tri_list))
tris.closePrimitive()

um_geom = Geom(vdata)
um_geom.addPrimitive(tris)

um_GN = GeomNode("UnitMetaball")
um_GN.addGeom(um_geom)


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.render.attachNewNode(um_GN)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 30.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.lookAt(0,0,0)
        self.camera.setPos(10 * sin(angleRadians), -10.0 * cos(angleRadians), 0.0)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
