FROM ubuntu:22.04@sha256:0a9887931b0e38af2e3487ed39e29436b0535c4f3f52e57745baaf79d1898956

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        ca-certificates curl wget git file less procps \
        gcc g++ gcc-multilib g++-multilib make gawk bison nasm binutils patchelf \
        gdb gdbserver libc6-dbg glibc-source strace ltrace \
        python3 python3-pip python3-dev python3-venv \
        ruby-dev libssl-dev libffi-dev libseccomp-dev \
        netcat-openbsd socat tmux vim-gtk3 fish locales && \
    sed -i 's/^# *en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen && \
    locale-gen

RUN pip3 install pwntools

RUN gem install --no-document seccomp-tools one_gadget

RUN git clone --depth 1 https://github.com/pwndbg/pwndbg /root/pwndbg && \
    cd /root/pwndbg && \
    UV_CONCURRENT_DOWNLOADS=2 ./setup.sh

RUN git clone --depth 1 https://github.com/scwuaptx/Pwngdb.git /root/Pwngdb && \
    sed '/peda\/peda.py/d' /root/Pwngdb/.gdbinit >> /root/.gdbinit

ENV SHELL=/usr/bin/fish

WORKDIR /work
CMD ["/usr/bin/fish"]
