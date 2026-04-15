#!/bin/bash
# Script per fer barrido de paràmetres i trobar l'òptim

DB_DIR="db.v4"
VAD="./bin/vad"
EVAL="./scripts/vad_evaluation.pl"
TEMP_DIR="/tmp/vad_sweep"
RESULTS="sweep_results.txt"

mkdir -p "$TEMP_DIR"

# Valors a probar
ALPHA_VALS="8 10 12 14 14.4 16 18 20"
ZCR_VALS="500 1000 1500 2000 2500"
HYST_VALS="10 15 20 25 30 35 40"

echo "Barrido de paràmetres VAD"
echo "========================="
echo "Data: $(date)" > "$RESULTS"
echo "" >> "$RESULTS"

BEST_SCORE=0
BEST_PARAMS=""

count=0
total=$(echo "$ALPHA_VALS $ZCR_VALS $HYST_VALS" | wc -w)

for alpha in $ALPHA_VALS; do
    for zcr in $ZCR_VALS; do
        for hyst in $HYST_VALS; do
            count=$((count + 1))
            echo "[$count] alpha=$alpha zcr=$zcr hyst=$hyst"
            
            # Processar cada fitxer de la base de dades
            for folder in $DB_DIR/*/; do
                for wav in "$folder"*.wav; do
                    [ -f "$wav" ] || continue
                    base=$(basename "$wav" .wav)
                    dir=$(dirname "$wav")
                    
                    # Executar VAD
                    $VAD -i "$wav" -o "$TEMP_DIR/${base}.vad" -0 "$alpha" -z "$zcr" -n "$hyst" 2>/dev/null
                    
                    # Copiar .lab de referencia
                    cp "$dir/${base}.lab" "$TEMP_DIR/${base}.lab" 2>/dev/null
                done
            done
            
            # Avaluar
            SCORE=$($EVAL $TEMP_DIR/*.lab 2>/dev/null | grep "===>" | head -1 | awk '{print $3}')
            SCORE_NUM=$(echo "$SCORE" | tr -d '%')
            
            if [ ! -z "$SCORE_NUM" ]; then
                echo "  TOTAL: $SCORE"
                echo "alpha=$alpha zcr=$zcr hyst=$hyst -> $SCORE" >> "$RESULTS"
                
                # Comparar amb el millor
                IS_BETTER=$(echo "$SCORE_NUM > $BEST_SCORE" | bc -l 2>/dev/null)
                if [ "$IS_BETTER" = "1" ]; then
                    BEST_SCORE=$SCORE_NUM
                    BEST_PARAMS="alpha=$alpha zcr=$zcr hyst=$hyst"
                fi
            fi
            
            # Netejar
            rm -f "$TEMP_DIR"/*.lab "$TEMP_DIR"/*.vad
        done
    done
done

echo ""
echo "========================="
echo "MILLOR RESULTAT: $BEST_PARAMS -> $BEST_SCORE%"
echo "========================="
echo ""
echo "Resultats complets a: $RESULTS"
