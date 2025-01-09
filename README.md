In order to access host postgress

/etc/postgresql/17/main/postgresql.conf. listen_addresses = '\*'.
So, it does not only listens on localhost

/etc/postgresql/17/main/pg_hba.conf
host all all 172.0.0.0/8 md5 (172.0.0.0/16 is the host ip of docker0)

sudo systemctl restart postgresql
That’s how you can user host service on docker container.
