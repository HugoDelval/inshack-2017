#!/bin/bash
TMPUSER="user${RANDOM}"
/usr/bin/id -u ${TMPUSER} 2> /dev/null
while [ $? -eq 0 ]; do
    TMPUSER="user${RANDOM}"
    /usr/bin/id -u ${TMPUSER} 2> /dev/null
done;
/usr/sbin/useradd ${TMPUSER}
bash -c "/bin/sleep 0.5 && (/usr/bin/pkill -9 -u ${TMPUSER} & /usr/sbin/userdel ${TMPUSER})" &
/bin/su -c "echo '${1}' | /usr/bin/python3 /app/yaml_load_dump.py" ${TMPUSER}
