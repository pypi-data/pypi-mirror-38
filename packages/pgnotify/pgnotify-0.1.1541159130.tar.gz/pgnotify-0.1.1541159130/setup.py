# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pgnotify']

package_data = \
{'': ['*']}

install_requires = \
['logx', 'psycopg2-binary']

setup_kwargs = {
    'name': 'pgnotify',
    'version': '0.1.1541159130',
    'description': 'Easily LISTEN to PostgreSQL NOTIFY notifications',
    'long_description': '# pgnotify: Easily LISTEN to PostgreSQL NOTIFY notifications\n\nLISTEN to and process NOTIFY events with a simple `for` loop, like so:\n\n    from pgnotify import await_pg_notifications\n\n    for notification in await_pg_notifications(\n            \'postgresql:///nameofdatabase\',\n            [\'channel1\', \'channel2\']):\n\n        print(notification.channel)\n        print(notification.payload)\n\nYou can also handle timeouts and signals, as in this more fully-fleshed example:\n\n    import signal\n\n    from pgnotify import await_pg_notifications, get_dbapi_connection\n\n    CONNECT = "postgresql:///example"\n    e = get_dbapi_connection(CONNECT)\n\n    SIGNALS_TO_HANDLE = [signal.SIGINT, signal.SIGTERM]\n\n      for n in await_pg_notifications(\n          e,\n          ["hello", "hello2"],\n          timeout=10,\n          yield_on_timeout=True,\n          handle_signals=SIGNALS_TO_HANDLE,\n      ):\n          # when n is an integer, a signal has been has been caught for further handling.\n          if isinstance(n, int):\n              sig = signal.Signals(n)\n              if n in SIGNALS_TO_HANDLE:\n                  print(f"handling {sig.name}")\n              print("interrupted, stopping")\n              break\n\n          # if `yield_on_timeout` has been set to True, the loop returns None after the timeout has been reached\n          elif n is None:\n              print("timeout, continuing")\n\n          # handle the actual notify occurrences here\n          else:\n              print((n.pid, n.channel, n.payload))\n\nFurther documentation to come.\n',
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'url': 'https://github.com/djrobstep/pgnotify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
