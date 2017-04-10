//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    multimedia-server.h
// date:    2017-01-16
// author:  paul.dautry
// purpose:
//      Header of the multimedia server implementation
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ifndef _MULTIMEDIA_SERVER_H_
#define _MULTIMEDIA_SERVER_H_

/*-----------------------------------------------------------------------------
handle_client
    Client communication routine
-----------------------------------------------------------------------------*/
int handle_client();
/*-----------------------------------------------------------------------------
handle_client
    Handle client routine
command
        pointer to input command buffer
response
        pointer to future buffer allocated within this method
resp_sz
        Size of response buffer
-----------------------------------------------------------------------------*/
int handle_cmd(const char *command, char **response, int *resp_sz);

#endif /*_MULTIMEDIA_SERVER_H_*/
