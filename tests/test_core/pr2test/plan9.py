from socket import socketpair

from pyroute2.plan9.client import Plan9ClientSocket
from pyroute2.plan9.server import Plan9ServerSocket


class AsyncPlan9Context:

    server = None
    client = None
    shutdown_response = None
    sample_data = b'Pi6raTaXuzohdu7n'

    def __init__(self):
        self.server_sock, self.client_sock = socketpair()
        self.server = Plan9ServerSocket(use_socket=self.server_sock)
        self.client = Plan9ClientSocket(use_socket=self.client_sock)
        inode = self.server.filesystem.create('test_file')
        inode.data.write(self.sample_data)

    async def ensure_session(self):
        self.task = await self.server.async_run()
        await self.client.start_session()

    async def close(self):
        self.task.cancel()
