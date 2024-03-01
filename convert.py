from argparse  import ArgumentParser
import subprocess

parser = ArgumentParser()

configfile = "config/convert.ini"

def convert() -> None:
    input = "resources/images/convert"
    output = "resources/converts/swapped_images"
    model = "resources/trains/model"
    alignments = "resources/images/convert/alignments.fsa"
    result = subprocess.run([
        "python", "lib/faceswap.py", "convert", 
        "--input-dir", input, "--output-dir", output, 
        "--model-dir", model, "--alignments", alignments,
        "--configfile", configfile
    ], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Failed to train")
    print("complete convert")

def _main():
    parser.add_argument('function_name',
                        type=str,
                        help='実行するメソッド名')

    args = parser.parse_args()
    if args.function_name == "convert":
        convert()

if __name__ == "__main__":
    _main()