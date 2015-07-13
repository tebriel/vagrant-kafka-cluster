user 'kafka-manager'
group 'kafka-manager'

dpkg_package "kafka-manager_1.2.5_all.deb" do
  source "/vagrant/kafka-manager_1.2.5_all.deb"
end

cookbook_file "/usr/share/kafka-manager/conf/application.conf"

# Have to do this because kafka-manager is looking for kafka-manager-zookeeper
# Likely it can't find its config file, possibly related to these issues:
# https://github.com/yahoo/kafka-manager/issues/16
# and
# https://github.com/yahoo/kafka-manager/issues/11
cookbook_file "/etc/init/kafka-manager.conf"

execute "chown -R kafka-manager:kafka-manager /usr/share/kafka-manager"
execute "chown -R kafka-manager:kafka-manager /var/log/kafka-manager"

service "kafka-manager" do
  action :restart
end
# The below builds the kafka-manager
# package "git"
#
# package "openjdk-7-jdk"
# package "openjdk-7-jre" do
#   version '7u79-2.5.5-0ubuntu0.14.04.2'
# end
#
# cookbook_file '/etc/apt/sources.list.d/sbt.list'
# execute 'apt-get update'
#
# package 'sbt' do
#   version "0.13.8"
#   options "--allow-unauthenticated"
# end
#
# git "/opt/kafka-manager" do
#   repository "https://github.com/yahoo/kafka-manager.git"
#   revision 'master'
# end
#
# execute "sbt -J-Xms256m -J-Xmx512m clean dist" do
#   cwd "/opt/kafka-manager"
# end

# This will fail because it never returns
# execute "bin/kafka-manager"
