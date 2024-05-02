import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Conv1D, Dense, Dropout, Flatten, MaxPooling1D

"""Data processing"""


def valid_X_categories():
    """Hardcoding of the features which the network will account for.

    If a data record has a feature which is not in the valid_cat,
    it is trained as if it did not have an input for that feature.
    """

    valid_cat = {
        "H_Germline": np.array(
            [
                "IGHV1-Homo",
                "IGHV1-Mus",
                "IGHV1-Oryctolagus",
                "IGHV1-Rattus",
                "IGHV2-Homo",
                "IGHV2-Mus",
                "IGHV2-Rattus",
                "IGHV3-Canis",
                "IGHV3-Homo",
                "IGHV3-Mus",
                "IGHV3-Rattus",
                "IGHV4-Homo",
                "IGHV4-Mus",
                "IGHV5-Homo",
                "IGHV5-Mus",
                "IGHV5-Rattus",
                "IGHV6-Homo",
                "IGHV6-Mus",
                "IGHV6-Rattus",
                "IGHV7-Homo",
                "IGHV7-Mus",
                "IGHV8-Mus",
                "IGHV9-Mus",
                "IGHV10-Mus",
                "IGHV10-Rattus",
                "IGHV12-Mus",
                "IGHV14-Mus",
            ]
        ),
        "L_Germline": np.array(
            [
                "IGKV1-Homo",
                "IGKV1-Mus",
                "IGKV1-Oryctolagus",
                "IGKV2-Homo",
                "IGKV2-Mus",
                "IGKV2-Rattus",
                "IGKV3-Homo",
                "IGKV3-Mus",
                "IGKV3-Rattus",
                "IGKV4-Homo",
                "IGKV4-Mus",
                "IGKV5-Mus",
                "IGKV6-Homo",
                "IGKV6-Mus",
                "IGKV6-Rattus",
                "IGKV7-Homo",
                "IGKV8-Mus",
                "IGKV8-Rattus",
                "IGKV9-Mus",
                "IGKV10-Mus",
                "IGKV11-Mus",
                "IGKV12-Mus",
                "IGKV12-Rattus",
                "IGKV13-Mus",
                "IGKV14-Mus",
                "IGKV15-Mus",
                "IGKV16-Mus",
                "IGKV17-Mus",
                "IGKV19-Mus",
                "IGKV19-Rattus",
                "IGKV22-Rattus",
                "IGLV1-Canis",
                "IGLV1-Homo",
                "IGLV1-Mus",
                "IGLV2-Homo",
                "IGLV3-Homo",
                "IGLV3-Mus",
                "IGLV3-Oryctolagus",
                "IGLV3-Rattus",
                "IGLV4-Homo",
                "IGLV4-Rattus",
                "IGLV5-Homo",
                "IGLV6-Homo",
                "IGLV8-Canis",
            ]
        ),
        "H_CanHV1": np.array(["1", "2", "3", "O"]),
        "H_CanHV2": np.array(["1", "2", "3", "4", "O"]),
        "H_CanHV3": np.array(["bulged", "non-bulged", "short"]),
        "L_CanHV1": np.array(["1", "2", "3", "4", "5", "6", "7", "8", "O"]),
        "L_CanHV2": np.array(["1", "2", "O"]),
        "L_CanHV3": np.array(["1", "2", "3", "4", "5", "6", "7", "8", "O"]),
    }

    return valid_cat


def categorize_X_data(a_df):
    """Categorizes the data into valid categories (valid_cats) which are ready as input into a network."""
    tmp_data = a_df.copy()
    valid_cats = valid_X_categories()

    germ_df = pd.concat(
        [
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["H_Germline"], categories=valid_cats["H_Germline"]
                ),
                prefix="H_G",
            ),
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["L_Germline"], categories=valid_cats["L_Germline"]
                ),
                prefix="L_G",
            ),
        ],
        axis=1,
        sort=False,
    )
    H_can_df = pd.concat(
        [
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["H_CanHV1"].astype(str), categories=valid_cats["H_CanHV1"]
                ),
                prefix="H_Can1",
            ),
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["H_CanHV2"].astype(str), categories=valid_cats["H_CanHV2"]
                ),
                prefix="H_Can2",
            ),
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["H_CanHV3"].astype(str), categories=valid_cats["H_CanHV3"]
                ),
                prefix="H_Can3",
            ),
        ],
        axis=1,
        sort=False,
    )

    L_can_df = pd.concat(
        [
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["L_CanHV1"].astype(str), categories=valid_cats["L_CanHV1"]
                ),
                prefix="L_Can1",
            ),
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["L_CanHV2"].astype(str), categories=valid_cats["L_CanHV2"]
                ),
                prefix="L_Can2",
            ),
            pd.get_dummies(
                pd.Categorical(
                    tmp_data["L_CanHV3"].astype(str), categories=valid_cats["L_CanHV3"]
                ),
                prefix="L_Can3",
            ),
        ],
        axis=1,
        sort=False,
    )
    HV_len_df = tmp_data.loc[
        :,
        ["H_HV1_len", "H_HV2_len", "H_HV3_len", "L_HV1_len", "L_HV2_len", "L_HV3_len"],
    ]
    feat_data = pd.concat([H_can_df, L_can_df, germ_df], axis=1)
    feat_data.index = tmp_data.index
    return pd.concat([HV_len_df, feat_data], axis=1).to_numpy(dtype=float)


def encode_X_sequence(a_df, encoding, add_position=1):
    """Encodes sequences based on encoding scheme with padding for even length."""
    a_array = a_df.sum(axis=1).values
    embedding_dic = embedding_read(encoding)
    tmp_data = list(str_padding(a_array, length="max"))
    return give_score(tmp_data, embedding_dic, add_position)


def embedding_read(Embedding_file):
    """Turns the embedding file into a dictionary for easy use."""
    embedding_dic = {}
    with open(Embedding_file, "r") as f:
        for line in f:
            if not line.startswith("#"):
                line = line.split()
                embedding_dic[line[0]] = [float(i) for i in line[1:]]
    return embedding_dic


def str_padding(a_array, length="max"):
    """Padding using X to each string in a nested list, in order to make all
    strings the same length. Padding is on both sides of the string.
    """
    if length == "max":
        max_l = len(max(a_array, key=len))
    else:
        max_l = int(length)

    for num, val in enumerate(a_array):
        if len(val) <= max_l:
            num_x = max_l - len(val)
            # Put X's on both sides of the sequence
            yield ("X" * int(np.ceil(num_x / 2))) + val + (
                "X" * int(np.floor(num_x / 2))
            )


def give_score(a_array, score_dic, add_position=0):
    """Applies the embedding to the sequence.

    Additionally a normalization of the position of the residue within the
    sequence can also be added.
    """
    if add_position == 0:
        return np.array([np.array([score_dic[j] for j in i]) for i in a_array])
    elif add_position == 1:
        return np.array(
            [
                np.array([score_dic[j] + [num / len(i)] for num, j in enumerate(i)])
                for i in a_array
            ]
        )


"""Model"""


def create_proABC_v2(hps):
    """Creates the model 'proABC_v2' and initializes it."""

    class proABC_v2(Model):
        def __init__(self, hps):
            super(proABC_v2, self).__init__()
            self.conv11 = Conv1D(filters=32, kernel_size=3, strides=1, activation="elu")
            self.maxpool11 = MaxPooling1D(pool_size=10, strides=3)
            self.dropout11 = Dropout(0.15)

            self.conv12 = Conv1D(filters=32, kernel_size=3, strides=1, activation="elu")
            self.maxpool12 = MaxPooling1D(pool_size=10, strides=3)
            self.dropout12 = Dropout(0.15)

            self.conv2 = Conv1D(64, 3, 1, activation="elu")
            self.maxpool2 = MaxPooling1D(pool_size=6, strides=3)
            self.dropout2 = Dropout(0.15)
            self.flatten = Flatten()
            self.d1 = Dense(512, activation="elu")
            self.dropout3 = Dropout(0.1)
            self.d2 = Dense(hps["y_out"], activation="sigmoid")

        def call(self, x):
            x1, x2 = x
            x11, x12 = x1[:, :153], x1[:, 153:]

            x11 = self.dropout11(self.maxpool11(self.conv11(x11)))
            x12 = self.dropout12(self.maxpool12(self.conv12(x12)))
            x1 = tf.concat([x11, x12], 1)  # either dimension 1 or 2
            x1 = self.dropout2(self.maxpool2(self.conv2(x1)))

            x1 = self.flatten(x1)
            x1 = tf.concat([x1, x2], 1)
            x1 = self.dropout3(self.d1(x1))
            return self.d2(x1)

    model = proABC_v2(hps)
    model.compile(loss=[focal_loss()], metrics=["accuracy"], optimizer="sgd")

    return model


def focal_loss(gamma=4, alpha=0.2, mask_val=-1):
    """Loss function that takes into account a low positive to negative ratio.

    Written by Martin Closter Jespersen.
    """

    def focal_loss_fixed(y_true, y_pred):
        y_mask = tf.cast(
            tf.where(
                tf.not_equal(y_true, mask_val),
                tf.ones_like(y_true),
                tf.zeros_like(y_true),
            ),
            tf.bool,
        )
        y_true = tf.boolean_mask(y_true, y_mask)
        y_pred = tf.boolean_mask(y_pred, y_mask)
        y_pred = tf.clip_by_value(
            y_pred, tf.keras.backend.epsilon(), 1 - tf.keras.backend.epsilon()
        )
        pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
        pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
        loss = -K.sum(alpha * K.pow(1.0 - pt_1, gamma) * K.log(pt_1)) - K.sum(
            (1 - alpha) * K.pow(pt_0, gamma) * K.log(1.0 - pt_0)
        )
        return loss / tf.reduce_sum(y_true)
        # return loss

    return focal_loss_fixed


def predict(out, hps, model_name, x_data):
    """Initialize the model with the correct weights and make the predictions"""

    # Create a vector of 0s in order to initialize the model
    # The out of the model is a numpy array of length 297 * (number of predicted interactions)
    y_target = np.zeros((1, out), dtype=int)
    tf.keras.backend.clear_session()
    proABC_model = create_proABC_v2(hps)

    #  Initialize the model with random weights
    proABC_model.fit(x_data, y_target, epochs=1, verbose=0)

    # Load in the correct weights from a trained model
    proABC_model.load_weights(model_name)

    # Make predictions
    y_pred = proABC_model.predict(x_data)

    return y_pred
