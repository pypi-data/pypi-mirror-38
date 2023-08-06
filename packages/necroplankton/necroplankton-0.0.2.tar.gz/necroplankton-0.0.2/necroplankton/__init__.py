import sys, os

__p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __p not in sys.path:
    sys.path.insert(0, __p)

from .lib import  fetch as __fetch
from .lib import out as __out

__author__ = 'necroplankton'


fetch = __fetch.Fetch()
output = __out.Put()

if __name__ == '__main__':
    #fetch.img('https://cloud.rainy.me/beach.jpg')
    output.json({})