import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


def simulate_time(total_time, sampling_frequency):
    n_samples = int(total_time * sampling_frequency)
    return np.arange(n_samples) / sampling_frequency


def simulate_linear_distance(time, track_height, running_speed=10):
    half_height = (track_height / 2)
    return (half_height * np.sin(2 * np.pi * time / running_speed - np.pi / 2)
            + half_height)


def _insert_pause(linear_distance, pause_time, sampling_frequency,
                  pause_position):
    peaks = np.nonzero((linear_distance == pause_position))[0]
    n_pause_samples = int(pause_time * sampling_frequency)
    pause_linear_distance = np.zeros(
        (linear_distance.size + n_pause_samples * peaks.size,))
    pause_ind = (peaks[:, np.newaxis] + np.arange(n_pause_samples))
    pause_ind += np.arange(peaks.size)[:, np.newaxis] * n_pause_samples

    pause_linear_distance[pause_ind.ravel()] = pause_position
    is_pause = np.isin(np.arange(pause_linear_distance.size), pause_ind)
    pause_linear_distance[~is_pause] = linear_distance
    return pause_linear_distance[:linear_distance.size]


def simulate_linear_distance_with_pauses(
        time, track_height=170, running_speed=10,
        pause_time=0.5, sampling_frequency=1):
    linear_distance = simulate_linear_distance(
        time, track_height, running_speed)
    linear_distance = _insert_pause(
        linear_distance, pause_time, sampling_frequency, track_height)
    linear_distance = _insert_pause(
        linear_distance, pause_time, sampling_frequency, 0.0)

    return linear_distance


def get_task(linear_distance):
    is_inbound = np.insert(np.diff(linear_distance) < 0, 0, False)
    is_outbound = np.insert(np.diff(linear_distance) > 0, 0, False)
    task = np.ones_like(linear_distance, dtype=object)
    task[is_inbound], task[is_outbound] = 'Inbound', 'Outbound'
    task[~is_inbound & ~is_outbound] = 'Well'

    return task


def get_speed(linear_distance, sampling_frequency, smooth_duration=0.500):
    smoothed_linear_distance = gaussian_filter1d(
        linear_distance, smooth_duration * sampling_frequency)

    speed = np.abs(np.diff(smoothed_linear_distance) * sampling_frequency)
    return np.insert(speed, 0, 0.0)
