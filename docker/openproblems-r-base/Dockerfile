FROM singlecellopenproblems/openproblems:latest

ARG NB_USER="sagemaker-user"
ARG NB_UID="1000"
ARG NB_GID="100"

USER $NB_UID

# Make the default shell bash (vs "sh") for a better Jupyter terminal UX
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    HOME=/home/$NB_USER

USER root
WORKDIR /

# Install R
RUN apt-get update -qq
RUN apt-get -yq --no-install-suggests --no-install-recommends --allow-unauthenticated install dirmngr ca-certificates gnupg gpgv gfortran libblas-dev liblapack-dev
RUN gpg --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN gpg --output key.gpg --export 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN apt-key add key.gpg
RUN echo 'deb http://cloud.r-project.org/bin/linux/debian buster-cran40/' >> /etc/apt/sources.list
RUN apt-get update -qq
RUN apt-get install -yq --no-install-suggests --no-install-recommends r-base-dev=4.0\*
RUN apt-get clean -y && apt-get autoremove -y

# Install R packages
RUN R -e "install.packages('renv'); renv::consent(TRUE)"
COPY ./docker/openproblems-r-base/r_requirements.txt ./r_requirements.txt
RUN R -e "renv::install(scan('r_requirements.txt', sep='\n', what=character()))"

# Install kernelspec
RUN R -e "IRkernel::installspec(user = FALSE);"

# Install single-cell open problems with R requirements
COPY . /usr/src/singlecellopenproblems
RUN cd /usr/src/singlecellopenproblems && git clean -fxdq
RUN pip install --no-cache-dir --editable /usr/src/singlecellopenproblems[r]

# Fix permissions
RUN chown -R $NB_USER:$NB_GID /home/$NB_USER

USER $NB_UID
WORKDIR $HOME
