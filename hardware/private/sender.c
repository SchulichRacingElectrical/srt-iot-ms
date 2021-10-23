// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis, Jonathan Mulyk

#include "../public/sender.h"
#include "../public/reader.h"
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define TIMEOUT_SECONDS         3
#define TIMEOUT_MICRO_SECONDS   0


void UDPClient(int port, char *IP, UDPServerInfo *serverInfo)
{
    struct sockaddr_in server;
    struct timeval tv;

    int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(sockfd < 0)
    {
        //error
        printf("socket function failed\n");
        close(sockfd);
        exit(1);
    }

    //server structure elements
    memset((char *) &server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(port)

    //IP
    if(inet_pton(AF_INET, IP, &server.sin_addr) == 0)
    {
        //handle error
        printf("inet_pton function failed\n");
        exit(1);
    }

    //set timeout
    tv.tv_sec = TIMEOUT_SECONDS;
    tv.tv_usec = TIMEOUT_MICRO_SECONDS;
    
    //set the socket descriptor to have the timeout
    setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (const char *) &tv, sizeof(tv));

    //store the server info in the serverInfo structure
    serverInfo->sockfd = sockfd;
    serverInfo->server = server;
    serverInfo->serverLen = sizeof(server);
}

//send buffer to the UDP server
//returns the number of bytes sent
int sendData(UDPServerInfo *serverInfo, char *buffer, int buffSize)
{
    int sentBytes = -1;

    //send buffer to the server
	sentBytes = sendto(serverInfo->sockfd, buffer, buffSize, MSG_CONFIRM, (const struct sockaddr *) &serverInfo->server, serverInfo->serverLen);
	if(sentBytes <= 0)
	{
		printf("sendto function failed in %s", __FILE__);	
		exit(1);
	}

    return sentBytes
}

int recvData()
{

}

//might have to change parameters when the actual implementation is added
void sendStruct(struct Sample *sample, const int serverPort, char *serverip){
    int sockfd;
    char buffer[2048] //constant size, change later
    UDPServerInfo serverInfo;

    //clear buffer
    memset(&buffer, '\0', sizeof(buffer));

    //format buffer 
    sprintf(buffer, "%s %s %s", sample->length, sample->sensor_data, sample->sensor_ids);


    close(sockfd);
}
