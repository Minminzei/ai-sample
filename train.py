from argparse  import ArgumentParser
import subprocess

parser = ArgumentParser()

def train() -> None:
    input_a = "resources/extract/input_a"
    input_b = "resources/extract/input_b"
    output = "resources/train"
    model_dir = f"{output}/model"
    configfile = "config/faceswap/train.ini"
    trainer = "lightweight"
    result = subprocess.run([
        "python", "faceswap/faceswap.py", "train", 
        "--input-A", input_a, "--input-B", input_b, 
        "--model-dir", model_dir, "--trainer", trainer,
        "--configfile", configfile
    ], stdout=subprocess.PIPE)
    print(result)
    if result.returncode != 0:
        raise Exception("Failed to train")

def _main():
    parser.add_argument('function_name',
                        type=str,
                        help='実行するメソッド名')
    
    args = parser.parse_args()
    if args.function_name == "train":
        train(args.input_a, args.input_b)

if __name__ == "__main__":
    _main()