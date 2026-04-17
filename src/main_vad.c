#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sndfile.h>
#include <string.h>

#include "vad.h"
#include "vad_docopt.h"

#define DEBUG_VAD 0x1

int main(int argc, char *argv[]) {
  int verbose = 0; /* To show internal state of vad: verbose = DEBUG_VAD; */

  SNDFILE *sndfile_in, *sndfile_out = NULL;
  SF_INFO sf_info;
  FILE *vadfile;
  int n_read = 0, i;

  VAD_DATA *vad_data;
  VAD_STATE state, last_state;

  float *buffer, *buffer_zeros;
  int frame_size;         /* in samples */
  float frame_duration;   /* in seconds */
  unsigned int t, last_t; /* in frames */

  char *input_wav, *output_vad, *output_wav;

  DocoptArgs args = docopt(argc, argv, /* help */ 1, /* version */ "2.0");

  verbose    = args.verbose ? DEBUG_VAD : 0;
  input_wav  = args.input_wav;
  output_vad = args.output_vad;
  output_wav = args.output_wav;
  
  float alpha0 = atof(args.alpha0);
  float zcr = atof(args.zcr);
  int hysteresis = atoi(args.hysteresis);
  float min_speech = atof(args.min_speech);
  float min_silence = atof(args.min_silence);

  if (input_wav == NULL || output_vad == NULL) {
    fprintf(stderr, "%s\n", args.usage_pattern);
    return -1;
  }

  /* Open input sound file */
  memset(&sf_info, 0, sizeof(sf_info));
  if ((sndfile_in = sf_open(input_wav, SFM_READ, &sf_info)) == NULL) {
    fprintf(stderr, "Error opening input file %s (%s)\n", input_wav, strerror(errno));
    return -1;
  }

  if (sf_info.channels != 1) {
    fprintf(stderr, "Error: the input file has to be mono: %s\n", input_wav);
    sf_close(sndfile_in);
    return -2;
  }

  /* Open vad file (text file with segments) */
  if ((vadfile = fopen(output_vad, "wt")) == NULL) {
    fprintf(stderr, "Error opening output vad file %s (%s)\n", output_vad, strerror(errno));
    sf_close(sndfile_in);
    return -1;
  }

  /* Open output sound file, with same format, channels, etc. than input */
  if (output_wav) {
    if ((sndfile_out = sf_open(output_wav, SFM_WRITE, &sf_info)) == NULL) {
      fprintf(stderr, "Error opening output wav file %s (%s)\n", output_wav, strerror(errno));
      sf_close(sndfile_in);
      fclose(vadfile);
      return -1;
    }
  }

  /* Initialize VAD */
  vad_data = vad_open(sf_info.samplerate);
  vad_data->llindar_0 = alpha0;
  vad_data->umbral_zcr = zcr;
  vad_data->hysteresis = hysteresis;
  vad_data->min_speech_ms = min_speech;
  vad_data->min_silence_ms = min_silence;

  /* Allocate memory for buffers */
  frame_size   = vad_frame_size(vad_data);
  buffer       = (float *) malloc(frame_size * sizeof(float));
  buffer_zeros = (float *) malloc(frame_size * sizeof(float));
  for (i=0; i < frame_size; ++i) buffer_zeros[i] = 0.0F;

  frame_duration = (float) frame_size / (float) sf_info.samplerate;
  last_state = ST_UNDEF;

  /* Bucle principal de processament */
  for (t = last_t = 0; ; t++) { 
    /* Llegim trama d'àudio */
    n_read = sf_read_float(sndfile_in, buffer, frame_size);
    if (n_read != frame_size) break;

    /* Detectem si la trama és veu o silenci */
    state = vad(vad_data, buffer);
    
    if (verbose & DEBUG_VAD) vad_show_state(vad_data, stdout);

    /* ESCRIURE ÀUDIO: Aquí és on es produeix la "cancel·lació" */
    if (sndfile_out != NULL) {
      if (state == ST_SILENCE) {
        /* Si és silenci, escrivim el buffer ple de zeros */
        sf_write_float(sndfile_out, buffer_zeros, n_read);
      } else {
        /* Si és veu, escrivim l'àudio original */
        sf_write_float(sndfile_out, buffer, n_read);
      }
    }

    /* Guardem els canvis d'estat al fitxer .vad */
    if (state != last_state) {
      if (t != last_t)
        fprintf(vadfile, "%.5f\t%.5f\t%s\n", last_t * frame_duration, t * frame_duration, state2str(last_state));
      last_state = state;
      last_t = t;
    }
  }

  /* Tanquem l'últim segment */
  state = vad_close(vad_data);
  if (t != last_t) {
    fprintf(vadfile, "%.5f\t%.5f\t%s\n", last_t * frame_duration, t * frame_duration + n_read / (float) sf_info.samplerate, state2str(state));
  }

  /* Neteja final */
  free(buffer);
  free(buffer_zeros);
  sf_close(sndfile_in);
  fclose(vadfile);
  if (sndfile_out) sf_close(sndfile_out);
  
  return 0;
}