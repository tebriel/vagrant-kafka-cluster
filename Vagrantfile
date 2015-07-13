# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  3.times do |idx|
    my_id = idx + 1
    config.vm.define "zookeeper#{my_id}", primary: (my_id == 1) do |zk|
      zk.vm.network "private_network", ip: "192.168.33.1#{my_id}"
      zk.vm.hostname = "zookeeper#{my_id}"
      zk.vm.provision "chef_solo" do |chef|
        # chef.log_level = :debug
        chef.cookbooks_path = "cookbooks"
        chef.add_recipe "zookeeper"
        if my_id == 1
          chef.add_recipe "kafka::kafka_manager"
        end
        chef.json = {
          "zookeeper" => {
            # Must start at 1
            "myid" => my_id
          }
        }
      end
    end
  end

  3.times do |idx|
    my_id = idx + 1
    config.vm.define "kafka#{my_id}" do |kafka|
      kafka.vm.network "private_network", ip: "192.168.33.2#{my_id}"
      kafka.vm.hostname = "kafka#{my_id}"
      kafka.vm.provision "chef_solo" do |chef|
        # chef.log_level = :debug
        chef.cookbooks_path = "cookbooks"
        chef.add_recipe "kafka"
        chef.json = {
          "kafka" => {
            # Must start at 1
            "myid" => my_id
          }
        }
      end
    end
  end
end
