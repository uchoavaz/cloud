
from celery.decorators import task
from vm_lib import VM


@task()
def teste(name, ip, droplet):
        vm = VM()
        vm.vm_name(name)
        vm.vm_ip(ip)
        vm.vm_path_image('linux.box')
        vm.vm_memory(droplet.memory)
        vm.vm_cpu(droplet.processor)
        vm.create()
