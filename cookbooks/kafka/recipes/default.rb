package "openjdk-7-jre" do
  version '7u181-2.6.14-0ubuntu0.1'
end

package "ufw" do
  action :purge
end

kafka_version = 'kafka_2.11-0.10.1.1'

# Vagrant adds 127.0.0.1 <hostname> <hostname> which fucks up kafka
cookbook_file '/etc/hosts'

remote_file "/tmp/kafka.tgz" do
  source "http://www-eu.apache.org/dist/kafka/0.10.1.1/#{kafka_version}.tgz"
end

execute 'tar -xzf /tmp/kafka.tgz -C /opt'
template "/opt/#{kafka_version}/config/server.properties"

ENV['JMX_PORT'] = '9999'
ENV['KAFKA_HEAP_OPTS'] = '-Xmx512m'

execute "echo \"export JMX_PORT=#{ENV['JMX_PORT']}\" >> /etc/profile"
execute "echo \"export KAFKA_HEAP_OPTS=#{ENV['KAFKA_HEAP_OPTS']}\" >> /etc/profile"

execute 'bin/kafka-server-start.sh -daemon config/server.properties' do
  cwd "/opt/#{kafka_version}"
end

# link "/opt/#{kafka_version}" do
#   to "/opt/kafka"
# end

# cookbook_file '/etc/init.d/kafka'
