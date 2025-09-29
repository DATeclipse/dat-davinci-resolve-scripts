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

if len(marker_positions) < 2:
    print("Need at least 2 markers")
    exit()

print(f"Found {len(marker_positions)} markers creating {len(marker_positions)-1} intervals")

# Get all items from video track 1
video_track = 1
items = timeline.GetItemListInTrack("video", video_track)
items.sort(key=lambda item: item.GetStart())

print(f"Found {len(items)} clips\n")

num_to_process = min(len(items), len(marker_positions) - 1)

# Try to get the current playhead position
current_playhead = timeline.GetCurrentTimecode()

# Process clips by selecting and using timeline edit functions
for i in range(num_to_process):
    item = items[i]

    # Target duration from markers
    target_duration = marker_positions[i + 1] - marker_positions[i]

    # Current info
    current_start = item.GetStart()
    current_end = item.GetEnd()
    current_duration = current_end - current_start

    print(f"Clip {i+1}: Duration {current_duration} -> {target_duration}")

    if current_duration == target_duration:
        print(f"  Already correct duration\n")
        continue

    # Calculate new end point
    new_end = current_start + target_duration
    trim_amount = current_duration - target_duration

    # Try using timeline-level trim operations
    # Position playhead at the point where we want to trim
    trim_position = new_end

    try:
        # Set playhead to trim position
        timeline.SetCurrentTimecode(str(trim_position))

        # Select only this clip
        timeline.SelectItem(item)

        # Try to use Trim function
        if trim_amount > 0:
            # Trim from right (make shorter)
            result = timeline.TrimEnd(item, trim_position, False)
            print(f"  TrimEnd result: {result}")
        else:
            # Extend right (make longer)
            result = timeline.ExtendEnd(item, trim_position)
            print(f"  ExtendEnd result: {result}")

    except Exception as e:
        print(f"  Error: {e}")

    # Verify
    final_start = item.GetStart()
    final_end = item.GetEnd()
    final_duration = final_end - final_start
    print(f"  Result: {final_start} to {final_end} (duration: {final_duration})\n")

# Restore playhead
timeline.SetCurrentTimecode(current_playhead)

print("Done!")

# # Get Resolve app
# resolve = bmd.scriptapp("Resolve")
# project = resolve.GetProjectManager().GetCurrentProject()
# timeline = project.GetCurrentTimeline()
# media_pool = project.GetMediaPool()

# if not timeline:
#     print("No active timeline")
#     exit()

# # Get all timeline markers
# markers = timeline.GetMarkers()
# marker_positions = sorted(markers.keys())

# if len(marker_positions) < 2:
#     print("Need at least 2 markers")
#     exit()

# print(f"Found {len(marker_positions)} markers creating {len(marker_positions)-1} intervals")

# # Get all items from video track 1
# video_track = 1
# items = timeline.GetItemListInTrack("video", video_track)

# if not items:
#     print(f"No clips found on video track {video_track}")
#     exit()

# items.sort(key=lambda item: item.GetStart())
# print(f"Found {len(items)} clips on track {video_track}\n")

# num_to_process = min(len(items), len(marker_positions) - 1)

# # Store all clip info before making changes
# clip_data = []
# for i in range(num_to_process):
#     item = items[i]
#     media_pool_item = item.GetMediaPoolItem()
#     start_frame = marker_positions[i]
#     end_frame = marker_positions[i + 1]
#     duration = end_frame - start_frame

#     clip_data.append({
#         "mediaPoolItem": media_pool_item,
#         "name": media_pool_item.GetName() if media_pool_item else f"Clip {i+1}",
#         "startFrame": start_frame,
#         "endFrame": end_frame,
#         "duration": duration
#     })

# print(f"Processing {len(clip_data)} clips...\n")

# # Delete all original clips
# print("Deleting original clips...")
# timeline.DeleteClips(items[:num_to_process], False)

# # Add clips back one by one
# for i, data in enumerate(clip_data):
#     print(f"Clip {i+1} ({data['name']}): frame {data['startFrame']} to {data['endFrame']} (duration: {data['duration']})")

#     # Create clip info with explicit parameters
#     clip_info = {
#         "mediaPoolItem": data["mediaPoolItem"],
#         "startFrame": 0,  # Start from beginning of source
#         "endFrame": data["duration"] - 1,  # Trim to exact duration
#         "recordFrame": data["startFrame"]  # Place at marker position
#     }

#     # Append to timeline
#     result = media_pool.AppendToTimeline([clip_info])

#     if not result:
#         print(f"  WARNING: Failed to add clip {i+1}")
#     else:
#         # Verify placement
#         current_items = timeline.GetItemListInTrack("video", video_track)
#         if current_items:
#             last_item = current_items[-1]
#             actual_start = last_item.GetStart()
#             actual_end = last_item.GetEnd()
#             print(f"  Added: start={actual_start}, end={actual_end}, duration={actual_end - actual_start}")

#             # Check if placement is correct
#             if actual_start != data["startFrame"]:
#                 print(f"  WARNING: Expected start {data['startFrame']} but got {actual_start}")

# print("\nDone!")