FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y haproxy python3
COPY haproxy.cfg /etc/haproxy/haproxy.cfg
COPY add_ha_custom_params.py /
RUN echo 'INSA{1_H0p3_You_lik3d_1t_it_w@s_really_fun_to_do}' > /var/lib/haproxy/the_flag_q4ZIDK2PYLo5yVszgsWZ

CMD /add_ha_custom_params.py && \
    service haproxy start && \
    tail -f /var/log/dmesg
