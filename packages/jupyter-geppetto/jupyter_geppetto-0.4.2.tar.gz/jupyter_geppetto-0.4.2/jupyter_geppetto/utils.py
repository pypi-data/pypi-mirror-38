import logging
# from jupyter_client import session
from zmq.utils import jsonapi
from ipykernel.jsonutil import json_clean

def convertToJS(content):
    # return session.json_packer(content).decode("utf-8")
    # Old way: this needs to be deleted if the above line is enough
    return jsonapi.dumps(json_clean(content)).decode("utf-8")

def convertToPython(content):
    # return session.json_unpacker(content)
    # Old way: this needs to be deleted if the above line is enough
    return jsonapi.loads(content)

def exception_to_string(exc_info):
    import IPython.core.ultratb
    tb = IPython.core.ultratb.VerboseTB()
    return tb.text(*exc_info)

def getJSONError(message, exc_info):
    data = {}
    data['type'] = 'ERROR'
    data['message'] = message

    if isinstance(exc_info, str):
        details = exc_info
    else:
        details = exception_to_string(exc_info)
    data['details'] = details
    return data

def getJSONReply():
    data = {}
    data['type'] = 'OK'
    return data

def configure_logging():
    try:
        # Configure log
        logger = logging.getLogger()
        fhandler = logging.FileHandler(filename='netpyne-ui.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        logger.setLevel(logging.DEBUG)
        logging.debug('Log configured')
    except Exception as exception:
        logging.exception("Unexpected error while initializing Geppetto from Python:")
        logging.error(exception)