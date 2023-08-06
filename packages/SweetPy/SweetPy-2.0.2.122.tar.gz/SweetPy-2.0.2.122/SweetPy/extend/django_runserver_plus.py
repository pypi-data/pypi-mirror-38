import sys
import os
from datetime import datetime
import errno
from django.core.servers.basehttp import (
    WSGIServer, get_internal_wsgi_application, run,
)
from django.utils import autoreload, six
from django.utils.encoding import force_text, get_system_encoding
from django.conf import settings
import socket

class Foo:
    online = None
    sweet_settings = None

def inner_run(self, *args, **options):
    # If an exception was silenced in ManagementUtility.execute in order
    # to be raised in the child process, raise it now.
    autoreload.raise_last_exception()

    threading = options['use_threading']
    # 'shutdown_message' is a stealth option.
    shutdown_message = options.get('shutdown_message', '')
    quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

    self.stdout.write("Performing system checks...\n\n")
    self.check(display_num_errors=True)
    # Need to check migrations here, so can't use the
    # requires_migrations_check attribute.
    self.check_migrations()
    now = datetime.now().strftime('%B %d, %Y - %X')
    if six.PY2:
        now = now.decode(get_system_encoding())
    self.stdout.write(now)
    self.stdout.write((
                          "Django version %(version)s, using settings %(settings)r\n"
                          "Starting development server at %(protocol)s://%(addr)s:%(port)s/\n"
                          "Quit the server with %(quit_command)s.\n"
                      ) % {
                          "version": self.get_version(),
                          "settings": settings.SETTINGS_MODULE,
                          "protocol": self.protocol,
                          "addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
                          "port": self.port,
                          "quit_command": quit_command,
                      })

    try:
        handler = self.get_handler(*args, **options)
        if Foo.sweet_settings:
            print('========app zk register======')
        if Foo.online:
            Foo.online(Foo.sweet_settings)
        run(self.addr, int(self.port), handler,
            ipv6=self.use_ipv6, threading=threading, server_cls=self.server_cls)
    except socket.error as e:
        # Use helpful error messages instead of ugly tracebacks.
        ERRORS = {
            errno.EACCES: "You don't have permission to access that port.",
            errno.EADDRINUSE: "That port is already in use.",
            errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
        }
        try:
            error_text = ERRORS[e.errno]
        except KeyError:
            error_text = force_text(e)
        self.stderr.write("Error: %s" % error_text)
        # Need to use an OS exit because sys.exit doesn't work in a thread
        os._exit(1)
    except KeyboardInterrupt:
        if shutdown_message:
            self.stdout.write(shutdown_message)
        sys.exit(0)

from django.core.management.commands.runserver import Command
Command.inner_run = inner_run