import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort
import time
import os

# Load the model
print("Loading model...")
model = YOLO('best.pt')

# Initialize the tracker
print("Setting up tracker...")
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# Store player positions
player_positions = {}

def process_video(input_video, output_video):
    print("Opening video...")
    cap = cv2.VideoCapture(input_video)
    
    # Get video info
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # Create video writer
    print("Creating output video...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    frame_count = 0
    total_time = 0
    
    print("Starting video processing...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Start timing
        start_time = time.time()
        
        # Detect players
        results = model(frame, conf=0.3, verbose=False)
        
        # Get detections
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].numpy()
                conf = box.conf[0].numpy()
                detections.append([x1, y1, x2, y2, conf])
        
        # Update tracker
        if len(detections) > 0:
            detections = np.array(detections)
            tracks = tracker.update(detections)
            
            # Draw boxes and IDs
            for track in tracks:
                x1, y1, x2, y2, track_id = track
                track_id = int(track_id)
                
                # Draw box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Draw ID
                cv2.putText(frame, f"ID: {track_id}", (int(x1), int(y1)-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Store position
                if track_id not in player_positions:
                    player_positions[track_id] = []
                player_positions[track_id].append((int((x1+x2)/2), int((y1+y2)/2)))
                
                # Draw path
                if len(player_positions[track_id]) > 1:
                    points = np.array(player_positions[track_id][-10:], dtype=np.int32)
                    cv2.polylines(frame, [points], False, (0, 255, 0), 1)
        
        # Calculate FPS
        end_time = time.time()
        processing_time = end_time - start_time
        total_time += processing_time
        frame_count += 1
        fps_current = 1 / processing_time
        
        # Show FPS
        cv2.putText(frame, f"FPS: {fps_current:.1f}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Write frame
        out.write(frame)
        
        # Show frame
        cv2.imshow('Player Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Print results
    print("\nResults:")
    print(f"Total frames processed: {frame_count}")
    print(f"Average FPS: {frame_count/total_time:.2f}")
    print(f"Total unique players tracked: {len(player_positions)}")
    
    # Clean up
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Main program
print("Starting player tracking program...")
input_video = "15sec_input_720p.mp4"
output_video = "output/output_tracked.mp4"
process_video(input_video, output_video)
print("Done!") 