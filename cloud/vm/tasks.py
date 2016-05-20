
from celery.decorators import task
from vm_lib import VMCreation
from vm_lib import VMDeletion
from .models import AvailableIps
from .models import UserDroplet


@task()
def create_vm(name, ip, droplet, image):
        path = '/images/{0}'.format(image.name_path)
        vm = VMCreation()
        vm.vm_name(name)
        vm.vm_ip(ip)
        vm.vm_path_image(path)
        vm.vm_memory(droplet.memory)
        vm.vm_cpu(droplet.processor)
        vm.create()
        UserDroplet.objects.filter(ip=ip).update(status=2, can_remove=True)


@task()
def remove_vm(vm_name):
    vm = VMDeletion()
    vm.vm_name(vm_name)
    vm.remove()
    AvailableIps.objects.filter(ip=vm_name).update(
        is_available=True)
