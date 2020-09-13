import argparse
import asyncio
import asyncssh
import sys
from typing import TYPE_CHECKING
from ssh_trickster_server.server import SSHTricksterServer
from ssh_trickster_server.handler import handle_client
if TYPE_CHECKING:
    from typing import Sequence


async def start_server(port: int, keys: 'Sequence[str]'):
    await asyncssh.create_server(
        server_factory=SSHTricksterServer,
        host='',
        port=port,
        server_host_keys=keys,
        process_factory=handle_client,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=22)
    parser.add_argument('--keys', '-k', nargs='*')
    kwargs = vars(parser.parse_args())
    loop = asyncio.get_event_loop()
    try:
        server = start_server(**kwargs)
        loop.run_until_complete(server)
    except (OSError, asyncssh.Error) as exc:
        sys.exit('Error starting server: ' + str(exc))
    loop.run_forever()
