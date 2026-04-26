#!/bin/bash

best_score=93.822
best_params="alpha0=12 zcr=3500 sil=110"

for alpha0 in 10 11 12; do
    for zcr in 3000 3200 3500 4000; do
        for sil in 80 100 110 120; do
            for am in 0 10 20 30 40 50; do
                echo "alpha0=$alpha0 zcr=$zcr sil=$sil am=$am"
                for filewav in db.v4/*/*.wav; do
                    filevad=${filewav/.wav/.vad}
                    ./build/vad -0 $alpha0 --zcr=$zcr --min-silence=$sil -i "$filewav" -o "$filevad" 2>/dev/null
                done
                score=$(perl scripts/vad_evaluation.pl db.v4/*/*.lab 2>/dev/null | grep "===> TOTAL" | awk '{print $3}' | sed 's/%//')
                if [ -n "$score" ]; then
                    if (( $(echo "$score > $best_score" | bc -l) )); then
                        best_score=$score
                        best_params="alpha0=$alpha0 zcr=$zcr sil=$sil am=$am"
                        echo "  -> NOU MILLOR: $score%"
                    fi
                fi
            done
        done
    done
done

echo ""
echo "Best: $best_score%"
echo "Params: $best_params"