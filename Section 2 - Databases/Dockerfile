FROM postgres:latest
ENV POSTGRES_PASSWORD P@ssw0rd
ENV POSTGRES_DB tech_challenge

RUN mkdir /tmp/sql_scripts
RUN mkdir /tmp/sample_data
RUN mkdir /tmp/sql_queries
COPY ./sql_scripts/* /tmp/sql_scripts
COPY ./sample_data/* /tmp/sample_data
COPY ./sql_queries/* /tmp/sql_queries

COPY ./sql_scripts/1-create_tables.sql /docker-entrypoint-initdb.d/

