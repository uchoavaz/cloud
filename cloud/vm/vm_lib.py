import os

COMMANDS = {
    'configinit': 'Vagrant.configure(2) do |config|\n',
    'vmname': '  config.vm.box = "{0}"\n',
    'vmip': '  config.vm.network "public_network", bridge: "wlan0", ip: "{0}" \n',
    'configmachine': '  config.vm.provider "virtualbox" do |v|\n',
    'vmcpu': '    v.cpus = {0}\n',
    'vmmemory': '    v.memory = {0}\n',
    'endconfigmachine': '  end\n'

}

VARIABLES = [
    'configinit',
    'vmname',
    'vmip',
    'configmachine',
    'vmcpu',
    'vmmemory',
    'endconfigmachine'
]

class VMCreation():
    name = None
    ip = None
    image = None
    cpu = None
    memory = None
    commands = {
        'configinit': COMMANDS['configinit'],
        'endconfigmachine': COMMANDS['endconfigmachine'],
        'configmachine': COMMANDS['configmachine']
    }
    initial_path = None

    def vm_name(self, name):
        self.commands['vmname'] = COMMANDS['vmname'].format(name)
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

        for var in VARIABLES:
            vagrantfile.write(self.commands[var])
        vagrantfile.write('end')
        vagrantfile.close()
        os.system("vagrant up")


class VMDeletion():
    initial_path = None
    name = None

    def vm_name(self, name):
        self.name = name
        self.initial_path = os.getcwd()

    def remove(self):
        halt_command = "vagrant halt"
        delete_folder_command = "rm -rf {0}"
        remove_command = "vagrant box remove {0}"
        if os.path.isdir("machines"):
            os.chdir(os.getcwd() + "/machines")
            print (os.getcwd())
            if os.path.isdir(self.name):
                os.chdir(os.getcwd() + "/" + self.name)
                os.system(halt_command)
                os.chdir("..")
                os.system(delete_folder_command.format(self.name))
                os.system(remove_command.format(self.name))
        os.chdir(self.initial_path)
