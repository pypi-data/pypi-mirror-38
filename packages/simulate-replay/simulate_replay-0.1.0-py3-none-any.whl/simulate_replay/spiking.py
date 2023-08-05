'''Tools for simulating place field spiking'''
import numpy as np
from scipy.stats import norm
from scipy.ndimage.measurements import label


def simulate_poisson_spikes(rate, sampling_frequency):
    return 1.0 * (np.random.poisson(rate / sampling_frequency) > 0)


def create_place_field(
    place_field_mean, linear_distance, sampling_frequency, is_condition=None,
        place_field_std_deviation=12.5, max_firing_rate=20,
        baseline_firing_rate=0.01):
    if is_condition is None:
        is_condition = np.ones_like(linear_distance, dtype=bool)
    field_firing_rate = norm(
        place_field_mean, place_field_std_deviation).pdf(linear_distance)
    field_firing_rate /= np.nanmax(field_firing_rate)
    field_firing_rate[~is_condition] = 0
    return baseline_firing_rate + max_firing_rate * field_firing_rate


def get_replay_spike_ind(linear_distance, task, place_field_centers,
                         replay_speed=20, replay_type='Inbound',
                         replay_order='Forward'):
    '''For a given replay type and order, return the spike time index that
    corresponds to the location of a neuron's place field location.

    Parameters
    ----------
    linear_distance : ndarray, shape (n_time,)
    task : ndarray, shape (n_time,)
    place_field_centers : ndarray, shape (n_neurons,)
    replay_speed : int, optional
    replay_type : str, optional
    replay_order : str, optional

    Returns
    -------
    spike_time_ind : ndarray, shape (n_neurons,)

    '''
    place_field_centers = np.array(place_field_centers)
    replay_order_map = {'Forward': 1,
                        'Reverse': -1}
    replay_type_map = {
        'Outbound': linear_distance[label(task == 'Outbound')[0] == 1],
        'Inbound': linear_distance[label(task == 'Inbound')[0] == 1],
    }
    replay_position = replay_type_map[replay_type][::replay_speed, np.newaxis]
    order = replay_order_map[replay_order]
    spike_time_ind = np.abs(
        place_field_centers - replay_position).argmin(axis=0)
    return spike_time_ind[::order]


def insert_replay_spikes(position_info, spikes, neuron_info, replay_info):
    spikes = spikes.copy()
    n_neurons = neuron_info.shape[0]

    for start_time, df in replay_info.groupby('start_time'):
        neuron_ind = []
        spike_time_ind = []
        for _, r in df.iterrows():
            time_ind = get_replay_spike_ind(
                position_info.linear_distance, position_info.task,
                neuron_info.place_field_center, replay_speed=r.replay_speed,
                replay_type=r.replay_type,
                replay_order=r.replay_order)
            neuron_ind.append(neuron_info.loc[
                (neuron_info.task_selectivity == r.replay_type) &
                (neuron_info.brain_area == r.brain_area)].index)
            spike_time_ind.append(time_ind[neuron_ind[-1]])

        neuron_ind = np.concatenate(neuron_ind)
        spike_time_ind = np.concatenate(spike_time_ind)
        n_time = spike_time_ind.max() + 1
        replay_spikes = np.zeros((n_time, n_neurons))
        replay_spikes[(spike_time_ind, neuron_ind)] = 1

        start_ind = np.searchsorted(position_info.index, start_time)
        end_ind = start_ind + replay_spikes.shape[0]
        spikes[start_ind:end_ind, :] = replay_spikes
    return spikes
