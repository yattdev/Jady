for i in intents/*.txt; do
    python -m chatette $i
    cp output/train/output.json ../jady/data/
done
