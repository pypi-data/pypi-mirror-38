import numpy as np
import pandas as pd

from simulate_replay.behavior import (get_speed, get_task,
                                      simulate_linear_distance_with_pauses,
                                      simulate_time)
from simulate_replay.LFP import simulate_LFP
from simulate_replay.multiunit import simulate_multiunit
from simulate_replay.spiking import (create_place_field, insert_replay_spikes,
                                     simulate_poisson_spikes)


def simulate_dataset(replay_info, sampling_frequency=1000, total_time=100.0,
                     brain_areas=None):
    '''
    '''
    # Behavior
    position_info = create_behavior_dataset(total_time, sampling_frequency)

    # spikes
    spikes, neuron_info = create_spikes_dataset(
        position_info.linear_distance, sampling_frequency,
        task=position_info.task, place_field_spacing=15,
        brain_areas=brain_areas)
    spikes = insert_replay_spikes(position_info, spikes, neuron_info,
                                  replay_info)

    # LFPs
    # time = position_info.index
    # lfps = np.stack((
    #     simulate_LFP(time, pause_times[:3, 0] + pause_width / 2, noise_amplitude=1.2,
    #                  ripple_amplitude=1, ripple_width=ripple_duration),
    #     simulate_LFP(time, pause_times[:2, 0] + pause_width / 2, noise_amplitude=1.2,
    #                  ripple_amplitude=1.1, ripple_width=ripple_duration)), axis=1)

    # multiunit
    # mark_means = np.array([200, 125, 325, 275])
    # place_field_means = np.stack((np.arange(0, 200, 50),
    #                               np.arange(25, 200, 50)))

    # multiunit = np.stack([
    #     simulate_multiunit(means, mark_means, linear_distance, sampling_frequency),
    #     for means in place_field_means], axis=-1)

    # TODO: Insert Replay

    # Ripple Times
    # is_ripple = np.zeros_like(time, dtype=bool)
    #
    # for start, end in ripple_times:
    #     is_ripple[(time >= start) & (time <= end)] = True

    return {
        'position_info': position_info,
        'spikes': spikes,
    }


def create_spikes_dataset(linear_distance, sampling_frequency, task=None,
                          place_field_spacing=15, brain_areas=None,
                          is_task_selective=True):
    linear_distance = np.array(linear_distance)
    if task is None:
        task = np.full_like(linear_distance, 'None', dtype=object)
    else:
        task = np.array(task)
    brain_areas = brain_areas or ['Default']

    place_field_centers = np.arange(
        linear_distance.min(), linear_distance.max(), place_field_spacing)
    neuron_info = []
    for b in np.unique(brain_areas):
        for t in pd.unique(task[pd.notnull(task)]):
            neuron_info.append(pd.DataFrame(
                {'place_field_center': place_field_centers,
                 'task_selectivity': t,
                 'brain_area': b}))
    neuron_info = pd.concat(neuron_info, ignore_index=True).dropna()

    place_fields = []
    for _, info in neuron_info.iterrows():
        place_fields.append(
            create_place_field(info.place_field_center, linear_distance,
                               sampling_frequency,
                               is_condition=(task == info.task_selectivity)))

    place_fields = np.stack(place_fields)
    spikes = simulate_poisson_spikes(place_fields, sampling_frequency).T

    return spikes, neuron_info


def create_behavior_dataset(total_time, sampling_frequency, pause_time=2.0):
    time = simulate_time(total_time, sampling_frequency)

    linear_distance = simulate_linear_distance_with_pauses(
        time, sampling_frequency=sampling_frequency, pause_time=pause_time)

    speed = get_speed(linear_distance, sampling_frequency)
    task = get_task(linear_distance)

    return pd.DataFrame({
        'linear_distance': linear_distance,
        'speed': speed,
        'task': task,
        'time': time,
    }).set_index('time')
