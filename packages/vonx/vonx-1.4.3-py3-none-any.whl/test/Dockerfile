FROM bcgovimages/von-image:py36-1.6-5
#FROM von-anchor-test

ADD --chown=indy:indy requirements.txt .

RUN pip --no-cache-dir install -r requirements.txt && \
    pip --no-cache-dir install gunicorn PyYaml

#RUN pip --no-cache-dir install --upgrade \
#      git+https://github.com/cywolf/von_anchor.git@master

ADD --chown=indy:indy . .

RUN pip --no-cache-dir install -e .

RUN mkdir -p /home/indy/.indy_client/wallet && \
    chown -R indy:indy /home/indy/.indy_client
