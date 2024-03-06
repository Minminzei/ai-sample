import glob
import os
from argparse import ArgumentParser 
import matplotlib.pyplot as plt
import imageio

parser = ArgumentParser()
resource_path = os.getenv("RESOURCE_PATH")

def video_to_images(person_name:str, fps:str) -> None:
    try:
        original = f'{resource_path}/originals/{person_name}'
        output = f'{resource_path}/images/{person_name}'
        counter = 0

        for file in glob.glob(f'{output}/*.png'):
            os.remove(file)

        for input_path in glob.glob(f'{original}/*.mp4'):
            video = imageio.get_reader(input_path, 'ffmpeg', fps=int(fps))
            for _, image in enumerate(video.iter_data()):
                plt.imsave(f'{output}/{counter:06}.png',image)
                counter += 1
        print(f"Saved {counter} images to {output}")
    except Exception as e:
        print("Error running ffmpeg")
        print(e)

def images_to_video(fps:str) -> None:
    try:
        output = f'{resource_path}/converts/video'
        for file in glob.glob(f'{output}/*.mp4'):
            os.remove(file)

        writer = imageio.get_writer(f'{output}/output.mp4', fps=int(fps))
        for file in sorted(glob.glob(f'{resource_path}/converts/swapped_images/*.png')):
            im = imageio.v2.imread(file)
            writer.append_data(im)
        writer.close()
        print(f"Saved video to {resource_path}/converts/video")
    except Exception as e:
        print("Error running ffmpeg")
        print(e)

def _main():
    parser.add_argument('function_name',
                        type=str,
                        help='実行するメソッド名')
    parser.add_argument('-n', '--name',
                        type=str,
                        help='取得したい人物の名前 [input_a, input_b]')
    parser.add_argument('-f', '--fps',
                        type=str,
                        help='フレームレート',
                        default="25")
    
    args = parser.parse_args()
    if args.function_name == "video_to_images":
        video_to_images(args.name, args.fps)
    elif args.function_name == "images_to_video":
        images_to_video(args.fps)

if __name__ == "__main__":
    _main()