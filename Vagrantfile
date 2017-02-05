# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_API_VERSION = "2"
Vagrant.configure(VAGRANT_API_VERSION) do |config|
  config.vm.define "dev", primary: true do |dev|
    dev.vm.box = "ubuntu/trusty64"

    # Provision using shell
    dev.vm.host_name = "dev.paperless"
    dev.vm.synced_folder ".", "/opt/paperless"
    dev.vm.provision "shell", path: "scripts/vagrant-provision"

    # Networking details
    dev.vm.network "private_network", ip: "172.28.128.4"
  end


  config.vm.define "docker" do |docker|
    docker.vm.box = "ailispaw/barge"
    docker.vm.synced_folder ".", "/opt/paperless"
  end
end
