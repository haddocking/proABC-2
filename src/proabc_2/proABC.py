#!/usr/bin/env python3

#
# Copyright 2019:
#   Francesco Ambrosetti
#   Pier Paolo Olimpieri
#   Tobias Hegelund Olsen
#   Brian Jimenez-Garcia
#

import argparse
import copy
import os

import numpy as np
import pandas as pd

import proabc_2.cnn as cn
import proabc_2.jobinput as ji
import proabc_2.numbering as nb

__author__ = [
    "Francesco Ambrosetti",
    "Pier Paolo Olimpieri",
    "Tobias Hegelund Olsen",
    "Brian Jimenez-Garcia",
]

__email__ = [
    "ambrosetti.francesco@gmail.com",
    "pierpaolo.olimpieri@gmail.com",
    "tobhe@dtu.dk",
    "b.jimenezgarcia@uu.nl",
]


def get_features(
    jobid, hmmpath, light, heavy, ig_database_H, ig_database_K, ig_database_L, log_file
):
    """Calculate features necessary to run proABC 2:
    - Aligned sequences
    - Germlines
    - Canonical structures
    - Loop lengths
    """

    fhLog = log_file

    # Path to executable
    TargetName = jobid.replace("/", "")

    # Check for input in heavy and light fasta
    fhLog.write("Checking input heavy chain sequence\n")
    ji.checkInput(heavy, jobid)

    fhLog.write("Checking input light chain sequence\n")
    ji.checkInput(light, jobid)

    # Write as a single one-line-sequence file
    format_heavy = "heavy_format.fasta"
    format_light = "light_format.fasta"
    ji.oneLiner_fasta(jobid, heavy, format_heavy)
    ji.oneLiner_fasta(jobid, light, format_light)

    # Generate working folders
    if not os.path.exists(os.path.join(jobid, "alignments")):
        os.makedirs(os.path.join(jobid, "alignments"))
    if not os.path.exists(os.path.join(jobid, "tmp")):
        os.makedirs(os.path.join(jobid, "tmp"))

    # Run HMM to get chain isotype
    fhLog.write("HMM Scanning to identify the isotype of the input chains\n")
    myAb = {"input": {"H": "", "L": "", "K": ""}}

    # Chain H
    Seq, isotype = ji.read_input_single(format_heavy, jobid, hmmpath)
    fhLog.write(heavy + " sequence is " + Seq + "\n")
    fhLog.write("Isotype is " + isotype + "\n")

    if isotype:
        myAb["input"][isotype] = Seq

    # Chain L
    Seq, isotype = ji.read_input_single(format_light, jobid, hmmpath)
    fhLog.write(light + " sequence is " + Seq + "\n")
    fhLog.write("Isotype is " + isotype + "\n")

    if isotype:
        myAb["input"][isotype] = Seq

    # Remove tmp file
    ji.rmTmpFile(jobid)
    os.removedirs(os.path.join(jobid, "tmp"))

    # Check if antibody contains both chains
    session = ji.BothChains(myAb, jobid)

    # Calculate germline for the Heavy chain
    fhLog.write("Calculating germline for heavy chain" "\n")
    germfile_H = os.path.join(jobid, "heavy.germ")
    germ_H = ji.get_germline(jobid, ig_database_H, format_heavy, germfile_H)

    for ab in session:

        # Initialize heavy chain class
        numbH = nb.H(session[ab]["H"])

        # Get sequence with H3 aligned
        # GAPs are now between the residues 92 and 104
        numbH.H3align()
        seq_H = numbH.alnH3

        # Calculates canonical structures and loop lengths for chain H
        fhLog.write("Assigning canonical structures to Heavy chain\n")
        cs_H = numbH.getCs()
        loop_H = numbH.loopLen()

        # Initialize light chain class
        fhLog.write("Calculating germline for light chain" "\n")
        germfile_L = os.path.join(jobid, "light.germ")

        if session[ab]["K"]:  # If isotype is K
            isotype = "K"
            germ_L = ji.get_germline(jobid, ig_database_K, format_light, germfile_L)

        elif session[ab]["L"]:  # If isotype is L
            isotype = "L"
            germ_L = ji.get_germline(jobid, ig_database_L, format_light, germfile_L)

        method = eval("nb." + isotype)
        numbL = method(session[ab][isotype])

        # Get Light chain sequence
        seq_L = session[ab][isotype]

        # Calculates canonical structures and loop lengths
        fhLog.write("Assigning canonical structures to Light chain\n")
        cs_L = numbL.getCs()
        loop_L = numbL.loopLen()

        # Write features file
        fhLog.write("Writing feature .csv file\n")
        features = {
            "H_HV1_len": [loop_H[list(loop_H)[0]]],
            "H_HV2_len": [loop_H[list(loop_H)[1]]],
            "H_HV3_len": [loop_H[list(loop_H)[2]]],
            "H_CanHV1": [cs_H[0]],
            "H_CanHV2": [cs_H[1]],
            "H_CanHV3": [cs_H[2]],
            "H_Germline": [germ_H],
            "L_HV1_len": [loop_L[list(loop_L)[0]]],
            "L_HV2_len": [loop_L[list(loop_L)[1]]],
            "L_HV3_len": [loop_L[list(loop_L)[2]]],
            "L_CanHV1": [cs_L[0]],
            "L_CanHV2": [cs_L[1]],
            "L_CanHV3": [cs_L[2]],
            "L_Germline": [germ_L],
            "heavy_seq": [seq_H],
            "light_seq": [seq_L],
        }

        df_features = pd.DataFrame.from_dict(features)
        df_features.to_csv(path_or_buf=jobid + TargetName + "-features.csv")

    return (
        df_features,
        numbH.numbering,
        seq_H,
        numbH.aligned,
        numbL.numbering,
        numbL.aligned,
    )


def reAln_H3(h_pred, h_seq, chothia):
    """It reorders the predictions according
    to the original Chothia alignment"""

    # Build full sequence data-frame
    full_seq = pd.DataFrame([list(h_seq)]).T
    full_seq.index = chothia
    h_pred.index = chothia

    # Extract residues between C 92 and G 104
    h3_stretch = full_seq.iloc[109:144]
    h3_stretch_pred = h_pred[109:144]

    # Clean up
    h3_df = pd.concat([h3_stretch, h3_stretch_pred], axis=1)
    h3_df.columns = ["Sequence", "Prediction"]
    h3_df_ng = h3_df[h3_df["Sequence"] != "-"]  # Remove gaps from the sequence

    # Re-align
    stop = list(h3_df_ng.index).index("101")
    h3_df_ng.index.values[:stop] = h3_stretch.index.values[:stop]

    # Build full prediction list
    # Predicted values are rearranged
    final_h_out = copy.deepcopy(h_pred)
    final_h_out.loc[list(h3_df_ng.index.values), 0] = h3_df_ng["Prediction"]

    # Create output
    re_aligned_pred = list(final_h_out[0])

    return re_aligned_pred


def prediction(input_path, heavy_fasta_file, light_fasta_file):
    """Make the proABC 2 prediction"""
    try:
        # input folder
        jobid = input_path

        # name of the fasta file containing the sequence of the heavy chain
        heavy = heavy_fasta_file

        # name of the fasta file containing the sequence of the light chain
        light = light_fasta_file

        # Calculate absolute paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        # file to encode the sequences
        seq_encoding = os.path.join(base_dir, "data", "Sparse_encoding_v2.txt")
        # igblastp database for heavy Kappa and Light chain
        ig_database_H = os.path.join(base_dir, "database", "IGHVp.fasta")
        ig_database_K = os.path.join(base_dir, "database", "IGKVp.fasta")
        ig_database_L = os.path.join(base_dir, "database", "IGLVp.fasta")

        # only needed if you want to specify the path for HMMER
        hmmpath = ""

        if not jobid.endswith("/"):
            jobid = jobid + "/"

        # Open file log
        open(os.path.join(jobid, "session.log"), "w").close()  # create empty file
        log = open(os.path.join(jobid, "session.log"), "a")

        # Get features, aligned chain sequences with GAPs and the Chothia schemes for both chains
        log.write("Running features calculation\n")
        df, numb_h, aln_H, seq_h, numb_L, aln_L = get_features(
            jobid,
            hmmpath,
            light,
            heavy,
            ig_database_H,
            ig_database_K,
            ig_database_L,
            log,
        )

        # Categorize residue features and encode the sequences
        log.write("Preparing features for predictions\n")
        feat_data = cn.categorize_X_data(df)
        seq_data = cn.encode_X_sequence(
            df.loc[:, ["heavy_seq", "light_seq"]], seq_encoding, add_position=1
        )
        x_data = (seq_data, feat_data)

        # Model
        log.write("Initializing model and making predictions\n")

        # Define model parameters
        output_names = ["pt", "hb", "hy"]  # type of interaction predicted
        split = len(output_names)
        tot = len(seq_data[0] * split)  # 297 [len H chain + len L chain] * split
        hps = {"N_BATCH": 50, "y_out": tot}

        # Prediction
        model_path = os.path.join(base_dir, "data", "proABC_v2")
        y_pred = cn.predict(tot, hps, model_path, x_data)

        log.write("Creating output file\n")

        # Return data-frame - one for chain H and one for chain L
        # chain H
        df_seq_H = pd.DataFrame([numb_h, seq_h], index=["Chothia", "Sequence"]).T
        len_H = df_seq_H.shape[0]

        # chain L
        df_seq_L = pd.DataFrame([numb_L, aln_L], index=["Chothia", "Sequence"]).T

        for i in range(split):

            split_values = np.split(y_pred[0], split)[i]

            # Chain H
            h_values = pd.DataFrame(split_values[:len_H])
            new_h_values = reAln_H3(h_values, aln_H, numb_h)  # retrive original H3 aln
            df_seq_H = pd.concat([df_seq_H, pd.DataFrame(new_h_values)], axis=1)

            # Chain L
            l_values = pd.DataFrame(split_values[len_H:])
            df_seq_L = pd.concat([df_seq_L, l_values], axis=1)

        # define colnames
        cols = ["Chothia", "Sequence"] + output_names

        # chain H
        df_seq_H.columns = cols
        out_h_ng = df_seq_H[
            df_seq_H["Sequence"] != "-"
        ]  # Remove gaps from the sequence
        out_h_ng = out_h_ng.round(2)

        # write final csv file
        out_h_ng.to_csv(path_or_buf=os.path.join(jobid, "heavy-pred.csv"))  # chain H

        # chain L
        df_seq_L.columns = cols
        out_l_ng = df_seq_L[
            df_seq_L["Sequence"] != "-"
        ]  # Remove gaps from the sequence
        out_l_ng = out_l_ng.round(2)

        # write final csv file
        out_l_ng.to_csv(path_or_buf=os.path.join(jobid, "light-pred.csv"))  # chain L

        # Close log file
        log.write("Job completed\n")
        log.close()

    except Exception as err:
        print("ERROR in proABC-2 prediction:")
        print(err)
        raise SystemExit(1)


def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="It predicts the antibody residues that will make contact with the antigen",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing the .fasta files for light and heavy chains",
    )
    parser.add_argument(
        "heavy", help="Name of the fasta file containing the heavy chain"
    )
    parser.add_argument(
        "light", help="Name of the fasta file containing the light chain"
    )

    args = parser.parse_args()

    # Make the prediction
    prediction(args.folder, args.heavy, args.light)


if __name__ == "__main__":
    main()
