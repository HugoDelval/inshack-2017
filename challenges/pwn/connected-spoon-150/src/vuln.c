int main(int argc,char * argv[])
{
        char buffer[2000];

        if(argc<2)
		return -1;

        strcpy(buffer,argv[1]);
        printf("Hello %s !\n", buffer);


        return 0;
}
