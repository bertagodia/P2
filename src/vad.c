#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#include "pav_analysis.h"
#include "vad.h"
#include "pav_analysis.h"

const float FRAME_TIME = 10.0F; /* in ms. */

/*
* As the output state is only ST_VOICE, ST_SILENCE, or ST_UNDEF,
* only this labels are needed. You need to add all labels, in case
* you want to print the internal state in string format
*/

const char *state_str[] = {
 "UNDEF", "S", "V", "INIT"
};

const char *state2str(VAD_STATE st) {
 return state_str[st];
}

/* Define a datatype with interesting features */
typedef struct {
 float zcr;
 float p;
 float am;
} Features;

/*
* TODO: Delete and use your own features!
*/


Features compute_features(const float *x, int N, float fm) {
 /*
  * Input: x[i] : i=0 .... N-1
  * Ouput: computed features
  */
 /*
  * DELETE and include a call to your own functions
  *
  * For the moment, compute random value between 0 and 1
  */
 Features feat;
 //feat.zcr = feat.p = feat.am = (float) rand()/RAND_MAX;
 feat.p = compute_power(x, N);
 feat.am = compute_am(x, N);
 feat.zcr = compute_zcr(x, N, 16000.0); //porque sabemos la frecuencia a la que se muestrea el audio, de 16KHz
 return feat;
}

/*
* TODO: Init the values of vad_data
*/

VAD_DATA * vad_open(float rate) {
 VAD_DATA *vad_data = malloc(sizeof(VAD_DATA));
 vad_data->state = ST_INIT;
 vad_data->sampling_rate = rate;
 vad_data->frame_length = rate * FRAME_TIME * 1e-3;
 return vad_data;
}

VAD_STATE vad_close(VAD_DATA *vad_data) {
 /*
  * TODO: decide what to do with the last undecided frames
  */
 VAD_STATE state = vad_data->state;


 free(vad_data);
 return state;
}

unsigned int vad_frame_size(VAD_DATA *vad_data) {
 return vad_data->frame_length;
}

/*
* TODO: Implement the Voice Activity Detection
* using a Finite State Automata
*/

VAD_STATE vad(VAD_DATA *vad_data, float *x, float alpha0) {

 /*
  * TODO: You can change this, using your own features,
  * program finite state automaton, define conditions, etc.
  */


 Features f = compute_features(x, vad_data->frame_length, vad_data->sampling_rate);
 vad_data->last_feature = f.p; /* save feature, in case you want to show */




float umbral_potencia = vad_data->llindar_0;
float umbral_zcr = 2000.0; // Ajusta según tus pruebas en WaveSurfer


 switch (vad_data->state) {
 case ST_INIT:
   vad_data->state = ST_SILENCE;
   // El silencio inicial sirve para calibrar el umbral
   vad_data->llindar_0 = f.p+alpha0;
   vad_data->counter = 0;
   break;


 case ST_SILENCE:
 // Condición de entrada a VOZ: Mucha potencia O potencia media con mucho ZCR (fricativas)
   if (f.p > umbral_potencia || (f.p > umbral_potencia - 10 && f.zcr > umbral_zcr))
     vad_data->state = ST_VOICE;
     vad_data->counter = 0;
   break;


 case ST_VOICE:
 // Condición de salida a SILENCIO: Solo si la potencia es baja
   if (f.p < umbral_potencia) {
       vad_data->counter++;
       //HISTERESIS: Solo cambiamos a silencio si llevamos 15 tramas (150ms) de nivel bajo
       if (vad_data->counter > 15) {
           vad_data->state = ST_SILENCE;
           vad_data->counter = 0;
       }
   } else {
       vad_data->counter = 0; // Si vuelve la potencia, reseteamos el contador
   }
   break;


 case ST_UNDEF:
   break;
 }


 if (vad_data->state == ST_SILENCE ||
     vad_data->state == ST_VOICE)
   return vad_data->state;
 else
   return ST_UNDEF;
}

void vad_show_state(const VAD_DATA *vad_data, FILE *out) {
 fprintf(out, "%d\t%f\n", vad_data->state, vad_data->last_feature);}
