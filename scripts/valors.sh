#!/bin/bash

echo "Fine-tuning around best params..."
echo "=========================================="

best_score=93.640
best_params="alpha0=13.9 zcr=3200 sil=130"

for alpha0 in 12 13 13.5 13.9 14.5 15; do
    for zcr in 2800 3000 3100 3200 3300 3400 3500; do
        for sil in 110 120 130 140 150; do
            echo "Testing alpha0=$alpha0 zcr=$zcr sil=$sil"
            
            for filewav in db.v4/*/*.wav; do
                filevad=${filewav/.wav/.vad}
                ./bin/vad -0 $alpha0 --zcr=$zcr --min-silence=$sil -i "$filewav" -o "$filevad" > /dev/null 2>&1
            done
            
            score=$(perl scripts/vad_evaluation.pl db.v4/*/*.lab 2>/dev/null | grep "===> TOTAL" | awk '{print $3}' | sed 's/%//')
            
            if [ -n "$score" ]; then
                echo "  => Score: $score%"
                if (( $(echo "$score > $best_score" | bc -l) )); then
                    best_score=$score
                    best_params="alpha0=$alpha0 zcr=$zcr sil=$sil"
                fi
            fi
        done
    done
done

echo ""
echo "=========================================="
echo "Best score: $best_score%"
echo "Best params: $best_params"