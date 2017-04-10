//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// file:    client.h
// date:    2017-01-16
// author:  paul.dautry
// purpose:
//      Trusted clients header
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ifndef _CLIENT_H_
#define _CLIENT_H_

/*-----------------------------------------------------------------------------
distribute_payload
    Distribute the payload
sd
    socket descriptor on which the attack must be performed
-----------------------------------------------------------------------------*/
int distribute_payload(int sd);

#endif /*_CLIENT_H_*/
