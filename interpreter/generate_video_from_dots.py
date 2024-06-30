import os
import subprocess
from PIL import Image


# Construct the path to the Graphviz bin directory
graphviz_bin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin', 'Graphviz-11.0.0-win64', 'bin')
# Add the Graphviz bin directory to the PATH environment variable for the current process
os.environ["PATH"] += os.pathsep + graphviz_bin_path
# Now you can attempt to use 'dot' as if it was in the system's PATH
#same for ffmpeg
ffmpeg_bin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin', 'ffmpeg-7.0.1-essentials_build', 'bin')
os.environ["PATH"] += os.pathsep + ffmpeg_bin_path


def merge_images(frame_png, table_png, output_dir):
    frame_img = Image.open(frame_png)
    table_img = Image.open(table_png)

    # Calculate dimensions for the new image
    width = max(frame_img.width, table_img.width)
    height = frame_img.height + table_img.height

    # Create a new image with the calculated dimensions
    new_img = Image.new('RGB', (width, height), (255, 255, 255))

    # Calculate x position for the table image to be centered
    table_x = (width - table_img.width) // 2
    # Paste the table image onto the new image, centered
    new_img.paste(table_img, (table_x, 0))

    # Paste the frame image onto the new image, directly below the table image
    new_img.paste(frame_img, (0, table_img.height))

    # Save the new image
    frame_number = os.path.basename(frame_png).split('_')[1].split('.')[0]
    new_img_path = os.path.join(output_dir, f'merged_frame_{frame_number}.png')
    new_img.save(new_img_path)
    return new_img_path

def merge_frames_and_tables(png_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # List all frame PNG files
    frame_files = [f for f in os.listdir(png_dir) if f.startswith('frame_') and f.endswith('.png')]
    # Sort files numerically based on the number in their names
    frame_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    merged_files = []
    for frame_file in frame_files:
        frame_number = frame_file.split('_')[1].split('.')[0]
        table_file = f'variableTable_{frame_number}.png'
        # Check if the corresponding table file exists
        if table_file in os.listdir(png_dir):
            frame_path = os.path.join(png_dir, frame_file)
            table_path = os.path.join(png_dir, table_file)
            # Merge and save the new image
            merged_file_path = merge_images(frame_path, table_path, output_dir)
            merged_files.append(merged_file_path)
            print(f"Merged {frame_file} and {table_file}")
        else:
            print(f"No matching variable table found for {frame_file}")
    return merged_files


def dot_frames_to_pngs(dot_frames_dir, png_dir):
    # Create the directory for PNGs if it doesn't exist
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)

    dot_files = [f for f in os.listdir(dot_frames_dir) if f.endswith('.dot')]
    # Sort files numerically based on the number in their names
    dot_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    for dot_file in dot_files:
        dot_path = os.path.join(dot_frames_dir, dot_file)
        png_path = os.path.join(png_dir, dot_file.replace('.dot', '.png'))  # Save PNGs in the new directory

        subprocess.run(['dot', '-Tpng', dot_path, '-o', png_path, '-Gdpi=55'], check=True)
        print(f"Converted {dot_file} to PNG")

def pngs_to_video(merged_png_dir, mp4_path):
    png_files = [f for f in os.listdir(merged_png_dir) if f.endswith('.png')]
    # Sort files numerically based on the number in their names
    png_files.sort(key=lambda x: int(x.split('_')[2].split('.')[0]))
    subprocess.run(['ffmpeg', '-y', '-r', '1', '-i', os.path.join(merged_png_dir, 'merged_frame_%d.png'), '-c:v', 'libx264', '-vf', 'fps=25', mp4_path], check=True)
    print(f"Generated video at {mp4_path}")

def generate_video_from_dots(dot_frames_dir, mp4_path):

    png_dir = os.path.join(dot_frames_dir, 'pngs')
    merged_png_dir = os.path.join(dot_frames_dir, 'merged_pngs')
    if not os.path.exists(png_dir):
        os.makedirs(png_dir)
    if not os.path.exists(merged_png_dir):
        os.makedirs(merged_png_dir)

    mp4_path_dir = os.path.dirname(mp4_path)
    if	not	os.path.exists(mp4_path_dir):
        os.makedirs(mp4_path_dir)
    dot_frames_to_pngs(dot_frames_dir, png_dir)
    merge_frames_and_tables(png_dir, merged_png_dir)
    pngs_to_video(merged_png_dir, mp4_path)

if __name__ == "__main__":
    bin_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'bin')
    dot_frames_dir = os.path.join(bin_dir, 'interpretation_frames')
    mp4_path = os.path.join(bin_dir, 'interpretation_video.mp4')
    generate_video_from_dots(dot_frames_dir, mp4_path)
