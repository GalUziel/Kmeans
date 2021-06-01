/* This module executes the calculation of the kmeans algorithm from a given array of clusters */

#include "getMeans.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

struct cluster{
    float *sum;
    int size;
};

static void init_clusters(struct cluster * clusters, int k, int d);
static int find_minimum(const float *p, int k);
static int is_equal(float **p1, float **p2, int k, int d);
static void copy_array(float **p1, float **p2, int k, int d);
struct cluster;
static void reset_clusters(struct cluster* s_array,int k,int d);
static float euc_dis(const float *p1,const float *p2,const int d);
static void add_obs_to_cluster(float *curr_obs,struct cluster s,int d);
static void update_cent(float **curr_cent, struct cluster* clusters, int k, int d);


int* getMeans(int k, int n, int d, int MAX_ITER, float** curr_cent, float** observations) {
    struct cluster * clusters;
    float **prev_cent;
    int *clusterIndex;
    int i;
    int j;
    int counter;
      
    /* malloc arrays */
    clusters=(struct cluster*)malloc(k* sizeof(struct cluster));
    if (clusters == NULL){
        printf("Failed to allocate memory\n");
        exit(1);
    }   
    /* malloc inside arrays */

    prev_cent = (float **) malloc(k  * sizeof(float *));
    if (prev_cent == NULL){
        printf("Failed to allocate memory\n");
        exit(1);
    }
    /* malloc inside arrays */
    for (i = 0; i < k; i++) {
        prev_cent[i] = (float *) malloc(d * sizeof(float));
        if (prev_cent[i] == NULL){
            printf("Failed to allocate memory\n");
            exit(1);
        }
        for (j = 0; j < d; j++){
            prev_cent[i][j] = 0;
        }
    }

    init_clusters(clusters, k, d);
    counter = 0;
    float *dist = (float *)calloc(k, sizeof(float));
    int a, b;
    /* repeat until: */
    while (counter < MAX_ITER && !is_equal(prev_cent, curr_cent, k, d)) {
        copy_array(prev_cent, curr_cent, k, d);
        reset_clusters(clusters,k,d);
        for (a = 0; a < n; a++) {
            int index;
            float *curr_obs = observations[a];

            for (b = 0; b < k; b++) {
                dist[b] = euc_dis(curr_obs, prev_cent[b], d);
            }
            index = find_minimum(dist, k);
            add_obs_to_cluster(curr_obs,clusters[index],d);
            clusters[index].size++;

        }
        update_cent(curr_cent,clusters,k,d);
        counter++;

    }
    clusterIndex =(int*)malloc(n * sizeof(int));
    for (a = 0; a < n; a++) {
            float *curr_obs = observations[a];
            for (b = 0; b < k; b++) {
                dist[b] = euc_dis(curr_obs, curr_cent[b], d);
            }
            clusterIndex[a] = find_minimum(dist, k);
    }


    /* Free the memory used */
    for (i = 0; i < n; i++) {
        free(observations[i]);
        observations[i] = NULL;
    }
    free(observations);
    observations = NULL;

    for (i = 0; i < k; i++) {
        free(prev_cent[i]);
        free(curr_cent[i]);
        prev_cent[i] = NULL;
        curr_cent[i] = NULL;

    }
    free(prev_cent);
    free(curr_cent);
    prev_cent = NULL;
    curr_cent = NULL;

    for (j=0;j<k; j++){
        free(clusters[j].sum);
        clusters[j].sum = NULL;
    }
    free(clusters);
    clusters = NULL;

    free(dist);
    dist = NULL;
    return clusterIndex;
}

/* return the index of the min value in array*/
static int find_minimum(const float *p, int k) {
    int c, index;
    float min;
    index = 0;
    min = p[0];
    for(c=0;c<k;c++){
        if (p[c] < min){
            index = c;
            min = p[c];
        }
    }
    return index;


}

/* checking if 2- array are equal*/
static int is_equal(float **p1, float **p2, int k, int d){
    int i,j;
    for (j=0;j<k; j++){
        for (i=0;i<d;i++){
            if (fabs(p1[j][i] - p2[j][i]) > 0.0001)
                return 0;
        }
    }
    return 1;
}

/*copy the second array to the first one */
static void copy_array(float **p1, float **p2, int k, int d){
    int i,j;
    for (j=0;j<k; j++){
        for (i = 0; i < d; i++) {
            p1[j][i] = p2[j][i];
        }
    }
}

/* reset clusters sum and size */
static void reset_clusters(struct cluster* s_array,int k,int d ){
    int i,j;
    for (j=0;j<k; j++){
        s_array[j].size=0;
        for (i=0;i<d; i++) {
            s_array[j].sum[i] = 0;
        }
    }
}

/* calculate the distance between 2 vectors */
static float euc_dis(const float *p1, const float *p2,const int d){
    float distance;
    int i;
    distance = 0;
    for (i =0; i< d; i++){
        distance += (p1[i]- p2[i])*(p1[i]- p2[i]);
    }
    return distance;
}

/* add the curr observation to the min cluster- update size and sum */
static void add_obs_to_cluster(float *curr_obs,struct cluster s,int d){
    int i;
    for (i=0;i<d; i++){
        s.sum[i] += curr_obs[i];
    }
}
/* update new centroids */
static void update_cent(float **curr_cent, struct cluster* clusters, int k, int d){
    int i,j;
    for(i=0; i<k; i++){
        for (j=0;j<d;j++){
            curr_cent[i][j] = clusters[i].sum[j]/ (float)clusters[i].size;
        }
    }
}

static void init_clusters(struct cluster * clusters, int k, int d){
    int i,j;
    for (j=0;j<k; j++){
        struct cluster c;
        c.size=0;
        c.sum = (float *) malloc(d * sizeof(float));
        if (c.sum == NULL){
            printf("Failed to allocate memory\n");
            exit(1);
        }        for (i=0;i<d; i++) {
            c.sum[i] = 0;
        }
        clusters[j]= c;
    }
}