import argparse
import os
import json

from src.utils.Config import Config
from src.train import train


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # Arguments for running any datasets
    parser.add_argument('-d', "--data_dir", default=None, help="Data directory containing train/val/test jsonl files")
    parser.add_argument('-p', "--pattern", default=None, help="Pattern to be used for this dataset")
    parser.add_argument('-v', "--dict_verbalizer", type=json.loads, default=None, help="Dictionary mapping label name (in dataset) to the verbalizer to use, e.g. '{\"0\": \"Yes\", \"1\": \"No\"}'")

    # Model and training hyperparams

    parser.add_argument('-w', '--pretrained_weight', type=str, default='albert-xxlarge-v2', help='Pretrained model weights from huggingface')
    parser.add_argument('-bs', '--batch_size', type=int, default=1, help='batch size during training')
    parser.add_argument('--eval_batch_size', type=int, default=1, help='batch size during evaluation')
    parser.add_argument('--grad_accumulation_factor', type=int, default=16, help='number of gradient accumulation steps')
    parser.add_argument('--num_batches', type=int, default=50, help='number of batches for experiment; 1 batch = grad_accumulation_factor x batch_size')
    parser.add_argument('--eval_every', type=int, default=1, help='number of training batches per evaluation')
    parser.add_argument('--max_text_length', type=int, default=256, help='maximum total input sequence length after tokenization for ADAPET')
    parser.add_argument('--lr', type=float, default=1e-5, help='learning rate for the model')
    parser.add_argument('--weight_decay', type=float, default=1e-2, help='weight decay for the optmizer')
    parser.add_argument('--grad_clip_norm', type=float, default=1, help='gradient clipping norm')
    parser.add_argument('--warmup_ratio', type=float, default=0.06, help='linear warmup over warmup_steps for num_batches')
    parser.add_argument('--dir_names', type=str, default="default")

    # ADAPET hyperparameters
    parser.add_argument('--pattern_idx', default=1, help="Pattern index among all patterns available; For SuperGLUE, can use numbers >1 depending on dataset. For a new dataset, please set this to 1.")
    parser.add_argument('--mask_alpha', type=float, default=0.105, help='masking ratio for the label conditioning loss')
    parser.add_argument('--idx_txt_trim', type=int, default=1, help="TXT_ID of the text that can be trimmed (usually the longer text). Eg. if TXT1 needs to be trimmed, set this to 1.")
    parser.add_argument('--max_num_lbl_tok', type=int, default=1, help="The maximum number of tokens per label for the verbalizer. It will raise an error if the tokenizer tokenizes a label into more than 'max_num_lbl_tok' tokens.")

    # Replicating SuperGLUE results
    parser.add_argument('-c', '--config', type=str, default=None, help='Use this for replicating SuperGLUE results.')

    args = parser.parse_args()

    # If even one of these three arguments are provided, we need all three as input
    if args.data_dir or args.pattern or args.dict_verbalizer:
        assert args.data_dir and args.pattern and args.dict_verbalizer, 'Please enter all of data_dir, pattern, dict_verbalizer!'

    if args.config is not None:
        use_config = args.config
    else:
        assert args.data_dir or args.pattern or args.dict_verbalizer, 'Please enter all of data_dir, pattern, dict_verbalizer if not providing config!'
        use_config = os.path.join("config", "Generic.json")

    update_config = vars(args)
    config = Config(use_config, update_config, mkdir=True)
    train(config)
