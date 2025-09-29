# Get Resolve app
resolve = bmd.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

if not timeline:
    print("No active timeline")
    exit()

# Get all timeline markers
markers = timeline.GetMarkers()
marker_positions = sorted(markers.keys())

if not marker_positions:
    print("No markers on timeline")
    exit()

# Get clips from Media Pool
media_pool = project.GetMediaPool()
current_folder = media_pool.GetCurrentFolder()
selected_clips = current_folder.GetClips()

if not selected_clips:
    print("No clips in Media Pool folder")
    exit()

clips_list = list(selected_clips.values())

# Loop through markers and place clips
for i, marker_frame in enumerate(marker_positions[:-1]):
    if i >= len(clips_list):
        break

    clip = clips_list[i]
    start_frame = marker_frame
    end_frame = marker_positions[i + 1]
    duration = end_frame - start_frame

    # Use AppendToTimeline with proper clip info
    clip_info = {
        "mediaPoolItem": clip,
        "trackIndex": 1,
        "recordFrame": int(start_frame)
    }

    media_pool.AppendToTimeline([clip_info])

    # Get the just-added clip
    items = timeline.GetItemListInTrack("video", 1)
    if items:
        last_item = items[-1]
        # Trim the clip to match duration
        last_item.SetProperty("End", int(start_frame + duration))

    print(f"Placed clip {i+1} at frame {start_frame} with duration {duration}")

print("Done!")