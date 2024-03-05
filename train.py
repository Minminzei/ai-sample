import os
from argparse  import ArgumentParser
import subprocess

parser = ArgumentParser()
resource_path = os.getenv("RESOURCE_PATH")

configfile = "config/train.ini"

def train(trainer:str) -> None:
    input_a = f"{resource_path}/extracts/input_a"
    input_b = f"{resource_path}/extracts/input_b"
    output = f"{resource_path}/trains"
    model_dir = f"{output}/model"
    result = subprocess.run([
        "python", "lib/faceswap.py", "train", 
        "--input-A", input_a, "--input-B", input_b, 
        "--model-dir", model_dir, "--trainer", trainer,
        "--configfile", configfile, "--write-image"
    ], stdout=subprocess.PIPE)
    print(result)
    if result.returncode != 0:
        raise Exception("Failed to train")

def _main():
    parser.add_argument('function_name',
                        type=str,
                        help='実行するメソッド名')
    parser.add_argument('-t', '--trainer',
                        type=str,
                        help='使用するモデル',
                        default="lightweight")

    args = parser.parse_args()
    if args.function_name == "train":
        train(args.trainer)

if __name__ == "__main__":
    _main()