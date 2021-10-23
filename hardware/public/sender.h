// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis
#ifndef SENDER
#define SENDER

#pragma once

typedef struct UDPServerInfo
{
    int sockfd;
    struct sockaddr_in server;
    socklen_t serverlen;
} UDPSInfo;

void sendStruct(struct Sample sample, const int port, char *ip);

#endif