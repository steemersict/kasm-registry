ARG BASE_TAG="1.19.0"
FROM kasmweb/core-ubuntu-noble:${BASE_TAG}
USER root

# Versie + checksum samen bijwerken (sha256 staat bij de release-asset op GitHub)
ARG FERDIUM_VERSION=7.2.3
ARG FERDIUM_SHA256=f8a3f5d3b6bc4e6af6a91f291fe807b97a84aa20b91313c65e860ea95d54adba

ENV HOME=/home/kasm-default-profile \
    STARTUPDIR=/dockerstartup
WORKDIR $HOME

RUN set -eux; \
    apt-get update; \
    wget -q -O /tmp/ferdium.deb "https://github.com/ferdium/ferdium-app/releases/download/v${FERDIUM_VERSION}/Ferdium-linux-${FERDIUM_VERSION}-amd64.deb"; \
    echo "${FERDIUM_SHA256}  /tmp/ferdium.deb" | sha256sum -c -; \
    apt-get install -y /tmp/ferdium.deb; \
    sed -i 's|Exec=/opt/Ferdium/ferdium %U|Exec=/opt/Ferdium/ferdium --no-sandbox %U|' /usr/share/applications/ferdium.desktop; \
    mkdir -p $HOME/Desktop; \
    cp /usr/share/applications/ferdium.desktop $HOME/Desktop/; \
    chmod +x $HOME/Desktop/ferdium.desktop; \
    rm -rf /tmp/ferdium.deb /var/lib/apt/lists/* /var/tmp/*

COPY custom_startup.sh $STARTUPDIR/custom_startup.sh
RUN chmod 755 $STARTUPDIR/custom_startup.sh

# Desktop voor één applicatie (zoals de officiële Kasm-appimages)
RUN cp $HOME/.config/xfce4/xfconf/single-application-xfce-perchannel-xml/* $HOME/.config/xfce4/xfconf/xfce-perchannel-xml/ && \
    cp /usr/share/backgrounds/bg_kasm.png /usr/share/backgrounds/bg_default.png && \
    apt-get remove -y xfce4-panel

RUN chown -R 1000:0 $HOME

ENV HOME=/home/kasm-user
WORKDIR $HOME
RUN mkdir -p $HOME && chown -R 1000:0 $HOME

USER 1000
