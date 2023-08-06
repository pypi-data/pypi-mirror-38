import logging

from python_agent.common import constants

log = logging.getLogger(__name__)


def override_xdist_exit_timeout():
    try:
        from xdist.workermanage import NodeManager
        NodeManager.EXIT_TIMEOUT = constants.XDIST_EXIT_TIMEOUT_IN_SECONDS
        log.info("Overridden xdist exit timeout to = %s" % constants.XDIST_EXIT_TIMEOUT_IN_SECONDS)
    except ImportError:
        pass
    except Exception as e:
        log.error("Failed overriding xdist exit timeout to = %s. Error=%s" % (constants.XDIST_EXIT_TIMEOUT_IN_SECONDS, str(e)))