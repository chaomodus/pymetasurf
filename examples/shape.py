# An example of using pymetasurf to create objects in Panda3d
# Written by Cas Rusnov <rusnovn@gmail.com>

import pymetasurf
import pymetasurf.shapes as shapes

from pandac.PandaModules import loadPrcFile
configfiles = ["./Config.prc",]
for prc in configfiles:
    loadPrcFile(prc)

import sys
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, PointLight, VBase4, AmbientLight, Spotlight, Vec4, DirectionalLight, Material
from panda3d.core import Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomNode, GeomTriangles
from math import pi, sin, cos, tan, sqrt, exp, radians


class spherical_coordinate(object):
    def __init__(self, rho=1, theta=0, phi=0):
        self.rho = rho
        self.theta = theta
        self.phi = phi

    @property
    def x(self):
        return self.rho * sin(radians(self.theta)) * cos(radians(self.phi))

    @property
    def y(self):
        return self.rho * sin(radians(self.theta)) * sin(radians(self.phi))

    @property
    def z(self):
        return self.rho * cos(radians(self.theta))

    def __str__(self):
        return "<scoord %d %d %d>" % (self.rho, self.theta, self.phi)

def sqr(x):
    return x**2

class meta_generic(pymetasurf.MetaSurface):
    def __init__(self, shapespec):
        pymetasurf.MetaSurface.__init__(self)
        self.set_inside(shapespec[0])
        self.set_bounds(*shapespec[1])
        self.set_resolution(*shapespec[2])
        self.func = shapespec[3]

    def eval_callback(self, x, y, z):
        return self.func(x,y,z);

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.render.setShaderAuto()

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.25, 0.25, 0.25, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)
        # Directional light 01
        directionalLight = DirectionalLight('directionalLight')
        directionalLight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        directionalLightNP = self.render.attachNewNode(directionalLight)
        self.dlnp = directionalLightNP
        # This light is facing backwards, towards the camera.
        directionalLightNP.setHpr(180, -20, 0)
        self.render.setLight(directionalLightNP)

        n = self.render.attachNewNode(um_GN)
        myMaterial = Material()
        myMaterial.setShininess(30.0) #Make this material shiny
        myMaterial.setAmbient(VBase4(1,1,1,1))
        myMaterial.setDiffuse(VBase4(0.5,0.6,0.5,1))
        myMaterial.setSpecular(VBase4(1,1,1,1))
        myMaterial.setTwoside(True)
        n.setMaterial(myMaterial)
        n.reparentTo(self.render)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        class KeyMgr(DirectObject.DirectObject):
            def __init__(self):
                self.states = {'up':False,'down':False,'left':False,'right':False,'pgup':False,'pgdn':False, 'a':False}
                self.accept('arrow_up',self.state, ['up', True])
                self.accept('arrow_up-up',self.state, ['up', False])
                self.accept('arrow_down',self.state, ['down', True])
                self.accept('arrow_down-up',self.state, ['down', False])
                self.accept('arrow_left',self.state, ['left', True])
                self.accept('arrow_left-up',self.state, ['left', False])
                self.accept('arrow_right',self.state, ['right', True])
                self.accept('arrow_right-up',self.state, ['right', False])
                self.accept('page_up',self.state, ['pgup',True])
                self.accept('page_up-up',self.state, ['pgup',False])
                self.accept('page_down',self.state, ['pgdn',True])
                self.accept('page_down-up',self.state, ['pgdn',False])
                self.accept('a', self.impulse, ['a',])
                self.accept('escape', sys.exit ) # exit on esc

                self.impulses = list()

            def state(self, key, st):
                self.states[key] = st
            def impulse(self, key):
                self.impulses.append(key)

            def __getitem__(self, key):
                return self.states.__getitem__(key)

        self.keymgr = KeyMgr()
        self.auto = False
        self.campos = spherical_coordinate(10,90,90)


    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        if self.keymgr['up']:
            self.campos.theta += 1
        if self.keymgr['down']:
            self.campos.theta -= 1
        if self.keymgr['left'] or self.auto:
            self.campos.phi -= 1
        if self.keymgr['right']:
            self.campos.phi += 1
        if self.keymgr['pgup']:
            self.campos.rho += 0.25
        if self.keymgr['pgdn']:
            self.campos.rho -= 0.25

        while (len(self.keymgr.impulses) > 0):
            k = self.keymgr.impulses.pop()
            if k == 'a':
                self.auto = not self.auto

        self.camera.setPos(self.campos.x, self.campos.y, self.campos.z)
        self.dlnp.setPos(self.campos.x, self.campos.y, self.campos.z)
        #self.camera.setHpr(angleDegrees, 0, 0)
        self.camera.lookAt(0,0,0)
        self.dlnp.lookAt(0,0,0)
        return Task.cont

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "specify a shape. -l for list."
        sys.exit(-1)

    if sys.argv[1] == '-l':
        for sh in shapes.keys():
            print sh
        sys.exit(0)

    shp = sys.argv[1]
    if not shapes.has_key(shp):
        print "cannot find shape, -l for list"
        sys.exit(-1)



    um = meta_generic(shapes[shp])
    um.polygonize()
    format=GeomVertexFormat.getV3n3()
    vdata=GeomVertexData("vertices", format, Geom.UHStatic)
    vertexWriter=GeomVertexWriter(vdata, "vertex")
    normalWriter=GeomVertexWriter(vdata, "normal")
    print len(um.tri_list), "vertices"
    print len(um.tri_list) / 3.0, "tris"

    for p in um.tri_list:
        vertexWriter.addData3f(p[0],p[1],p[2])
    for p in um.normal_list:
        normalWriter.addData3f(p[0],p[1],p[2])

    for p in reversed(um.tri_list):
        vertexWriter.addData3f(p[0],p[1],p[2])
    for p in reversed(um.normal_list):
        normalWriter.addData3f(-1 * p[0], -1 * p[1], -1 *p[2])

    tris = GeomTriangles(Geom.UHStatic)
    tris.addConsecutiveVertices(0, len(um.tri_list))
    tris.closePrimitive()

    um_geom = Geom(vdata)
    um_geom.addPrimitive(tris)

    um_GN = GeomNode(shp)
    um_GN.addGeom(um_geom)

    app = MyApp()
    app.run()
