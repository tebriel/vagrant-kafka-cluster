package "scala" do
  version "2.9.2+dfsg-2"
end

package "ufw" do
  action :purge
end

kafka_version = 'kafka_2.9.2-0.8.2.1'

# Vagrant adds 127.0.0.1 <hostname> <hostname> which fucks up kafka
cookbook_file '/etc/hosts'

remote_file "/tmp/kafka.tgz" do
  source "http://apache.mirrors.lucidnetworks.net/kafka/0.8.2.1/#{kafka_version}.tgz"
  checksum "b748030f22ff5b3473094f5e9bee79ab66bca8cbb1bbf31d2cb7022e079e8f56"
end

execute 'tar -xzf /tmp/kafka.tgz -C /opt'
template "/opt/#{kafka_version}/config/server.properties"

execute 'JMX_PORT=9999 KAFKA_HEAP_OPTS=-Xmx512m bin/kafka-server-start.sh -daemon config/server.properties' do
  cwd "/opt/#{kafka_version}"
end

# link "/opt/#{kafka_version}" do
#   to "/opt/kafka"
# end

# cookbook_file '/etc/init.d/kafka'
