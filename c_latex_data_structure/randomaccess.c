#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/time.h>
#include <time.h>
#include <limits.h>

long nano_seconds(struct timespec *t_start, struct timespec *t_stop) {
    return (t_stop->tv_nsec- t_start->tv_nsec) + (t_stop->tv_sec- t_start->tv_sec)*1000000000;
}

long random_access_benchmark(int n, int loop) {
    int *array = malloc(n * sizeof(int));
    int *index_array = malloc(loop * sizeof(int));

    for (int i = 0; i < n; i++){
        array[i] = i;
    }
    for (int i = 0; i < loop; i++){
        index_array[i] = rand() % n;
    }

    struct timespec t_start, t_stop;
    int sum = 0;

    clock_gettime(CLOCK_MONOTONIC, &t_start);
    for (int i = 0; i < loop; i++){
        sum += array[index_array[i]];
    }
    clock_gettime(CLOCK_MONOTONIC, &t_stop);

    free(array);
    free(index_array);
    
    // Force compiler to not let sum variable and its operation be treated as dead code
    if (sum == 0){
        return 0;
    }
    return nano_seconds(&t_start, &t_stop);
}

long search_benchmark(int n, int loop) {
    int *array = (int*) malloc(n*sizeof(int));
    for (int i = 0; i < n; i++)
        array[i] = rand()%(n*2);
    
    int *keys = (int*) malloc(loop*sizeof(int));
    for (int i = 0; i < loop; i++)
        keys[i] = rand()%(n*2);
    
    struct timespec t_start, t_stop;
    int sum = 0;
    clock_gettime(CLOCK_MONOTONIC, &t_start);
    for (int i = 0; i < loop; i++) {
        int key = keys[i];
        for (int j = 0; j < n; j++) {
            if (key == array[j]) {
                sum++;
                break;
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t_stop);
    
    free(array);
    free(keys);
    
    long elapsed_time = nano_seconds(&t_start, &t_stop);
    return elapsed_time;
}

// loop param is not used, kept due to parameter uniformity
long duplicates_benchmark(int n, int loop) { 
    int *array = (int*) malloc(n*sizeof(int));
    for (int i = 0; i < n; i++)
        array[i] = rand()%(n*2);
    
    int sum = 0;
    struct timespec t_start, t_stop;
    
    clock_gettime(CLOCK_MONOTONIC, &t_start);
    for (int i = 0; i < n; i++) {
        int key = array[i];
        for (int j = i+1; j < n; j++) {
            if (key == array[j]) {
                sum++;
                break;
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &t_stop);
    
    free(array);
    
    long wall = nano_seconds(&t_start, &t_stop);
    return wall;
}

int main(int argc, char *argv[]) {
    srand(time(NULL));
    int SIZE_LENGTH = 8;
    int sizes[] = {1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072};
    int trials = 16;
    int loop = 1024;
    for (int i = 0; i < SIZE_LENGTH; i++) {
        int size = sizes[i];
        long min = LONG_MAX;
        long max = 0;
        long total = 0;
        
        printf("--- BENCHMARK MEASUREMENTS (%d, %d SIZE) ---\n", i, size);
        for (int j = 0; j < trials; j++) {
            long elapsed_time = search_benchmark(size, loop);
            if (elapsed_time < min){
                min = elapsed_time;
            }
            if (elapsed_time > max){
                max = elapsed_time;
            }
            total += elapsed_time;
            printf("ELAPSED TIME: TOTAL: %ld ns, AVG PER LOOP: %0.2f ns\n", elapsed_time, (double) elapsed_time/loop);
        }
        printf("\n");
    
        printf("--- BENCHMARK SUMMARY (%d) ---\n", i);
        printf("MAX TIME: %.2f ns/operation \n", (double)max/loop);
        printf("MIN TIME: %.2f ns/operation \n", (double)min/loop);
        printf("AVG TIME: %.2f ns/operation \n", (((double)total)/loop)/trials);
        printf("TOT TIME: %.2f ns/operation \n", (((double)total)/loop));
        printf("\n\n");
    }
    return 0;
}