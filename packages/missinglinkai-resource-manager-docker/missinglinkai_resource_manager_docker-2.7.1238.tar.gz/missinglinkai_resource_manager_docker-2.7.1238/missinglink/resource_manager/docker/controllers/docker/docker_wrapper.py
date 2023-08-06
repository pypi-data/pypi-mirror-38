import logging
import os

import docker

from missinglink.resource_manager.docker.config import docker_client
from missinglink.resource_manager.docker.pip import get_version

logger = logging.getLogger(__name__)


class DockerWrapper:
    @classmethod
    def get(cls):
        return cls()

    def __init__(self):
        self.docker_client = docker_client()

    @classmethod
    def _safe_get(cls, method, args=None, kwargs=None, default=None):
        args = args or []
        kwargs = kwargs or {}
        try:
            return method(*args, **kwargs)
        except docker.errors.NotFound:
            return default

    @classmethod
    def get(cls):
        return cls()

    def container(self, container_id):
        return self._safe_get(self.docker_client.containers.get, [container_id])

    def volume(self, volume_id):
        return self._safe_get(self.docker_client.volumes.get, [volume_id])

    def image(self, image_id):
        return self._safe_get(self.docker_client.images.get, [image_id])

    def create_volume(self, name, **kwargs):
        labels = kwargs.pop('labels', {})

        for k, v in labels.items():
            if not isinstance(v, str):
                labels[k] = str(v)
        kwargs['labels'] = labels
        return self.docker_client.volumes.create(name, **kwargs)

    def create_container(self, **kwargs):
        return self.docker_client.containers.create(**kwargs)

    def raw_status(self):
        return self.docker_client.info()

    def be_summary(self):

        raw = self.raw_status()
        key_mapping = {
            "cpu.memory": "MemTotal",
            "cpu.count": "NCPU",
            "cpu.max.memory": "MemTotal",
            "cpu.max.count": "NCPU",
            "server.arch": "Architecture",
            "server.kernel": "KernelVersion",
            "server.os": "OperatingSystem",
            "server.name": 'Name',
            "server.type": 'OSType',

        }
        res = {}

        def set_key_in_path(key_, val_):
            # res[key] = val
            # TODO: fix deep dics FB error
            prc = res
            key_arr = key_.split('.')
            for lvl in key_arr[:-1]:  # the last one is the key
                if lvl not in prc:
                    prc[lvl] = {}
                prc = prc[lvl]
            prc[key_arr[-1]] = val_

        for key in key_mapping:
            src = key_mapping[key]
            val = raw.get(src)
            set_key_in_path(key, val)
        res["server"]['rm'] = {
            'ML_RM_VERSION': get_version(),
            'ML_PIP_INDEX': os.environ.get('ML_PIP_INDEX'),
            'ML_PIP_VERSION': os.environ.get('ML_PIP_VERSION')
        }
        return res

    def has_nvidia(self):
        try:
            import docker
            logger.info('Validating GPU...')
            self.docker_client.images.pull('nvidia/cuda:9.0-base')
            logger.debug('Validating GPU... Run')
            self.docker_client.containers.run('nvidia/cuda:9.0-base', 'env', runtime='nvidia', remove=True)  # also try auto_remove
            logger.info('Validating GPU... True')
            return True
        except Exception as ex:
            logger.debug('GPU not found, ignore the error if you do not have GPU installed on this machine', exc_info=1)
            logger.info('GPU not found, ignore the error if you do not have GPU installed on this machine: %s', str(ex))
            return False

    @classmethod
    def _image_downgrade_supported(cls, image):
        return True

    @classmethod
    def _remove_gpu_tag(cls, image):
        if ':' not in image:
            return image

        image_parts = image.split(':')
        tag = image_parts[-1]
        if 'gpu' not in tag:
            return image

        tag = tag.replace('gpu', '').replace('--', '-')
        if tag.endswith('-'):
            tag = tag[:-1]
        if tag.startswith('-'):
            tag = tag[1:]
        image_parts[-1] = tag
        return ':'.join(image_parts)

    @classmethod
    def downgrade_gpu_image_if_needed(cls, original_image, has_gpu):
        if has_gpu:
            return original_image

        if cls._image_downgrade_supported(original_image):
            image = cls._remove_gpu_tag(original_image)
            if image != original_image:
                logger.warning('image %s changed to %s due to lack of GPU on the host machine' % (original_image, image))
            else:
                logger.info('will use image %s on cpu server', original_image)
            return image
