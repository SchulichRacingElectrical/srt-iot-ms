// Copyright Schulich Racing FSAE
// Written by Justin Tijunelis, Jonathan Mulyk

#include "../public/sender.h"
#include "../public/reader.h"
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>


#define TIMEOUT_SECONDS         3
#define TIMEOUT_MICRO_SECONDS   0
#define MAX_BUFF_SIZE           2048

//Start a UDP client
void UDPClient(UDPServerInfo *serverInfo, int port, char *IP)
{
    struct sockaddr_in server;
    struct timeval tv;

    int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(sockfd < 0)
    {
        //error
        printf("socket function failed\n");
        close(sockfd);
        return;
    }

    //server structure elements
    memset((char *) &server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(port);

    //IP
    if(inet_pton(AF_INET, IP, &server.sin_addr) == 0)
    {
        //handle error
        printf("inet_pton function failed\n");
        return;
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
		return -1;
	}

    return sentBytes;
}

//receive data from UDP server
//returns the number of bytes receives
// -- might be obsolete if the UDP client never needs to receive data
int recvData(UDPServerInfo *serverInfo, char *buffer, int buffSize)
{
    int recBytes = -1;
	//receive the response from the micro-service
	recBytes = recvfrom(serverInfo->sockfd, buffer, buffSize, MSG_CONFIRM, (struct sockaddr *) &serverInfo->server, &serverInfo->serverLen);
    if(recBytes <= 0)
    {
        printf("recvfrom function failed in %s", __FILE__);
        return -1;
    }
	//microBuffer[recBytes] = '\0';
    //apend null terminator on the end on the buffer
	//recBytes++;
    return recBytes;
}

//might have to change parameters when the actual implementation is added
void sendStruct(struct Sample *sample, int serverPort, char *serverIP){

    char buffer[MAX_BUFF_SIZE];
    UDPServerInfo serverInfo;

    #if 0//[ Test information for the sample structure
    sample->length = ""; 
    sample->sensor_data = "";
    sample->sensor_ids = "";

    #endif//]

    UDPClient(&serverInfo, serverPort, serverIP);

    //clear buffer
    memset(&buffer, '\0', sizeof(buffer));

    //format buffer 
    sprintf(buffer, "%d%s%s", sample->length, sample->sensor_data, sample->sensor_ids);

    //send the buffer to the UDP server
    sendData(&serverInfo, buffer, strlen(buffer));


    close(serverInfo.sockfd);
}
