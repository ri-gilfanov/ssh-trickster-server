import asyncssh
from random import randint
from sys import stderr
from ssh_trickster_server.attempts import attempts


class SSHTricksterServer(asyncssh.SSHServer):
    def __init__(self, *args, **kwargs):
        self.first_retry = True
        super().__init__(*args, **kwargs)

    def connection_made(self, conn: 'asyncssh.SSHServerConnection'):
        print('SSH connection received from %s.' %
               conn.get_extra_info('peername')[0])

    def connection_lost(self, exc):
        if exc:
            print('SSH connection error: ' + str(exc), file=stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username):
        return True

    def password_auth_supported(self):
        return True

    def kbdint_auth_supported(self):
        return False

    def validate_password(self, username, password):
        if password:
            item = attempts.get_by_username(username)
            if item and item.password == password:
                return True
            elif randint(1, 13) == 13:
                attempts.update(username, password)
                return True
        return False
