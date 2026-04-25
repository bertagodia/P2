#!/bin/bash
# Script per executar VAD amb diferents paràmetres

# Valors per defecte
ALPHA0=${1:-14.4}
ZCR=${2:-2000}
HYSTERESIS=${3:-15}

# Fitxers
INPUT="PAV_2121.wav"
OUTPUT="output.txt"

echo "Executant VAD amb:"
echo "  alpha0 = $ALPHA0"
echo "  zcr = $ZCR"
echo "  hysteresis = $HYSTERESIS"
echo ""

./bin/vad -i "$INPUT" -o "$OUTPUT" -0 "$ALPHA0" -z "$ZCR" -n "$HYSTERESIS"

echo ""
echo "Resultat guardat a: $OUTPUT"
