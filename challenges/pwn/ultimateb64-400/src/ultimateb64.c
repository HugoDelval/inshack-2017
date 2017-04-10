#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include "b64.h"


#define SIZE_BUF 512

void m_exit(int s)
{
  _exit(s);
}

void banner()
{
	printf("|******************************************************|\n");
	printf("|*************| Ultimate base64 decoder |**************|\n");
	printf("|******************************************************|\n");
	printf("|******************************************************|\n");
        printf("|**| Another |*|Crappy Tools Foundation|*| creation |**|\n");
	printf("|******************************************************|\n");
	printf("\n");
}

int main(int argc, char **argv)
{
        signal(SIGALRM, m_exit);
        alarm(30);
	banner();
	char outputbuf[SIZE_BUF];
	char input[SIZE_BUF] = {0};

	while(1)
	{
		puts("b64> ");
		fflush(stdout);
		fgets(input, SIZE_BUF-1, stdin);
		if(!strcmp(input,"exit\n")) break;
		size_t *decsize = malloc(sizeof(size_t));
		char *output = b64_decode(input, strlen(input), decsize);
		int i;
		//printf("%lu\n", *decsize);
		for(i=0;i<SIZE_BUF && i<*decsize;i++) outputbuf[i] = *output++;
		outputbuf[i] = 0;
		puts("out> ");
		printf(outputbuf);
		puts("\n");
		memset(input, 0, sizeof(input));
		memset(outputbuf, 0, sizeof(outputbuf));
	}

        return 0;

}
