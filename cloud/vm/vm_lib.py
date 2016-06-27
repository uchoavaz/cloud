
import os
import socket

COMMANDS = {

    """
    Esta variável consiste em armazenar um dicionário
    dos comandos que poderão ser escritos no VagranFile de
    cada máquina virtual peo Vagrant
    """

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
    'vmshell': '  sudo apt-get install openssl shellinabox <<EOF\nY\n  EOF\n',
    'vmpassword': (
        '  sudo passwd vagrant <<EOF\n'
        '{0}\n'
        '{0}\n'
        '  EOF\n'
    ),
    'vmprovisionend': '  SHELL\n'

}


class Disk():
    """
    Esta classe é responsável por modificar o tamanho do
    disco de uma determinada máquina virtual
    """

    def set_disk(self, disk, vm_name, atual_path):
        """
        Este método é responsável por definir qual o tamanho que o
        usuário deseja setar em uma maquina virtual passada para ele
        """
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
    """
    Esta classe é reponsável por criar uma máquina virtual
    pelo vagrant
    """
    name = None
    ip = None
    image = None
    cpu = None
    memory = None
    disk = None
    password = None
    initial_path = None

    commands = {
        """
        Esta variável define os comandos que realmente 
        serão setados no Vagranfile
        """
        'configinit': COMMANDS['configinit'],
        'endconfigmachine': COMMANDS['endconfigmachine'],
        'configmachine': COMMANDS['configmachine'],
        'vmprovision': COMMANDS['vmprovision'],
        'vmprovisionend': COMMANDS['vmprovisionend'],
        'vmshell': COMMANDS['vmshell']
    }

    VARIABLES = [
        """
        Esta lista representa qual será a ordem de escrita de cada
        variável definida em "commands"
        """
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
        'vmprovisionend',
        'vmprovision',
        'vmshell',
        'vmprovisionend',

    ]

    def vm_name(self, name):
        """
        Define o nome da VM
        """
        self.commands['vmname'] = COMMANDS['vmname'].format(name)
        self.commands['vname'] = COMMANDS['vname'].format(name)
        self.commands['vmmachinename'] = COMMANDS['vmmachinename'].format(
            name.replace('.', '_'))
        self.name = name

    def vm_ip(self, ip):
        """
        Define o ip da máquina na rede privada
        """
        self.commands['vmip'] = COMMANDS['vmip'].format(ip)
        self.ip = ip

    def vm_cpu(self, cpu):
        """
        Define a quantidade de core da VM
        """
        self.commands['vmcpu'] = COMMANDS['vmcpu'].format(cpu)
        self.cpu = cpu

    def vm_memory(self, memory):
        """
        Define a memória da máquina em MB
        """
        self.commands['vmmemory'] = COMMANDS['vmmemory'].format(memory)
        self.memory = memory

    def vm_path_image(self, image):
        """
        Define onde está a imagem para contruir a VM
        """
        self.image = os.getcwd() + "/" + image

    def vm_disk(self, disk):
        """
        Define o tamanho do disco na VM
        """
        self.disk = disk

    def vm_password(self, password):
        """
        Define a senha da conexao ssh com a VM
        """
        self.commands['vmpassword'] = COMMANDS['vmpassword'].format(password)
        self.password = password

    def create(self):
        """
        Este método executa automaticamente os processos de criação 
        da vm listados abaixo
        """
        self.initial_path = os.getcwd()
        self.create_folder(self.name)
        self.create_vm()
        self.create_vagrantfile()
        os.chdir(self.initial_path)

    def create_folder(self, folder_name):
        """
        Cria a a pasta no computador raiz referente a VM em instância
        """
        if not os.path.isdir("machines"):
            os.system("mkdir machines")
        os.chdir(os.getcwd() + "/machines")
        command = "mkdir {0}".format(folder_name)
        os.system(command)
        folder = os.getcwd() + "/" + folder_name
        os.chdir(folder)

    def create_vm(self):
        """
        Executa o comando de criação da VM
        """
        command = "vagrant box add {0} {1}".format(self.name, self.image)
        os.system(command)

    def create_vagrantfile(self):
        """
        Cria o VagrantFile dentro da pasta listada acima
        """
        os.system("vagrant init")
        vagrantfile = open("Vagrantfile", "w")

        for var in self.VARIABLES:
            vagrantfile.write(self.commands[var])
        vagrantfile.write('end')
        vagrantfile.close()
        os.system("vagrant up")

        if self.disk > 40960:
            """
            O vagrant, por padrão, cria a máquina com 40 GB. Caso a máquina
            seja maior de este valor, ele pausa a máquina faz o aumento do
            disco e sobe a máquina novamente
            """
            os.system("vagrant halt")
            vm_path = os.getcwd()
            self.set_disk(self.disk, self.name, vm_path)
            os.system("vagrant up")


class VMDeletion():
    """
    Esta classe é reponsável por deletar do computador raiz uma VM antes já criada
    """
    initial_path = None
    name = None

    def vm_name(self, name):
        """
        Define o nome da VM
        """
        self.name = name
        self.initial_path = os.getcwd()

    def remove(self):
        """
        Remove a VM da máquina e todos os seus vestígios
        """
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
    """
    Esta classe é responsável por editar/alterar as configurações de 
    uma VM antes já criada
    """
    name = None
    ip = None
    image = None
    cpu = None
    memory = None
    disk = None
    initial_path = None

    commands = {
        """
        Esta variável define os comandos que realmente
        serão setados no Vagranfile
        """
        'configinit': COMMANDS['configinit'],
        'endconfigmachine': COMMANDS['endconfigmachine'],
        'configmachine': COMMANDS['configmachine'],
        'vmprovision': COMMANDS['vmprovision'],
        'vmprovisionend': COMMANDS['vmprovisionend']
    }

    VARIABLES = [
        """
        Esta lista representa qual será a ordem de escrita de cada
        variável definida em "commands"
        """

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
        'vmprovisionend'
    ]

    def vm_name(self, name):
        """
        Define o nome da VM
        """
        self.commands['vmname'] = COMMANDS['vmname'].format(name)
        self.commands['vname'] = COMMANDS['vname'].format(name)
        self.commands['vmmachinename'] = COMMANDS['vmmachinename'].format(
            name.replace('.', '_'))
        self.name = name

    def vm_ip(self, ip):
        """
        Define o ip da máquina na rede privada
        """
        self.commands['vmip'] = COMMANDS['vmip'].format(ip)
        self.ip = ip

    def vm_cpu(self, cpu):
        """
        Define a quantidade de core da VM
        """
        self.commands['vmcpu'] = COMMANDS['vmcpu'].format(cpu)
        self.cpu = cpu

    def vm_memory(self, memory):
        """
        Define a memória da máquina em MB
        """
        self.commands['vmmemory'] = COMMANDS['vmmemory'].format(memory)
        self.memory = memory

    def vm_disk(self, disk):
        """
        Define o tamanho do disco na VM
        """
        self.disk = disk

    def reset_password(self, password):
        """
        Reseta a senha de conexão ssh com a VM
        Também refaz o VagranFile
        """
        variables = [
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
            'vmprovisionend'
        ]
        self.commands['vmpassword'] = COMMANDS['vmpassword'].format(password)
        self.initial_path = os.getcwd()

        if os.path.isdir("machines"):
            os.chdir(os.getcwd() + "/machines")
            if os.path.isdir(self.name):
                os.chdir(os.getcwd() + "/" + self.name)

                os.system("vagrant halt")
                vagrantfile = open("Vagrantfile", "w")

                for var in variables:
                    vagrantfile.write(self.commands[var])
                vagrantfile.write('end')
                vagrantfile.close()

                os.system("vagrant up")
                os.system("vagrant provision")

        os.chdir(self.initial_path)

    def edit(self):
        """
        Executa os comandos de dar pausa na VM para subir as modificações
        para a VM
        """
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
                os.system("vagrant provision")

        os.chdir(self.initial_path)
