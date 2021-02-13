FROM python:3.7

# Set C.UTF-8 locale as default (Needed by the Click library)
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8


WORKDIR /root

# Create directories for config, data and logs
RUN mkdir --parents .local/share/osm_wheelchair

# Copy osm_wheelchair workers repo from local repo
COPY osm_wheelchair/ osm_wheelchair/
COPY config/ config/
COPY requirements.txt .
COPY setup.py .

# Update setuptools and install osm_wheelchair with dependencies (requirements.txt)
RUN pip3 install --upgrade setuptools
RUN pip3 install .

