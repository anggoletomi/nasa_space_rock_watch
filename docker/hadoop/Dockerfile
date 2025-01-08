FROM apache/hadoop:3.4.1

# Switch to root for yum installs and config changes
USER root

# Fix CentOS repos to use vault.centos.org for 7.6
RUN sed -i 's|^mirrorlist=|#mirrorlist=|g; s|^#baseurl=|baseurl=|g; s|mirror.centos.org|vault.centos.org|g' \
    /etc/yum.repos.d/CentOS-Base.repo \
    /etc/yum.repos.d/CentOS-AppStream.repo \
    /etc/yum.repos.d/CentOS-Extras.repo \
    /etc/yum.repos.d/CentOS-PowerTools.repo || true

RUN yum clean all && yum makecache
RUN yum update -y

# Copy local config from hadoop_conf
COPY hadoop_conf/core-site.xml /opt/hadoop/etc/hadoop/core-site.xml
COPY hadoop_conf/hdfs-site.xml /opt/hadoop/etc/hadoop/hdfs-site.xml

# Install OpenSSH + Java
RUN yum install -y \
    openssh-server \
    openssh-clients \
    java-1.8.0-openjdk-devel && \
    yum clean all

# Generate base host SSH keys if missing
RUN ssh-keygen -A

# Disable strict host checking
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# Patch hadoop-env.sh so Hadoop definitely sees JAVA_HOME
RUN sed -i '/export JAVA_HOME/d' /opt/hadoop/etc/hadoop/hadoop-env.sh && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk" >> /opt/hadoop/etc/hadoop/hadoop-env.sh

# Environment variables for Hadoop scripts
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
ENV PATH=$PATH:$JAVA_HOME/bin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root

# Set up passwordless SSH for root user
# Generate an RSA key pair with an empty passphrase.
RUN mkdir -p /root/.ssh && \
    ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/authorized_keys

# Allow root login with key
RUN sed -i 's/^#*PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config

# Return to root user (already root, but just in case)
USER root
