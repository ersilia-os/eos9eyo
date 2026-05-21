import csv
import os
import sys

from ersilia_pack_utils.core import read_smiles, write_out
from lazyqsar.api.classifier_predict import predict

import consensus

input_file  = sys.argv[1]
output_file = sys.argv[2]
root        = os.path.dirname(os.path.abspath(__file__))
checkpoints = os.path.abspath(os.path.join(root, "..", "..", "checkpoints"))

# Sub-model order: every row of run_columns.csv except the leading consensus_score.
columns_file = os.path.abspath(os.path.join(root, "..", "columns", "run_columns.csv"))
with open(columns_file) as f:
    MODEL_NAMES = [row["name"] for row in csv.DictReader(f) if row["name"] != "consensus_score"]
model_dir_dict = {m: os.path.join(checkpoints, "models", m) for m in MODEL_NAMES}

_, smiles_list = read_smiles(input_file)
R, cols_ordered = predict(model_dir_dict, smiles=smiles_list, predict_type="rank")
results, header = consensus.compute_consensus(R, cols_ordered, MODEL_NAMES, checkpoints)
write_out(results, header, output_file)
