
# -*- coding: utf-8 -*-
from celery.decorators import task
from vm_lib import VMCreation
from vm_lib import VMDeletion
from vm_lib import VMEdition
from .models import AvailableIps
from .models import UserDroplet
from core.mail import send_mail


@task()
def create_vm(name, ip, droplet, image, initial_password, username, email):
    path = '/images/{0}'.format(image.name_path)
    vm = VMCreation()
    vm.vm_name(name)
    vm.vm_ip(ip)
    vm.vm_path_image(path)
    vm.vm_memory(droplet.memory)
    vm.vm_cpu(droplet.processor)
    vm.vm_disk(droplet.disk * 1024)
    vm.vm_password(initial_password)
    vm.create()
    UserDroplet.objects.filter(ip=ip).update(
        status=2, can_remove=True, initial_password=initial_password)
    mailer.delay(
        '',
        name,
        initial_password,
        username, email)


@task()
def remove_vm(vm_name):
    vm = VMDeletion()
    vm.vm_name(vm_name)
    vm.remove()
    AvailableIps.objects.filter(ip=vm_name).update(is_available=True)


@task()
def edit_vm(ip, cpu, memory, name, disk):

    vm = VMEdition()
    vm.vm_name(name)
    vm.vm_ip(ip)
    vm.vm_memory(memory)
    vm.vm_cpu(cpu)
    vm.vm_disk(disk * 1024)
    vm.edit()
    UserDroplet.objects.filter(ip=ip).update(
        can_remove=True, status=2)


@task
def new_password_vm(name, ip, cpu, memory, new_password, username, email):
    vm = VMEdition()
    vm.vm_name(name)
    vm.vm_ip(ip)
    vm.vm_memory(memory)
    vm.vm_cpu(cpu)
    vm.reset_password(new_password)

    UserDroplet.objects.filter(ip=ip).update(
        can_remove=True, status=2, initial_password=new_password)

    mailer.delay(
        u'Redefinição de senha para a',
        name,
        new_password,
        username, email)


@task
def mailer(title, machine, password, username, user_email):
    send_mail(title, machine, password, username, user_email)
