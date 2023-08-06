from importlib import import_module
from redis import StrictRedis
from . import settings, setup_logging
from .files import DownloadedFile, FileEncoder
import json
import logging
import requests
import rq


def get_queue():
    connection = StrictRedis.from_url(settings.REDIS_URL)
    return rq.Queue(settings.RQ_QUEUE, connection=connection)


class Entity(object):
    def __init__(self, data):
        self.id = data['id']
        self.__kind = data['type']

        for key, value in data['attributes'].items():
            setattr(self, key, value)

    def __repr__(self):
        return '<%sEntity %s>' % (
            self.__kind.replace('-', ' ').title().replace(' ', ''),
            self.id
        )


class Workflow(object):
    def __init__(self, workflow, operations, objects):
        self.id = workflow['id']
        self.url = workflow['links']['self']
        self.key = workflow['attributes']['key']
        self.context = {}
        self.cleanup = []

        logger.debug('New workflow: %(id)s' % workflow)

        for obj in objects:
            if obj['type'] == 'workflows':
                if obj['id'] == workflow['attributes']['parent']:
                    self.context.update(
                        obj['attributes'].get('result', {})
                    )

        args = workflow['attributes'].get('args', {})
        self.context.update(args)

        if 'object' in self.context:
            for obj in objects:
                if obj['type'] == args['object']['type']:
                    if obj['id'] == args['object']['id']:
                        self.context['object'] = Entity(obj)
                        break

        if 'media' in self.context:
            self.context['media'] = DownloadedFile(
                self.context['media']
            )

        self.__original_context = sorted(set(self.context.keys()))
        self.operations = [
            Operation(self, operation)
            for operation in operations
        ]

    def log(self, message, exc_info=False):
        if exc_info:
            logger.error(message, exc_info=True)
        else:
            logger.debug(message)

    def enqueue(self):
        logger.debug('Enqueuing')
        queue = get_queue()
        queue.enqueue(self.work)

    def _cleanup(self):
        while len(self.cleanup):
            self.cleanup.pop()()

    def work(self):
        for operation in self.operations:
            if operation.run() is False:
                self._cleanup()
                return

        data = json.dumps(
            {
                'data': {
                    'type': 'workflows',
                    'id': self.id,
                    'attributes': {
                        'result': dict(
                            [
                                (key, value)
                                for (key, value) in self.context.items()
                                if key != 'object'
                            ]
                        )
                    }
                }
            },
            cls=FileEncoder(self),
            indent=4
        )

        try:
            response = requests.patch(
                self.url,
                data=data,
                headers={
                    'Authorization': 'Bearer %s' % settings.API_KEY,
                    'Content-Type': 'application/vnd.api+json'
                },
                timeout=5
            )

            response.raise_for_status()
        except Exception:
            raise
            self.log(
                'Error communicating with Podiant API',
                exc_info=True
            )
        else:
            self.log('PATCH %s %d' % (self.url, response.status_code))
        finally:
            self._cleanup()

    def new_result(self, result):
        nr = {}

        for key, value in result.items():
            if key in self.__original_context:
                continue

            nr[key] = value

        return nr


class Operation(object):
    def __init__(self, workflow, data):
        self.workflow = workflow
        self.id = data['id']
        self.name = data['attributes']['name']

        namespace, func = self.name.rsplit('.', 1)

        try:
            module = import_module(namespace)
        except ImportError:
            raise Exception('Not equipped to run this operation.')

        try:
            self.func = getattr(module, func)
        except AttributeError:
            raise Exception('Operation does not exist.')

        self.can_fail = data['attributes']['can-fail']
        self.url = data['links']['self']

        self.verbose_name = getattr(
            self.func,
            '_process_name',
            func.replace('_', ' ').capitalize()
        )

        self.description = getattr(
            self.func,
            '_process_description',
            ''
        )

        self.takes_context = getattr(self.func, '_takes_context', False)
        self.progress = 0
        self.status = 'scheduled'

    def update(self, status='running', progress=None, message=None, **result):
        attributes = {
            'status': status
        }

        nc = self.workflow.new_result(result)
        advanced = False

        if any(nc.keys()):
            attributes['result'] = nc

        if progress is not None:
            p = float(progress)

            if p > self.progress:
                if p < 100 and status == 'running':
                    remainder = int(round(p, 0)) % 10
                    if remainder == 0:
                        attributes['progress'] = p
                        advanced = True

                self.progress = progress

            if status == 'running' and self.status == 'running':
                if not advanced:
                    return

        self.status = status
        data = json.dumps(
            {
                'data': {
                    'type': 'operations',
                    'id': self.id,
                    'attributes': attributes
                },
                'meta': {
                    'verbose-name': message or self.verbose_name,
                    'description': self.description
                }
            },
            cls=FileEncoder(self.workflow),
            indent=4
        )

        try:
            response = requests.patch(
                self.url,
                data=data,
                headers={
                    'Authorization': 'Bearer %s' % settings.API_KEY,
                    'Content-Type': 'application/vnd.api+json'
                },
                timeout=5
            )

            response.raise_for_status()
        except Exception:
            raise
            self.workflow.log(
                'Error communicating with Podiant API',
                exc_info=True
            )

            return

        self.workflow.log(
            'PATCH %s (%d)' % (self.url, response.status_code)
        )

    def run(self):
        self.workflow.log(
            'Running operation %s ("%s")' % (
                self.id,
                self.name
            )
        )

        self.update()
        args = []

        if self.takes_context:
            args.append(self)

        try:
            result = self.func(*args, **self.workflow.context)
        except Exception as ex:
            logger.error('Error running operation', exc_info=True)
            self.update('failed', message=str(ex))
            return self.can_fail
        else:
            if isinstance(result, dict):
                self.workflow.context.update(result)
                self.update('successful', **result)
            elif result is not None and result is not False:
                raise Exception('Invalid response')
            else:
                self.update('successful')

            return True


setup_logging()
logger = logging.getLogger('podiant.workflows')
