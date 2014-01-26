"""
Run the socket dictionary server on given port.

Usage:

   python mapper.py <host> <port>

"""

import sys
import coils

server = coils.MapSockServer(sys.argv[1], int(sys.argv[2]), encode=False)
server.run()
