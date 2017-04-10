#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
	char buf[256];
        strcpy(buf,argv[1]);
        printf("Input:%s\n",buf);
	return 0;
}
