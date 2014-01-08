"""
Run the socket server on given port.
"""

import sys
from coils import MapSockServer
server = MapSockServer('localhost', int(sys.argv[1]), encode=False)
server.run()
