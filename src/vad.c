#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#include "pav_analysis.h"
#include "vad.h"
#include "pav_analysis.h"

const float FRAME_TIME = 10.0F;

const char *state_str[] = {
 "UNDEF", "S", "V", "INIT"
};

const char *state2str(VAD_STATE st) {
 return state_str[st];
}

typedef struct {
 float zcr;
 float p;
 float am;
} Features;

Features compute_features(const float *x, int N, float fm) {
 Features feat;
 feat.p = compute_power(x, N);
 feat.am = compute_am(x, N);
 feat.zcr = compute_zcr(x, N, fm);
 return feat;
}

VAD_DATA * vad_open(float rate) {
 VAD_DATA *vad_data = malloc(sizeof(VAD_DATA));
 vad_data->state = ST_INIT;
 vad_data->sampling_rate = rate;
 vad_data->frametime = 10.0F;
 vad_data->frame_length = rate * vad_data->frametime * 1e-3;
 vad_data->counter = 0;
 return vad_data;
}

VAD_STATE vad_close(VAD_DATA *vad_data) {
 VAD_STATE state = vad_data->state;
 free(vad_data);
 return state;
}

unsigned int vad_frame_size(VAD_DATA *vad_data) {
 return vad_data->frame_length;
}

VAD_STATE vad(VAD_DATA *vad_data, float *x) {
  Features f = compute_features(x, vad_data->frame_length, vad_data->sampling_rate);
  vad_data->last_feature = f.p;

  float umbral_potencia = vad_data->llindar_0;
  float umbral_zcr = vad_data->umbral_zcr;

  switch (vad_data->state) {
  case ST_INIT:
      vad_data->state = ST_SILENCE;
      vad_data->llindar_0 = f.p + vad_data->llindar_0;
      vad_data->counter = 0;    
    break;

  case ST_SILENCE:
    if (f.p > umbral_potencia || (f.p > umbral_potencia - 10.0f && f.zcr > umbral_zcr)) {
        vad_data->state = ST_VOICE;
        vad_data->counter = 0;
    }
    break;

  case ST_VOICE:
    if (f.p < umbral_potencia) {
      vad_data->counter++;
      if (vad_data->counter > (vad_data->min_silence_ms / vad_data->frametime)) {
        vad_data->state = ST_SILENCE;
        vad_data->counter = 0;
      }
    } else {
      vad_data->counter = 0;
    }
    break;

  case ST_UNDEF:
    break;
  }
  if (vad_data->state == ST_SILENCE || vad_data->state == ST_VOICE)
    return vad_data->state;
  else
    return ST_UNDEF;
}

void vad_show_state(const VAD_DATA *vad_data, FILE *out) {
 fprintf(out, "%d\t%f\n", vad_data->state, vad_data->last_feature);}