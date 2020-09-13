from asyncio import sleep
from datetime import datetime, timedelta
from random import choice, randint, uniform
from typing import TYPE_CHECKING
from ssh_trickster_server.attempts import attempts
if TYPE_CHECKING:
    from asyncssh.process import SSHServerProcess


DEFAULT_HOSTNAME = choice(('db', 'server', 'support', 'test', 'web', 'www',))
random_time_offset = randint(1, 13 * 24 * 60 * 60)
DEFAULT_TIMESTAMP = (datetime.today() - timedelta(seconds=random_time_offset))
DEFAULT_PEERNAME = '.'.join(str(randint(1, 255)) for i in range(4))


async def handle_client(process: 'SSHServerProcess'):
    username = process.get_extra_info('username')
    last_attempt = attempts.get_by_username(username)
    if not last_attempt.timestamp or not last_attempt.peername:
        last_attempt = attempts.update(
            username,
            timestamp=DEFAULT_TIMESTAMP,
            peername=DEFAULT_PEERNAME,
        )
    await sleep(uniform(0, 59))
    timestamp_str = last_attempt.timestamp.strftime('%a %b %d %H:%M:%S %Y')
    process.stdout.write(f'Last login: {timestamp_str}'
                         f'from {last_attempt.peername}\n')
    current_attempt = attempts.update(
        username,
        timestamp=datetime.now(),
        peername=process.get_extra_info('peername')[0],
    )
    await sleep(uniform(0, 59))
    process.stdout.write(f'[{current_attempt.username}@{DEFAULT_HOSTNAME}]$ ')
    await sleep(13 * 60)
    process.exit(0)
