from os import path, walk, makedirs
from jinja2 import Template


EMPTY = ''
CURRENT_DIR = '.'
READ_FLAG = 'r'
WRITE_FLAG = 'w+'
SERVICE_KEY = 'service'
SERVICE_REPLACE = '{{service}}'
TEMPLATE_DIR = 'templates'
IGNORED_FILES = ['.DS_Store']


def _replace_template_file(template_file, destination, **kwargs):
    service_name = kwargs.get(SERVICE_KEY, EMPTY)
    final_destination = destination.replace(SERVICE_REPLACE, service_name)[:-3]
    if not any(substring in template_file for substring in IGNORED_FILES):
        template_content = open(template_file, READ_FLAG).read()
        template = Template(template_content)
        with open(final_destination, WRITE_FLAG) as file:
            file.write(template.render(kwargs))


def _process_template_files(service_name, priority, destination_dir=CURRENT_DIR):
    destination = path.join(destination_dir, service_name)
    makedirs(destination, exist_ok=True)
    current_dir = path.dirname(path.realpath(__file__))
    template_dir = path.join(current_dir, TEMPLATE_DIR)
    for directory, _, file_list in walk(template_dir):
        for file in file_list:
            new_path = destination + path.join(directory, file).split(TEMPLATE_DIR)[1]
            makedirs(path.dirname(new_path), exist_ok=True)
            _replace_template_file(path.join(directory, file), new_path, service=service_name, priority=priority)


def scaffold_up_service(service_name, priority):
    _process_template_files(service_name, priority)
