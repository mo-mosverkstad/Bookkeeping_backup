#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/time.h>
#include <time.h>
long nano_seconds(struct timespec *t_start, struct timespec *t_stop) {
    return (t_stop->tv_nsec- t_start->tv_nsec) + (t_stop->tv_sec- t_start->tv_sec)*1000000000;
}


int main() {
    struct timespec t_start, t_stop;
    int given[] = {1,2,3,4,5,6,7,8,9,0};
    int sum = 0;
    for(int i = 0; i < 10; i++) {
        clock_gettime(CLOCK_MONOTONIC, &t_start);
        sum += given[i];
        clock_gettime(CLOCK_MONOTONIC, &t_stop);
        long wall = nano_seconds(&t_start, &t_stop);
        printf("one operation in %ld ns\n", wall);
    }
}