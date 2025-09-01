import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def parse_asc_file(file_path):
    samples = []
    fixations = []
    saccades = []
    blinks = []
    messages = []

    # Regular expressions to match events
    fixation_pattern = re.compile(r'EFIX\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)')
    saccade_pattern = re.compile(r'ESACC\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)')
    blink_pattern = re.compile(r'EBLINK\s+(\w+)\s+(\d+)\s+(\d+)')
    message_pattern = re.compile(r'MSG\s+(\d+)\s+(.+)')  # Matches MSG lines with timestamp and message content

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            if line:
                # Parsing sample data (including pupil size)
                if line[0].isdigit():  # Sample data for right or left eye
                    parts = line.split()
                    time = float(parts[0])  # Timestamp
                    if parts[1] == '.' or parts[2] == '.':
                        print(f"Warning: Found '.' for coordinates in line: {line}.")
                    else:
                        x, y = float(parts[1]), float(parts[2])  # Gaze coordinates
                    pupil_size = float(parts[3])  # Pupil size
                    samples.append([time, x, y, pupil_size])

                # Parsing fixation events
                elif line.startswith('EFIX'):
                    match = fixation_pattern.match(line)
                    if match:
                        eye, start, end, duration, x, y, pupil_size = match.groups()
                        fixations.append([eye, int(start), int(end), int(duration), float(x), float(y), float(pupil_size)])

                # Parsing saccade events
                elif line.startswith('ESACC'):
                    match = saccade_pattern.match(line)
                    if match:
                        eye, start, end, duration, start_x, start_y, end_x, end_y = match.groups()
                        saccades.append([eye, int(start), int(end), int(duration), float(start_x), float(start_y), float(end_x), float(end_y)])

                # Parsing blink events
                elif line.startswith('EBLINK'):
                    match = blink_pattern.match(line)
                    if match:
                        eye, start, end = match.groups()
                        blinks.append([eye, int(start), int(end)])

                # Parsing messages
                elif line.startswith('MSG'):
                    match = message_pattern.match(line)
                    if match:
                        time, msg = match.groups()
                        messages.append([int(time), msg])

    # Converting to pandas DataFrames
    sample_df = pd.DataFrame(samples, columns=['Time', 'X', 'Y', 'PupilSize'])
    fixation_df = pd.DataFrame(fixations, columns=['Eye', 'Start', 'End', 'Duration', 'X', 'Y', 'PupilSize'])
    saccade_df = pd.DataFrame(saccades, columns=['Eye', 'Start', 'End', 'Duration', 'StartX', 'StartY', 'EndX', 'EndY'])
    blink_df = pd.DataFrame(blinks, columns=['Eye', 'Start', 'End'])
    message_df = pd.DataFrame(messages, columns=['Time', 'Message'])

    return sample_df, fixation_df, saccade_df, blink_df, message_df

def eye_movement_visualization(sample_data, fixation_data=None, saccade_data=None, blink_data=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot raw gaze samples with color based on time for a smooth gradient
    times = sample_data['Time']
    norm = plt.Normalize(times.min(), times.max())  # Normalize the time for color mapping
    cmap = plt.get_cmap('viridis')  # Gradient color map
    
    scatter = ax.scatter(sample_data['X'], sample_data['Y'], c=times, cmap=cmap, label='Gaze Path', s=5, alpha=0.8)

    # Plot fixations with size proportional to duration and color based on duration
    if fixation_data is not None and not fixation_data.empty:
        norm_fix_duration = plt.Normalize(fixation_data['Duration'].min(), fixation_data['Duration'].max())
        ax.scatter(fixation_data['X'], fixation_data['Y'], 
                    s=fixation_data['Duration']*0.1,  # Size by fixation duration
                    c=fixation_data['Duration'], cmap='coolwarm', label='Fixations', alpha=0.7, edgecolor='black')

    # Plot saccades as lines between fixation points
    if saccade_data is not None and not saccade_data.empty:
        for _, row in saccade_data.iterrows():
            ax.plot([row['StartX'], row['EndX']], [row['StartY'], row['EndY']], color='green', alpha=0.6)

    # Plot blinks as gaps or transparent markers
    '''
    if blink_data is not None and not blink_data.empty:
        for _, row in blink_data.iterrows():
            ax.axvspan(row['Start'], row['End'], color='gray', alpha=0.3)
    '''

    # Add color bar for gaze path time
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label('Time (ms)')
    
    # Add labels and aesthetics
    ax.set_title('Enhanced Eye Movement Visualization')
    ax.set_xlabel('Gaze X Coordinate')
    ax.set_ylabel('Gaze Y Coordinate')
    ax.invert_yaxis()  # Inverting Y axis to match eye-tracker data format
    ax.legend(loc='best')
    ax.grid(True)

    # Show the enhanced plot
    plt.show()

# Example usage
sample_data, fixation_data, saccade_data, blink_data, message_data = parse_asc_file('/media/ak278591/Ali/ss00r01.asc')
eye_movement_visualization(sample_data, fixation_data, saccade_data, blink_data)

# Preview the parsed data
print("Sample Data:\n", sample_data.head())
print("Fixation Data:\n", fixation_data.head())
print("Saccade Data:\n", saccade_data.head())
print("Blink Data:\n", blink_data.head())
print("Message Data:\n", message_data.head())