
from celery.decorators import task
from vm_lib import VMCreation
from vm_lib import VMDeletion


@task()
def create_vm(name, ip, droplet):
        vm = VMCreation()
        vm.vm_name(name)
        vm.vm_ip(ip)
        vm.vm_path_image('linux.box')
        vm.vm_memory(droplet.memory)
        vm.vm_cpu(droplet.processor)
        vm.create()


@task()
def remove_vm(vm_name):
    vm = VMDeletion()
    vm.vm_name(vm_name)
    vm.remove()
