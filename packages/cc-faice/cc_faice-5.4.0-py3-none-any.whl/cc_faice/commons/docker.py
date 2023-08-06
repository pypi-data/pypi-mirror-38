import os
import docker

from cc_core.commons.cwl import location
from cc_core.commons.files import read
from cc_core.commons.exceptions import AgentError
from cc_core.commons.engines import DEFAULT_DOCKER_RUNTIME, NVIDIA_DOCKER_RUNTIME
from cc_core.commons.gpu_info import set_nvidia_environment_variables


def docker_result_check(ccagent_data):
    if ccagent_data['state'] != 'succeeded':
        raise AgentError('ccagent did not succeed')


def dump_job(job_data, mapped_input_dir):
    job = {}

    for key, arg in job_data.items():
        val = arg
        if isinstance(arg, list):
            val = []
            for index, i in enumerate(arg):
                if isinstance(i, dict):
                    path = os.path.join(mapped_input_dir, '{}_{}'.format(key, index))
                    val.append({
                        'class': 'File',
                        'path': path
                    })
                else:
                    val.append(i)
        elif isinstance(arg, dict):
            path = os.path.join(mapped_input_dir, key)
            val = {
                'class': 'File',
                'path': path
            }

        job[key] = val

    return job


def input_volume_mappings(job_data, dumped_job_data, input_dir):
    volumes = []

    for key, val in job_data.items():
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
            for i, e in enumerate(val):
                file_path = location(key, e)

                if not os.path.isabs(file_path):
                    file_path = os.path.join(os.path.expanduser(input_dir), file_path)

                container_file_path = dumped_job_data[key][i]['path']
                volumes.append([os.path.abspath(file_path), container_file_path])

        if isinstance(val, dict):
            file_path = location(key, val)

            if not os.path.isabs(file_path):
                file_path = os.path.join(os.path.expanduser(input_dir), file_path)

            container_file_path = dumped_job_data[key]['path']
            volumes.append([os.path.abspath(file_path), container_file_path])

    return volumes


def env_vars(preserve_environment):
    if preserve_environment is None:
        return {}

    environment = {}

    for var in preserve_environment:
        if var in os.environ:
            environment[var] = os.environ[var]

    return environment


class DockerManager:
    def __init__(self):
        self._client = docker.DockerClient(
            base_url='unix://var/run/docker.sock',
            version='auto'
        )

    def pull(self, image, auth=None):
        self._client.images.pull(image, auth_config=auth)

    def run_container(self,
                      name,
                      image,
                      command,
                      ro_mappings,
                      rw_mappings,
                      work_dir,
                      leave_container,
                      ram,
                      runtime=DEFAULT_DOCKER_RUNTIME,
                      gpus=None,
                      environment=None):
        binds = {}

        if environment is None:
            environment = {}

        if gpus is None:
            gpus = []

        for host_vol, container_vol in ro_mappings:
            binds[host_vol] = {
                'bind': container_vol,
                'mode': 'ro'
            }

        for host_vol, container_vol in rw_mappings:
            binds[host_vol] = {
                'bind': container_vol,
                'mode': 'rw'
            }

        mem_limit = None

        if ram is not None:
            mem_limit = '{}m'.format(ram)

        if runtime == NVIDIA_DOCKER_RUNTIME:
            set_nvidia_environment_variables(environment, map(lambda gpu: gpu.device_id, gpus))

        c = self._client.containers.create(
            image,
            command,
            volumes=binds,
            name=name,
            user='1000:1000',
            working_dir=work_dir,
            mem_limit=mem_limit,
            memswap_limit=mem_limit,
            runtime=runtime,
            environment=environment,
        )

        c.start()
        c.wait()
        std_out = c.logs()

        if not leave_container:
            c.remove()

        return read(std_out.decode('utf-8'), 'CCAGENT_OUTPUT')
