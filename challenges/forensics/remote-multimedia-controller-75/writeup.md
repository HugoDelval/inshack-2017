# Writeup - Remote Multimedia Controller

You have a .pcap file, a Wireshark capture.

Open the .pcap file with Wireshark and dissect TCP packets.

You will quickly realize something is going on between multiple clients and a server and it seems that there is a protocol used.

The last client to connect to the server is a strange one, it sends commands which seem to be unreadable.

What this last client is trying to achieve is in fact an exploiting a buffer overflow vulnerability in the server.

Its attack is successful and one of the last TCP packets contains the content of a file which is base64 encoded.

Yet if you try to base64-decode the string you'll not obtain a plaintext. 

Here you know what happened, the plaintext was base64-encoded multiple times.

You can retrieve the plaintext by looping on a base64-decode operation until you get a flag.
