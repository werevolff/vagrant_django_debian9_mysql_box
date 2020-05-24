# -*- mode: ruby -*-
# vi: set ft=ruby :

##
# This function gets count of the available cpus count
def get_cpus_count()
    host = RbConfig::CONFIG['host_os']
    if host =~ /darwin/
        cpus = `sysctl -n hw.ncpu`.to_i
    elsif host =~ /linux/
        cpus = `nproc`.to_i
    else
        cpus = `wmic cpu get NumberOfCores`.split("\n")[2].to_i
    end
    return cpus
end

##
# This function gets a share from the total RAM size
def get_memory_size(divider)
    host = RbConfig::CONFIG['host_os']
    if host =~ /darwin/
        # sysctl returns Bytes and we need to convert to MB
        mem = `sysctl -n hw.memsize`.to_i / 1024 / 1024 / divider
    elsif host =~ /linux/
        cpus = `nproc`.to_i
        mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i / 1024 / divider
    else
        cpus = `wmic cpu get NumberOfCores`.split("\n")[2].to_i
        mem = `wmic OS get TotalVisibleMemorySize`.split("\n")[2].to_i / 1024 / divider
    end
    return mem
end

Vagrant.configure(2) do |config|
    config.env.enable
    config.vm.synced_folder ".", "/vagrant", owner: ENV['DEFAULT_USER']
    config.vagrant.plugins = ["vagrant-vbguest", "vagrant-env"]
    config.vm.provider "virtualbox" do |vb|
        # Don't boot with headless mode
        # vb.gui = true
        vb.memory = 2048
        vb.cpus = 2
        vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/vagrant", "1"]
    end

    config.vm.define "django_debian9_mysql", primary: true, autorestart: false do |django_debian9_mysql|
        django_debian9_mysql.vm.box = "generic/debian9"
        django_debian9_mysql.vm.network "private_network", ip: ENV['PRIVATE_NETWORK_IP']
        django_debian9_mysql.vm.network "forwarded_port", guest: ENV['SSH_PORT_GUEST'], host: ENV['SSH_PORT_HOST'], id: "ssh"

        django_debian9_mysql.vm.provision "django_debian9", type: "shell" do |shell|
            shell.path = "build_box/install_ansible.sh"
            shell.privileged = false
            shell.keep_color = true
        end

        ansible_base_vars = {
            MYSQL_ROOT_PASSWORD: ENV['MYSQL_ROOT_PASSWORD'],
            PYENV_ROOT: ENV['PYENV_ROOT'],
            PYTHON_SYSTEM_VERSION: ENV['PYTHON_SYSTEM_VERSION'],
            DEFAULT_USER: ENV['DEFAULT_USER'],
        }
        ansible_provision_vars = {
            PYTHON_PROJECT_VERSION: ENV['PYTHON_PROJECT_VERSION'],
            REQUIREMENTS_PATH: ENV['REQUIREMENTS_PATH'],
            GUNICORN_BACKEND_PID_DIR: ENV['GUNICORN_BACKEND_PID_DIR'],
            GUNICORN_BACKEND_LOG_DIR: ENV['GUNICORN_BACKEND_LOG_DIR'],
            BACKEND_PATH: ENV['BACKEND_PATH'],
            BACKEND_ENV_PATH: ENV['BACKEND_ENV_PATH'],
            MAIN_APP_NAME: ENV['MAIN_APP_NAME'],
            GUNICORN_BIND: ENV['GUNICORN_BIND'],
            DROP_DATABASE: ENV['DROP_DATABASE'],
            MYSQL_DB: ENV['MYSQL_DB'],
            MYSQL_USER: ENV['MYSQL_USER'],
            MYSQL_PASSWORD: ENV['MYSQL_PASSWORD'],
            MEDIA_ROOT: ENV['MEDIA_ROOT'],
            CELERY_BACKEND_PID_DIR: ENV['CELERY_BACKEND_PID_DIR'],
            CELERY_BACKEND_LOG_DIR: ENV['CELERY_BACKEND_LOG_DIR'],
            RABBITMQ_VHOST: ENV['RABBITMQ_VHOST'],
            RABBITMQ_USER: ENV['RABBITMQ_USER'],
            RABBITMQ_PASSWORD: ENV['RABBITMQ_PASSWORD'],
            VENV_PATH: ENV['VENV_PATH'],
            CELERY_BEAT_BACKEND_PID_DIR: ENV['CELERY_BEAT_BACKEND_PID_DIR'],
            CELERY_BEAT_BACKEND_LOG_DIR: ENV['CELERY_BEAT_BACKEND_LOG_DIR'],
        }

        django_debian9_mysql.vm.provision "ansible_local" do |ansible_build_box|
            ansible_build_box.inventory_path      = './build_box/hosts'
            ansible_build_box.limit               = 'local'
            ansible_build_box.playbook            = 'build_box/vagrant.yml'
            ansible_build_box.verbose             = 'vvvv'
            ansible_build_box.config_file         = 'ansible.cfg'
            ansible_build_box.raw_arguments       = ['-e ansible_python_interpreter=/usr/bin/python3']
            ansible_build_box.extra_vars          = ansible_base_vars
        end

        if ENV['RUN_DJANGO_PROJECT'] == 'true'
            django_debian9_mysql.vm.provision "ansible_local" do |ansible_provision|
                ansible_provision.inventory_path      = './build_box/hosts'
                ansible_provision.limit               = 'local'
                ansible_provision.playbook            = 'django/provision/vagrant.yml'
                ansible_provision.verbose             = 'vvvv'
                ansible_provision.config_file         = 'ansible.cfg'
                ansible_provision.raw_arguments       = ['-e ansible_python_interpreter=/usr/bin/python3']
                ansible_provision.extra_vars          = ansible_base_vars.merge(ansible_provision_vars)
            end
        end

        django_debian9_mysql.vm.box_check_update = true
    end
end
