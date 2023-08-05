"""This is the external interface to the Rook package."""
import sys
import os
import traceback

import six


class Rook(object):
    """This class represents a control object for the module."""

    def __init__(self):
        """Initialize a new Rook controller."""
        self._rook = None
        self._debug = False
        self._silence_errors = True

    def start(self,
              token=None,
              host=None,
              port=None,
              debug=None,
              silence_errors=None,
              log_file=None,
              log_level=None,
              log_to_stderr=None,
              **kwargs):
        """Start the rook module.

        Arguments:
        host - The address to the Rookout Agent. Only "localhost" is recommended.
        port - The port the Rookout Agent is listening on.
        """
        if self._rook is not None:
            return

        if isinstance(debug, bool):
            self._debug = debug
        elif os.environ.get('ROOKOUT_DEBUG') == '1':
            self._debug = True

        if isinstance(silence_errors, bool):
            self._silence_errors = silence_errors

        if not isinstance(log_to_stderr, bool) and os.environ.get('ROOKOUT_LOG_TO_STDERR') == '1':
            log_to_stderr = True

        log_file = log_file or os.environ.get('ROOKOUT_LOG_FILE')
        log_level = log_level or os.environ.get('ROOKOUT_LOG_LEVEL')
        host = host or os.environ.get('ROOKOUT_AGENT_HOST')
        port = port or os.environ.get('ROOKOUT_AGENT_PORT')
        token = token or os.environ.get('ROOKOUT_TOKEN')

        try:
            from rook.exceptions.tool_exceptions import RookMissingToken, RookInvalidToken, RookVersionNotSupported, \
                RookCommunicationException
            try:
                from rook.config import LoggingConfiguration

                if log_file is not None:
                    LoggingConfiguration.FILE_NAME = log_file

                if log_level is not None:
                    LoggingConfiguration.LOG_LEVEL = log_level

                if log_to_stderr is not None:
                    LoggingConfiguration.LOG_TO_STDERR = log_to_stderr

                if self._debug:
                    LoggingConfiguration.LOG_LEVEL = 'DEBUG'
                    LoggingConfiguration.LOG_TO_STDERR = True

                if not host and not token:
                    raise RookMissingToken()

                import rook.singleton
                self._rook = rook.singleton.singleton_obj

                return self._rook.connect(token, host, port)
            except (RookMissingToken, RookInvalidToken, RookVersionNotSupported) as e:
                six.print_("[Rookout] Failed to connect to the agent:", e, file=sys.stderr)
                raise
            except RookCommunicationException:
                six.print_("[Rookout] Failed to connect to the agent - will continue attempting in the background", file=sys.stderr)
                raise
            except ImportError as e:
                six.print_("[Rookout] Failed to import dependencies:", e, file=sys.stderr)
                raise
            except Exception as e:
                six.print_("[Rookout] Failed initialization:", e, file=sys.stderr)
                raise
        except Exception:
            if not self._silence_errors:
                raise

            if self._debug:
                traceback.print_exc()

    def flush(self):
        self._rook.flush()

    def set_version_information(self, **kwargs):
        """Set the application's version information.

        If the agent connection has already been established, updated version information will be sent immediately.
        If the agent connection has not yet been established, the version information will be sent on connection.
        """
        self._rook.set_version_information(**kwargs)
