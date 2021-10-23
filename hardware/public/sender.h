// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis, Jonathan Mulyk
#ifndef SENDER
#define SENDER

#pragma once

typedef struct UDPServerInfo
{
    int sockfd;
    struct sockaddr_in server;
    socklen_t serverlen;
} UDPSInfo;

//functions 
UDPClient(UDPServerInfo *serverInfo, int port, char *IP);
int sendData(UDPServerInfo *serverInfo, char *buffer, int buffSize);
int recvData(UDPServerInfo *serverInfo, char *buffer, int buffSize);
void sendStruct(struct Sample *sample, const int serverPort, char *serverIP);

#endif