//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    client.c
// date:    2017-01-16
// author:  paul.dautry
// purpose:
//      Trusted clients implementation
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#include "rmcp.h"
#include "client.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#define ANSWER_BUFF_SZ 1024

int main(int argc, char **argv)
{
    int err=1;
    int sd;
    struct sockaddr_in saddr;
    uint16_t port=7979;
#ifdef CLIENT_TRUSTED_1
    printf("compiled with: CLIENT_TRUSTED_1\n");
#elif CLIENT_TRUSTED_2
    printf("compiled with: CLIENT_TRUSTED_2\n");
#elif CLIENT_TRUSTED_3
    printf("compiled with: CLIENT_TRUSTED_3\n");
#else /* error case */
#   error Define one of { CLIENT_TRUSTED_1, CLIENT_TRUSTED_2, CLIENT_TRUSTED_3 }
#endif
    // stage 1: create a socket
    sd=socket(AF_INET, SOCK_STREAM, 0);
    if (sd<0) {
        goto abrt;
    }
    printf("info: socket created!\n");
    // stage 2: connect socket to server
    memset(&saddr, 0, sizeof(struct sockaddr_in));  /* clear struct */
    saddr.sin_family=AF_INET;                       /* internet/IP */
    saddr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);   /* incoming addr */
    saddr.sin_port=htons(port);                     /* server port */
    if (connect(sd, (struct sockaddr*) &saddr, sizeof(saddr))<0) {
        goto abrt;
    }
    printf("info: socket connected!\n");
    distribute_payload(sd);
    close(sd);
    /* success */
    err=0;
abrt:
    if (err!=0) {
        perror("err: an error occured! details");
    }
    return err;
}
/*-----------------------------------------------------------------------------
distribute_payload
    
-----------------------------------------------------------------------------*/
int distribute_payload(int sd)
{
    int err=1, status;
    char *answer=(char*)malloc(ANSWER_BUFF_SZ*sizeof(char));
#ifdef CLIENT_TRUSTED_1
    SEND(sd, RMCP_VERS, strlen(RMCP_VERS))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_PLAY, strlen(RMCP_PLAY))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_NEXT, strlen(RMCP_NEXT))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_NEXT, strlen(RMCP_NEXT))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_QUIT, strlen(RMCP_QUIT))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
#elif CLIENT_TRUSTED_2
    SEND(sd, RMCP_VERS, strlen(RMCP_VERS))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_PAUSE, strlen(RMCP_PAUSE))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_NEXT, strlen(RMCP_NEXT))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_PREV, strlen(RMCP_PREV))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_PREV, strlen(RMCP_PREV))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_PLAY, strlen(RMCP_PLAY))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_QUIT, strlen(RMCP_QUIT))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
#elif CLIENT_TRUSTED_3
    SEND(sd, RMCP_VERS, strlen(RMCP_VERS))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_STOP, strlen(RMCP_STOP))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
    SEND(sd, RMCP_SHUTDOWN, strlen(RMCP_SHUTDOWN))
    MEMSET_RECV(sd, answer, ANSWER_BUFF_SZ)
#endif
    err=0;
abrt:
    free(answer);
    return err;
}
