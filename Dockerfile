FROM debian:latest
WORKDIR /app
ENV DEBIAN_FRONTEND noninteractive
ARG JPP_VERSION=2.0.0-rc3

# Japanese
RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE en_US
ENV LC_ALL=
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# Install Juman++
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make cmake libprotobuf-dev wget ca-certificates \
    && wget -q https://github.com/ku-nlp/jumanpp/releases/download/v${JPP_VERSION}/jumanpp-${JPP_VERSION}.tar.xz \
    && tar xf jumanpp-${JPP_VERSION}.tar.xz \
    && cd jumanpp-${JPP_VERSION} \
    && mkdir bld \
    && cd bld \
    && cmake .. -DCMAKE_BUILD_TYPE=Release \
    && make -j "$(nproc)" \
    && make install \
    && cd /app \
    && rm jumanpp-${JPP_VERSION}.tar.xz \
    && rm -rf jumanpp-${JPP_VERSION}

# Install KNP
RUN apt-get update && apt-get install -y --no-install-recommends \
    zlib1g-dev libtool automake autoconf git unzip \
    && git clone --depth 1 https://github.com/ku-nlp/knp.git \
    && cd knp \
    && ./autogen.sh \
    && wget -q http://lotus.kuee.kyoto-u.ac.jp/nl-resource/knp/dict/latest/knp-dict-latest-bin.zip \
    && unzip knp-dict-latest-bin.zip \
    && cp -ars $(pwd)/dict-bin/* ./dict \
    && ./configure \
    && make -j "$(nproc)" \
    && make install \
    && cd /app \
    && rm -rf knp \
    && apt-get purge -y automake autoconf git unzip wget

# Clean up all temporary files
RUN apt-get clean \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /tmp/* /var/tmp/* \
    && rm -rf /var/lib/apt/lists/*

CMD /bin/bash
