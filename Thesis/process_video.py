import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def process_videos(green_range, bg_image_path, video_paths):
    # Load the background image
    bg_image = ImageClip(bg_image_path)

    # Define the processed video file paths
    processed_video_paths = {}

    # Get the path to the Videos folder
    videos_folder_path = os.path.join(os.path.dirname(os.getcwd()), "Videos")

    # Process each video file
    for name, path in video_paths.items():
        # Load the video clip
        video_clip = VideoFileClip(os.path.join(videos_folder_path, path))

        # Apply the green screen effect to the video clip
        green_screen_clip = video_clip.fx(vfx.colorkey, color=green_range)

        # Resize the green screen clip to fit the background image
        green_screen_clip = green_screen_clip.resize(bg_image.size)

        # Create a composite video clip with the green screen clip and the background image
        composite_clip = CompositeVideoClip([green_screen_clip, bg_image.set_duration(green_screen_clip.duration)])

        # Set the background color of the composite clip as the mask color
        mask_color = tuple(int(bg_image.get_frame(0)[i]) for i in range(3))
        composite_clip = composite_clip.set_mask(ImageClip(bg_image.size, color=mask_color))

        # Write the processed video clip to a file
        processed_path = f"{name}_processed.mp4"
        composite_clip.write_videofile(processed_path, fps=25, codec='libx264')

        # Add the processed video file path to the dictionary
        processed_video_paths[name] = processed_path

    return processed_video_paths