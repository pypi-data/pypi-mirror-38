import sys
import six
import os

from rook.logger import logger

hook_installed = False

if sys.platform in ('darwin', 'linux2', 'linux'):
    original_os_fork = None

    def os_fork_hook():
        try:
            six.print_("[Rookout] Rookout does not support running in forking processes. Shutting down.")

            from .singleton import singleton_obj
            singleton_obj.stop()

        except:
            pass

        return original_os_fork()

    def install_fork_handler():
        global hook_installed
        if hook_installed:
            return
        hook_installed = True

        logger.debug("Installing os.fork handler")
        global original_os_fork
        original_os_fork = os.fork
        os.fork = os_fork_hook

else:
    def install_fork_handler():
        pass
