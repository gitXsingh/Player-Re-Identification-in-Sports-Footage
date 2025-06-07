# Player Re-Identification in Sports Footage

This project performs player re-identification in a 5-second soccer video using a fine-tuned YOLOv5 model. It assigns consistent IDs to players, even when they leave and re-enter the frame, simulating real-time tracking and handling occlusion to ensure identity consistency throughout the clip.

## Features

- Player detection using YOLOv5
- Player tracking with SORT algorithm
- Re-identification when players re-enter frame
- Basic trajectory visualization
- Performance metrics tracking

## Requirements

- Python 3.8+
- OpenCV
- NumPy
- Ultralytics YOLO
- SORT tracking algorithm

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gitXsingh/Player-Re-Identification-in-Sports-Footage.git
cd Player-Re-Identification-in-Sports-Footage
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your input video in the project directory
2. Run the tracking script:
```bash
python player_tracking.py
```

3. The output video will be saved in the `output` directory

## Project Structure

- `player_tracking.py`: Main tracking script
- `requirements.txt`: Required Python packages
- `report.md`: Project report and documentation
- `output/`: Directory for output videos

## Performance

- Current FPS: ~0.87
- Average detections per frame: ~10.49
- Total unique players tracked: 69

## Limitations

- Requires good CPU/GPU for real-time processing
- Basic re-identification capabilities
- Limited to single camera view
- Performance depends on hardware

## Future Improvements

- GPU acceleration
- Better re-identification
- Multiple camera support
- Real-time processing
- Advanced visualization

## License

This project is open source and available under the MIT License. 