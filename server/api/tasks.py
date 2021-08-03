from server import  zk, fp, celery
import base64, requests
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def send_health_check(service):
    global zk
    zk.ensure_path("/RoomR/Services")
    try:
        logger.info("Sending to http://" + service + "/Health")
        beat = fp.getHostFromFile(service)
        response = requests.get("http://" + service + "/Health")
        if response.ok:
            if beat:
                if not zk.exists("/RoomR/Services/" + beat._name):
                    zk.create("/RoomR/Services/" + beat._name, ephemeral=True, value=beat._address.encode('utf-8'))
                    logger.info(beat._name + " node created")
            logger.info(beat._name + " node already exists")
        else:
            if zk.exists("/RoomR/Services/" + beat._name):
                zk.delete("/RoomR/Services/" + beat._name)
                logger.info(beat._name + " node deleted")
            logger.info(beat._name + " node not deleted")
    except requests.exceptions.ConnectionError:
        if zk.exists("/RoomR/Services/" + beat._name):
            zk.delete("/RoomR/Services/" + beat._name)
            logger.info(beat._name + " ERROR")
        logger.info(beat._name + " node does not exist")



        
@celery.task
def error_handler(request, exc, traceback):
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(request.id, exc, traceback))
        