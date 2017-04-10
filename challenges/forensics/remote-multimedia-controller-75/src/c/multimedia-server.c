//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    multimedia-server.c
// date:    2017-01-16
// author:  paul.dautry
// purpose:
//      Source code of multimedia server
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#include "multimedia-server.h"
#include "rmcp.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>

#define FOR_BUFF_SZ 1024
#define CMD_BUFF_SZ 64
#define CMD_RECV_SZ 128
#define PORT        7979

#define PRINT_CMD(cmd)                                                        \
    printf("info: %s command received\n", cmd)

#define HANDLE_CMD(cmd, resp, resp_sz, content, sz)                           \
    PRINT_CMD(cmd);                                                           \
    (resp)=(char*)calloc((sz),sizeof(char));                                  \
    strncpy((resp), (content), (sz));                                         \
    (resp_sz)=sz

static int __shutdown=0;
static int client_sd;

int main(int argc, char **argv)
{
    int err=1;
    int sd, has_client=0;
    uint16_t port=PORT;
    struct sockaddr_in saddr, paddr;
    socklen_t paddr_len;
    // stage 1: socket creation
    sd=socket(AF_INET, SOCK_STREAM, 0);
    if (sd<0) {
        goto abrt;
    }
    printf("info: socket created!\n");
    // stage 2: bind socket to local address
    memset(&saddr, 0, sizeof(struct sockaddr_in));  /* clear struct */
    saddr.sin_family=AF_INET;                       /* internet/IP */
    saddr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);   /* incoming addr */
    saddr.sin_port=htons(port);                     /* server port */
    if (bind(sd, (struct sockaddr *) &saddr, sizeof(saddr))<0) {
        goto abrt;
    }
    printf("info: socket binded!\n");
    // stage 3: listen
    if (listen(sd, 1)<0) {
        goto abrt;
    }
    printf("info: listening!\n");
    // stage 4: accept
    do {
        client_sd=accept(sd, (struct sockaddr *) &paddr, &paddr_len);
        if (client_sd<0) {
            goto abrt;
        }
        printf("info: client accepted!\n");
        if (handle_client()<0) {
            goto abrt;
        }
        close(client_sd);
    } while (__shutdown==0);
    printf("info: shutdown requested.\n");
    close(sd);
    /* success */
    err=0;
abrt:
    if (err!=0) {
        perror("err: an error occured! details");
    }
    printf("info: exiting.\n");
    return err; 
}
/*-----------------------------------------------------------------------------
handle_client
    Client communication routine
-----------------------------------------------------------------------------*/
int handle_client()
{
    int err=1;
    int status;
    int resp_sz;
    char *resp=NULL;
    int (*process_command)(const char*, char**, int*);
    char command[CMD_BUFF_SZ];
    process_command=&handle_cmd;
    do {
        memset(command, 0, CMD_BUFF_SZ);
        RECV(client_sd, command, CMD_RECV_SZ);
        printf("dbg: process_command: %p\n", *process_command);
        err=(*process_command)(command, &resp, &resp_sz);
        if (err!=0) {
            goto abrt;
        }
        printf("info: response (size=%d) is: %s\n", resp_sz, resp);
        SEND(client_sd, resp, resp_sz);
        free(resp); resp=NULL;
    } while(strcmp(command, RMCP_QUIT)&&strcmp(command, RMCP_SHUTDOWN));
    err=0;
abrt:
    return err;
}
/*-----------------------------------------------------------------------------
handle_client
    Handle client routine
-----------------------------------------------------------------------------*/
int handle_cmd(const char *command, char **response, int *resp_sz)
{
    int err=1;
    if (!strncmp(command, RMCP_PLAY, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_PLAY, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_PAUSE, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_PAUSE, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_STOP, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_STOP, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_NEXT, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_NEXT, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_PREV, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_PREV, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_VERS, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_VERS, *response, *resp_sz, RMCP_OK" "RMCP_VERSION, 
            strlen(RMCP_OK" "RMCP_VERSION));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_QUIT, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_QUIT, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        // fake controler nothing to do here
    } else if (!strncmp(command, RMCP_SHUTDOWN, RMCP_CMD_SZ)) {
        HANDLE_CMD(RMCP_SHUTDOWN, *response, *resp_sz, RMCP_OK, strlen(RMCP_OK));
        __shutdown=1;
    } else if (!strncmp(command, RMCP_RDBG, RMCP_CMD_SZ)) {
        PRINT_CMD(command);
        (*resp_sz)=256;
        (*response)=(char*)calloc((*resp_sz),sizeof(char));
        snprintf(*response, (*resp_sz), "command: %p\nclient_sd: %d", 
            command, client_sd);
    } else {
        HANDLE_CMD("<unknown>", *response, *resp_sz, RMCP_KO, strlen(RMCP_KO));
    }
    err=0;
abrt:
    return err;
}
