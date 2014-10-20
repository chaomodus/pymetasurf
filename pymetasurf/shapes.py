# Various interesting shapes!
# Written by Cas Rusnov <rusnovn@gmail.com>

"""These are simple metasurface states and equations for producing interesting shapes with metasurface."""

from math import pi, sin, cos, tan, sqrt, exp, radians
import pymetasurf
sqr = lambda x: x**2

shapes = {
    'pineapple':(pymetasurf.MSURF_LESSER, (-8,-8,-8,8,8,8), (60,60,60), lambda x, y, z: -(cos(x) * sin(y) + cos(y) * sin(z) + cos(z) * sin(x))*(cos(x) * sin(y) + cos(y) * sin(z) + cos(z) * sin(x))+0.05-exp(100.0*(x*x/64+y*y/64 + z*z/(1.6*64)*exp(-0.4*z/8) - 1))),
    'splitsphere':(pymetasurf.MSURF_LESSER, (-2,-2,-2,2,2,2), (60,60,60), lambda x, y, z: (y**2+z**2-1)**2 +(x**2+y**2-1)**3),
    'pillow':(pymetasurf.MSURF_LESSER, (-2,-2,-2,2,2,2), (60,60,60), lambda x, y, z: x**4 * y**2 + y**4 * x**2 - x**2 * y**2 + z**6),
    'heart':(pymetasurf.MSURF_LESSER, (-2,-2,-2,2,2,2), (60,60,60), lambda x, y, z: ((-1 * (x**2)*(z**3)-(9/80)*(y**2)*(z**3))+((x**2)+(9/4)*(y**2)+(z**2)-1)**3)),
    'cone':(pymetasurf.MSURF_LESSER, (-2,-2,-2,2,2,2), (60,60,60), lambda x, y, z: sqrt(sqr(x) + sqr(z)) - abs(y)),
    'pipes':(pymetasurf.MSURF_LESSER, (-4,-4,-4,4,4,4), (60,60,60), lambda x, y, z: -(cos(x) + cos(y) + cos(z))),
    'organic1':(pymetasurf.MSURF_LESSER, (-2.5,-2.5,-2.5,2.5,2.5,2.5), (60,60,60), lambda x, y, z: cos(4.0*x/(x*x+y*y+z*z+0.0001))*sin(4.0*y/(x*x+y*y+z*z+0.0001))+ cos(4.0*y/(x*x+y*y+z*z+0.0001))*sin(4.0*z/(x*x+y*y+z*z+0.0001))+ cos(4.0*z/(x*x+y*y+z*z+0.0001))*sin(4.0*x/(x*x+y*y+z*z+0.0001))+ exp(0.1*(x*x+y*y+z*z-0.2)) - exp(-10.0*(x*x+y*y+z*z-0.15))),
    'organic2':(pymetasurf.MSURF_LESSER, (-1.5,-1.5,-1.5,1.5,1.5,1.5), (100,100,100), lambda x, y, z: cos(4.0*x/(x*x+y*y+z*z+0.0001))*sin(4.0*y/(x*x+y*y+z*z+0.0001))+ cos(4.0*y/(x*x+y*y+z*z+0.0001))*sin(4.0*z/(x*x+y*y+z*z+0.0001))+ cos(4.0*z/(x*x+y*y+z*z+0.0001))*sin(4.0*x/(x*x+y*y+z*z+0.0001))+ exp(1*(x*x+y*y+z*z-0.2))),
    'organic3':(pymetasurf.MSURF_LESSER, (-1.5,-1.5,-1.5,1.5,1.5,1.5), (100,100,100), lambda x, y, z: cos(4.0*x/(x*x+y*y+z*z+0.0001))*sin(4.0*y/(x*x+y*y+z*z+0.0001))+ cos(4.0*y/(x*x+y*y+z*z+0.0001))*sin(4.0*z/(x*x+y*y+z*z+0.0001))+ cos(4.0*z/(x*x+y*y+z*z+0.0001))*cos(4.0*x/(x*x+y*y+z*z+0.0001))+ exp(10*(x*x+y*y+z*z-0.2))),
    'magnetic':(pymetasurf.MSURF_LESSER, (-0.5,-0.5,-0.5,0.5,0.5,0.5), (100,100,100), lambda x, y, z: sin(7.0*x/(x*x+y*y+z*z+0.0001))*sin(7.0*y/(x*x+y*y+z*z+0.0001))*cos(4.0*x/(x*x+y*y+z*z+0.0001))+ exp(10*(x*x+y*y+z*z-0.2))),
    'ripple':(pymetasurf.MSURF_LESSER, (-10,-10,-3,10,10,3), (60,60,60), lambda x, y, z: z - (sin(2*sqrt(x*x + y*y)) - cos(2.5*sqrt(x*x + y*y)))),
    'jack':(pymetasurf.MSURF_LESSER, (-5,-5,-5,5,5,5), (60,60,60), lambda x, y, z: sqrt(z*z + y*y + x*x) - (cos(x * pi) + cos(y * pi) + cos(z * pi))),
    'cubething':(pymetasurf.MSURF_LESSER, (-5,-5,-5,5,5,5), (60,60,60), lambda x, y, z: sqrt(z*z + y*y + x*x) - (sin(x * x * pi) + sin(y * y * pi) + sin(z * z * pi)) + 1.2*(cos(x * x * pi) + cos(y * y * pi) + cos(z * z * pi))),
    'fronds':(pymetasurf.MSURF_LESSER, (-8,-8,-8,8,8,8), (150,150,150), lambda x, y, z: sqrt(z*z + x*x + y*y) - (abs(exp(cos(x * y) - sin(y * z) - sin(x*z) - cos(y*x)))))
}
