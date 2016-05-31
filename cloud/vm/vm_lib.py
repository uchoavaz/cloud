
import os
import socket

COMMANDS = {
    'configinit': 'Vagrant.configure(2) do |config|\n',
    'vmname': '  config.vm.box = "{0}"\n',
    'vmip': '  config.vm.network "public_network", bridge: "wlan0", ip: "{0}" \n',
    'configmachine': '  config.vm.provider "virtualbox" do |v|\n',
    'vname': '    v.name = "{0}"\n',
    'vmcpu': '    v.cpus = {0}\n',
    'vmmemory': '    v.memory = {0}\n',
    'endconfigmachine': '  end\n',
    'vmprovision': '  config.vm.provision "shell", inline: <<-SHELL\n',
    'vmmachinename': '  sudo hostnamectl set-hostname "{0}"\n',
    'vmpassword': (
        '  sudo passwd vagrant <<EOF\n'
        '{0}\n'
        '{0}\n'
        '  EOF\n'
        '  SHELL\n'
    ),

}


class Disk():

    def set_disk(self, disk, vm_name, atual_path):
        new_disk = 'resized-disk1.vdi'
        old_disk = 'box-disk1.vmdk'
        os.chdir(
            "/home/{0}/VirtualBox VMs/".format(socket.gethostname()))

        if os.path.isdir(self.name):
            os.chdir(os.getcwd() + "/" + vm_name)

            if not os.path.isfile(new_disk):
                os.system(
                    "VBoxManage clonehd '{0}'"
                    " '{1}' --format vdi".format(old_disk, new_disk))
                os.system(
                    "VBoxManage modifyhd"
                    " '{0}' --resize {1}".format(
                        new_disk, disk))

                os.system(
                    "VBoxManage storageattach {0} --storagectl "
                    "'SATAController' --port 0 --device 0 --type hdd "
                    "--medium {1}".format(vm_name, new_disk))

                os.system('rm -rf {0}'.format(old_disk))

            else:
                os.system(
                    "VBoxManage modifyhd"
                    " '{0}' --resize {1}".format(
                        new_disk, disk))

        os.chdir(atual_path)


class VMCreation(Disk):
    name = None
    ip = None
    image = None
    cpu = None
    memory = None
    disk = None
    password = None
    initial_path = None

    commands = {
        'configinit': COMMANDS['configinit'],
        'endconfigmachine': COMMANDS['endconfigmachine'],
        'configmachine': COMMANDS['configmachine'],
        'vmprovision': COMMANDS['vmprovision']
    }

    VARIABLES = [
        'configinit',
        'vmname',
        'vmip',
        'configmachine',
        'vname',
        'vmcpu',
        'vmmemory',
        'endconfigmachine',
        'vmprovision',
        'vmmachinename',
        'vmpassword',

    ]

    def vm_name(self, name):
        self.commands['vmname'] = COMMANDS['vmname'].format(name)
        self.commands['vname'] = COMMANDS['vname'].format(name)
        self.commands['vmmachinename'] = COMMANDS['vmmachinename'].format(
            name.replace('.', '_'))
        self.name = name

    def vm_ip(self, ip):
        self.commands['vmip'] = COMMANDS['vmip'].format(ip)
        self.ip = ip

    def vm_cpu(self, cpu):
        self.commands['vmcpu'] = COMMANDS['vmcpu'].format(cpu)
        self.cpu = cpu

    def vm_memory(self, memory):
        self.commands['vmmemory'] = COMMANDS['vmmemory'].format(memory)
        self.memory = memory

    def vm_path_image(self, image):
        self.image = os.getcwd() + "/" + image

    def vm_disk(self, disk):
        self.disk = disk

    def vm_password(self, password):
        self.commands['vmpassword'] = COMMANDS['vmpassword'].format(password)
        self.password = password

    def create(self):
        self.initial_path = os.getcwd()
        self.create_folder(self.name)
        self.create_vm()
        self.create_vagrantfile()
        os.chdir(self.initial_path)

    def create_folder(self, folder_name):
        if not os.path.isdir("machines"):
            os.system("mkdir machines")
        os.chdir(os.getcwd() + "/machines")
        command = "mkdir {0}".format(folder_name)
        os.system(command)
        folder = os.getcwd() + "/" + folder_name
        os.chdir(folder)

    def create_vm(self):
        command = "vagrant box add {0} {1}".format(self.name, self.image)
        os.system(command)

    def create_vagrantfile(self):
        os.system("vagrant init")
        vagrantfile = open("Vagrantfile", "w")

        for var in self.VARIABLES:
            vagrantfile.write(self.commands[var])
        vagrantfile.write('end')
        vagrantfile.close()
        os.system("vagrant up")

        if self.disk > 40960:
            os.system("vagrant halt")
            vm_path = os.getcwd()
            self.set_disk(self.disk, self.name, vm_path)
            os.system("vagrant up")


class VMDeletion():
    initial_path = None
    name = None

    def vm_name(self, name):
        self.name = name
        self.initial_path = os.getcwd()

    def remove(self):
        halt_command = "vagrant halt"
        destroy_command = 'vagrant destroy --f'
        delete_folder_command = "rm -rf {0}"
        remove_command = "vagrant box remove {0}"
        remove_host_ssh = (
            "ssh-keygen -f '/home/{0}/.ssh/known_hosts'"
            " -R {1}".format(socket.gethostname(), self.name)
        )

        if os.path.isdir("machines"):
            os.chdir(os.getcwd() + "/machines")
            if os.path.isdir(self.name):
                os.chdir(os.getcwd() + "/" + self.name)
                os.system(halt_command)
                os.system(destroy_command)
                os.chdir("..")
                os.system(delete_folder_command.format(self.name))
                os.system(remove_command.format(self.name))
                os.system(remove_host_ssh)
        os.chdir(self.initial_path)


class VMEdition(Disk):
    name = None
    ip = None
    image = None
    cpu = None
    memory = None
    disk = None
    initial_path = None

    commands = {
        'configinit': COMMANDS['configinit'],
        'endconfigmachine': COMMANDS['endconfigmachine'],
        'configmachine': COMMANDS['configmachine']
    }

    VARIABLES = [
        'configinit',
        'vmname',
        'vmip',
        'configmachine',
        'vname',
        'vmcpu',
        'vmmemory',
        'endconfigmachine'
    ]


    def vm_name(self, name):
        self.commands['vmname'] = COMMANDS['vmname'].format(name)
        self.commands['vname'] = COMMANDS['vname'].format(name)
        self.name = name

    def vm_ip(self, ip):
        self.commands['vmip'] = COMMANDS['vmip'].format(ip)
        self.ip = ip

    def vm_cpu(self, cpu):
        self.commands['vmcpu'] = COMMANDS['vmcpu'].format(cpu)
        self.cpu = cpu

    def vm_memory(self, memory):
        self.commands['vmmemory'] = COMMANDS['vmmemory'].format(memory)
        self.memory = memory

    def vm_disk(self, disk):
        self.disk = disk

    def reset_password(self, password):
        variable = [
            'configinit',
            'vmname',
            'vmip',
            'configmachine',
            'vname',
            'vmcpu',
            'vmmemory',
            'endconfigmachine',
            'vmpassword'
        ]
        self.commands['vmpassword'] = COMMANDS['vmpassword'].format(password)
        self.initial_path = os.getcwd()

        if os.path.isdir("machines"):
            os.chdir(os.getcwd() + "/machines")
            if os.path.isdir(self.name):
                os.chdir(os.getcwd() + "/" + self.name)

                os.system("vagrant halt")
                vagrantfile = open("Vagrantfile", "w")

                for var in variable:
                    vagrantfile.write(self.commands[var])
                vagrantfile.write('end')
                vagrantfile.close()

                os.system("vagrant up")
                os.system("vagrant provision")

        os.chdir(self.initial_path)

    def edit(self):
        self.initial_path = os.getcwd()

        if os.path.isdir("machines"):
            os.chdir(os.getcwd() + "/machines")
            if os.path.isdir(self.name):
                os.chdir(os.getcwd() + "/" + self.name)

                os.system("vagrant halt")
                vagrantfile = open("Vagrantfile", "w")

                for var in self.VARIABLES:
                    vagrantfile.write(self.commands[var])
                vagrantfile.write('end')
                vagrantfile.close()

                vm_path = os.getcwd()

                self.set_disk(self.disk, self.name, vm_path)

                os.system("vagrant up")

        os.chdir(self.initial_path)
