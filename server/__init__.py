from flask import Flask

from celery import Celery
from server.api.models import FileParser

from kazoo.client import KazooClient, KazooState

zk = KazooClient(hosts='host.docker.internal:2181')
zk.start()

app = Flask(__name__)


#c = Celery("server", broker='redis://redis-service.default.svc.cluster.local:6379', backend='redis://redis-service.default.svc.cluster.local:6379')
#app.config['CELERY_BROKER_URL'] = 'redis://redis-service.default.svc.cluster.local:6379/2'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://redis-service.default.svc.cluster.local:6379/2'

app.config['CELERY_BROKER_URL'] = 'redis://host.docker.internal:6379/2'
#app.config['RESULT_BACKEND'] = 'redis://host.docker.internal:6379/2'

fp = FileParser("./hosts.txt")
print(fp.getBeatSchedule(), flush=True)
print(fp.getHostFromFile("host.docker.internal:8090"), flush=True)

def make_celery(app):
    celery = Celery(
        app.import_name,
        #backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'], 
        include=['server.api.tasks']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    celery.control.purge()
    
    celery.conf.beat_schedule = fp.getBeatSchedule()
    celery.conf.timezone = 'UTC'
    return celery


def create_app():
    #Intialize modules
    from server.api.routes import registrar
    app.register_blueprint(registrar, url_prefix="/registrar/v1")
    return app


celery = make_celery(app)



celery.conf.update(app.config)