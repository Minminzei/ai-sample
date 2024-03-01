import glob
import os
import shutil
from argparse  import ArgumentParser
import subprocess

parser = ArgumentParser()

configfile = 'config/extract.ini'

def extract(person_name: str) -> None:
    input = f"resources/images/{person_name}"
    output = f"resources/extracts/{person_name}"
    # 学習で使用するモデルで規定されたサイズを指定する
    # Ex. Lightweight: 64px, Realface: 64-128px
    size = 512

    for file in glob.glob(f'{output}/*.png'):
        os.remove(file)

    result = subprocess.run([
        "python", "lib/faceswap.py", "extract", 
        "--input-dir", input, "--output-dir", output,
        "--size", str(size), "--configfile", configfile
    ], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Failed to extract faces")

    print("complete extract")

def sort_by_face(person_name: str) -> None:
    input = f"resources/extracts/{person_name}"
    sort_by = "face"
    threshold = "0.5"
    group_by = "face"
    final = "rename"
    result = subprocess.run([
        "python", "lib/tools.py", "sort", "--input", input,
        "--sort-by", sort_by, "--group-by", group_by,
        "--threshold", threshold, "--final-process", final
    ], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Failed to extract faces")

    print("complete sorting")

def clean_up(person_name: str) -> None:
    faces = f"resources/extracts/{person_name}"
    # 生成されたフォルダを削除して、画像を1階層あげる
    for file in glob.glob(f"{faces}/*"):
        if os.path.isdir(file):
            for image in glob.glob(f"{file}/*.png"):
                os.rename(image, f"{faces}/{os.path.basename(image)}")
            shutil.rmtree(file, ignore_errors=True)
    alignments = f"resources/images/{person_name}/alignments.fsa"
    job = "remove-faces"
    output = "file"
    result = subprocess.run([
        "python", "lib/tools.py", "alignments", "--alignments_file", alignments,
        "--job", job, "-faces_folder", faces, "--output", output
    ], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception("Failed to clean up")

    print("complete clean up")

def _main():
    parser.add_argument('function_name',
                        type=str,
                        help='実行するメソッド名')
    parser.add_argument('-n', '--name',
                        type=str,
                        help='取得したい人物の名前 [input_a, input_b]')

    args = parser.parse_args()
    if args.function_name == "extract":
        extract(args.name)
    elif args.function_name == "sort_by_face":
        sort_by_face(args.name)
    elif args.function_name == "clean_up":
        clean_up(args.name)

if __name__ == "__main__":
    _main()