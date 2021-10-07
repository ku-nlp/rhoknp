FROM ubuntu:latest AS builder
WORKDIR /app
ENV DEBIAN_FRONTEND noninteractive
ARG JPP_VERSION=2.0.0-rc3

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make cmake libprotobuf-dev wget ca-certificates \
    zlib1g-dev libtool automake autoconf git unzip

# Build and install Juman++
RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v${JPP_VERSION}/jumanpp-${JPP_VERSION}.tar.xz -qO - \
    | tar Jxvf - \
    && cd jumanpp-${JPP_VERSION} \
    && mkdir bld \
    && cd bld \
    && cmake .. -DCMAKE_BUILD_TYPE=Release \
    && make -j "$(nproc)" \
    && make install

# Build and install KNP
RUN git clone --depth 1 https://github.com/ku-nlp/knp.git \
    && cd knp \
    && ./autogen.sh \
    && wget -q http://lotus.kuee.kyoto-u.ac.jp/nl-resource/knp/dict/latest/knp-dict-latest-bin.zip \
    && unzip knp-dict-latest-bin.zip \
    && cp -ars $(pwd)/dict-bin/* ./dict \
    && ./configure \
    && make -j "$(nproc)" \
    && make install

FROM ubuntu:latest AS runner

# Configure Japanese locale
RUN apt-get update \
    && apt-get install -y locales \
    && locale-gen ja_JP.UTF-8
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="en_US" \
    LC_ALL="ja_JP.UTF-8"
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

COPY --from=builder /usr/local /usr/local

CMD /bin/bash
