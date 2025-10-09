## docker-compose from https://hub.docker.com/_/debian as of October 8, 2025
###########################################################################################
## Modifiert Korbinian Musch
## Oktober 2025 / Au in der Hallertau
## Fan control HP ProLaint Server G9 with modified ILO4 firmware
###########################################################################################

FROM rockylinux:9

LABEL maintainer="Korbinian Musch <deine.email@domain.de>"
LABEL description="Fan control HP ProLiant Server G9 with modified ILO4 firmware"
LABEL version="2025-10-08"

RUN dnf update && \
    dnf install -y openssh-server curl && \
    mkdir /var/run/sshd && \
    echo 'root:rootpasswort' | chpasswd && \
    curl -L -o /root/installer-dnf.sh https://raw.githubusercontent.com/Korbinian0/Luefterregelung-HP-ProLaint-Server-G9/main/installer-dnf.sh && \
    chmod +x /root/installer-dnf.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]