from __future__ import absolute_import
import allensdk.core.json_utilities as ju
import sys
import os.path
from run_pipeline import run_pipeline
import generate_pipeline_input as gpi
import ipfx.logging_utils as lu

OUTPUT_DIR = "local1\\ephys\\tsts"

INPUT_JSON = "pipeline_input.json"
OUTPUT_JSON = "pipeline_output.json"



def main():
    """
    Runs pipeline from the nwb file
    Usage:
    python pipeline_from_nwb_file.py INPUT_NWB_FILE

    User must specify the OUTPUT_DIR

    """

    input_nwb_file = sys.argv[1]
    input_nwb_file_basename = os.path.basename(input_nwb_file)
    cell_name = os.path.splitext(input_nwb_file_basename)[0]

    cell_dir = os.path.join(OUTPUT_DIR,cell_name)

    if not os.path.exists(cell_dir):
        os.makedirs(cell_dir)

    lu.configure_logger(cell_dir)

    pipe_input = gpi.generate_pipeline_input(cell_dir,
                                             input_nwb_file = input_nwb_file)

    input_json = os.path.join(cell_dir,INPUT_JSON)
    ju.write(input_json,pipe_input)

    #   reading back from disk
    pipe_input = ju.read(input_json)
    pipe_output = run_pipeline(pipe_input["input_nwb_file"],
                          pipe_input.get("input_h5_file", None),
                          pipe_input["output_nwb_file"],
                          pipe_input.get("stimulus_ontology_file", None),
                          pipe_input.get("qc_fig_dir",None),
                          pipe_input["qc_criteria"],
                          pipe_input["manual_sweep_states"])

    ju.write(os.path.join(cell_dir,OUTPUT_JSON), pipe_output)

if __name__ == "__main__": main()



