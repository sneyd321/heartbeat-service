from flask import Flask
from celery import Celery
from server.api.models import FileParser
from kazoo.client import KazooClient, KazooState

zk = KazooClient()
app = Flask(__name__)
fp = FileParser("./hosts_dev.txt")





def make_celery(app, env):
    if env == "prod":
        zk.set_hosts('zookeeper.default.svc.cluster.local:2181')
        app.config['CELERY_BROKER_URL'] = 'redis://redis-service.default.svc.cluster.local:6379/2'

    elif env == "dev":
        zk.set_hosts('host.docker.internal:2181')
        app.config['CELERY_BROKER_URL'] = 'redis://host.docker.internal:6379/2'

    else:
        return None

    zk.start()


    celery = Celery(
        app.import_name,
        #backend=app.config['RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'], 
        include=['server.api.tasks']
    )
    celery.conf.update(app.config)
    celery.control.purge()

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

celery = make_celery(app, "prod")

