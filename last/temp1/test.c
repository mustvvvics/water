#include <stdio.h>

//apt-get install libusb-1.0-0-dev
//gcc -o test test.c -L./ -ltemp -lusb-1.0

int main() {
	int ret;
	double v, v2;
	ret = tempdev_open();
	if(ret)
	{
		if(ret == 1)
			printf("Init Error\n");
		else if(ret == 2)
			printf("Cannot open device\n");
		else if(ret == 3)
			printf("Cannot Claim Interface\n");
		else
			printf("OpenErr: %d\n", ret);
		return 0;
	}
	while(1)
	{
		ret = tempdev_get(&v);
		if(ret != 0)
			break;
		printf("Temp: %.1f\n", v);
	}
	tempdev_close();
	return 0;
}
