//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    rmcp.h
// date:    2017-01-16
// author:  paul.dautry
// purpose:
//      Remote Multimedia Controler Protocol
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ifndef _RMCP_H_
#define _RMCP_H_

#define RMCP_CMD_SZ      4
#define RMCP_RDBG        "RDBG"
#define RMCP_PLAY        "PLAY"
#define RMCP_PAUSE       "PAUS"
#define RMCP_STOP        "STOP"
#define RMCP_NEXT        "NEXT"
#define RMCP_PREV        "PREV"
#define RMCP_QUIT        "QUIT"
#define RMCP_VERS        "VERS"
#define RMCP_SHUTDOWN    "SHUT"
#define RMCP_OK          "OK"
#define RMCP_KO          "KO"
#define RMCP_VERSION     "1.0b"

#define SEND(sd, content, len)                                                \
    if (len==0) {                                                             \
        printf("warn: len is 0 when calling send.\n");                        \
    }                                                                         \
    printf("info: sending: %s\n", content);                                   \
    status=send(sd, content, len, 0);                                         \
    if (status==0) {                                                          \
        printf("warn: peer disconnected\n");                                  \
        goto abrt;                                                            \
    } else if (status<0) {                                                    \
        printf("err: an error occured while calling send\n");                 \
        goto abrt;                                                            \
    }

#define RECV(sd, content, len)                                                \
    if (len==0) {                                                             \
        printf("warn: len is 0 when calling recv.\n");                        \
    }                                                                         \
    status=recv(sd, content, len, 0);                                         \
    if (status==0) {                                                          \
        printf("warn: peer disconnected\n");                                  \
        goto abrt;                                                            \
    } else if (status<0) {                                                    \
        printf("err: an error occured while calling recv\n");                 \
        goto abrt;                                                            \
    }                                                                         \
    printf("info: received: %s\n", content);

#define MEMSET_RECV(sd, buf, sz)                                              \
    memset((buf), 0, (sz));                                                   \
    RECV((sd), (buf), (sz))

#endif /*_RMCP_H_*/
