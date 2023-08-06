import docker
from docker.models.containers import Container
from .languages import LANGUAGES
from threading import Thread

client = docker.from_env()

_language_lookup = LANGUAGES

def get_image_command(language, version):
    language_config = _language_lookup.get(language)
    if language_config:
        versions = language_config['versions']
        default = versions.get('default')
        image = default['image']
        tag = default['tag']
        command = default['command']
        return f"{image}:{tag}", command


class Runner:
    def __init__(self, language, version='default', *, block=True):
        self.image, self.command = get_image_command(language.lower(), version.lower())
        self.container = None  # type: Container
        if block:
            self._run_container()
        else:
            create_thread = Thread(target=self._run_container)
            create_thread.start()

    def _run_container(self):
        self.container = client.containers.run(self.image, command="sleep 3600", detach=True)

    @property
    def ready(self):
        return self.container is not None

    def __del__(self):
        if self.container and self.container.status == 'running':
            self.container.kill()

    def get_output(self, code, decode=True):
        exit_code, result = self.container.exec_run(
            self.command.format(
                code.replace('"', r'\"')
            )
        )
        if decode:
            return result.decode()
        else:
            return result


# for language_name in LANGUAGES:
#     _language_lookup[language_name] = LANGUAGES[language_name]
#     aliases = language_name.get('aliases')
#     if aliases:
#         for alias in aliases:
#             _language_lookup[alias] = LANGUAGES[language_name]

