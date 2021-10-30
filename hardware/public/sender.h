// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis, Jonathan Mulyk
#ifndef SENDER
#define SENDER

#pragma once

#include "../public/reader.h"
#include <sys/socket.h>
#include <arpa/inet.h>

//typedef struct UDPServerInfo
typedef struct UDPServerInfo
{
    int sockfd;
    struct sockaddr_in server;
    socklen_t serverLen;
} UDPServerInfo;

//functions 
void UDPClient(UDPServerInfo *serverInfo, int port, char *IP);
int sendData(UDPServerInfo *serverInfo, char *buffer, int buffSize);
int recvData(UDPServerInfo *serverInfo, char *buffer, int buffSize);
void sendStruct(struct Sample *sample, int serverPort, char *serverIP);

#endif