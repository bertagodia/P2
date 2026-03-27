#include <math.h>
#include "pav_analysis.h"

float compute_power(const float *x, unsigned int N) {
    float sum = 1e-12;
    for (unsigned int n = 0; n < N; n++) {
        sum += x[n] * x[n];
    }
    return 10 * log10f(sum / N);
}

float compute_am(const float *x, unsigned int N) {
    float sum = 0.0f;
    for (unsigned int n = 0; n < N; n++) {
        sum += fabsf(x[n]);
    }
    return sum / N;
}

float compute_zcr(const float *x, unsigned int N, float fm) {
    unsigned int crossings = 0;
    for (unsigned int n = 1; n < N; n++) {
        if ((x[n] >= 0 && x[n-1] < 0) || (x[n] < 0 && x[n-1] >= 0)) {
            crossings++;
        }
    }
    return (float) crossings * fm / (2 * (N-1));
}
