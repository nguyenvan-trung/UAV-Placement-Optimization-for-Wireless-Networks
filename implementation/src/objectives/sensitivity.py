"""Opt-in sensitivity evaluator; does not replace baseline evaluate_solution."""
import numpy as np

from ..constants.network import TRANSMIT_POWER_DBM, NOISE_POWER_DBM
from ..physics.channel import (compute_distance_3d, compute_elevation_angle_deg,
                              compute_los_probability, compute_path_loss, compute_snr)
from .metrics import calculate_energy_consumption, calculate_interference_rate


def evaluate_sensitivity(uav_coords, ue_coords, weights, coverage_quantity='SNR',
                         threshold_db=18., min_alt=50., max_alt=300.):
    w=np.array([weights[k] for k in ('C','E','I')],dtype=float)
    if not np.isfinite(w).all() or (w<0).any() or not np.isclose(w.sum(),1):
        raise ValueError('Invalid weights')
    if coverage_quantity not in ('SNR','SINR'):
        raise ValueError('Unknown coverage quantity')
    distances=compute_distance_3d(uav_coords,ue_coords)
    angles=compute_elevation_angle_deg(uav_coords,ue_coords,distances)
    loss=compute_path_loss(distances,compute_los_probability(angles))
    snr=compute_snr(loss)
    # dBm -> mW; sum only other UAVs to avoid cancellation of strongest signal.
    rx=10.**((TRANSMIT_POWER_DBM-loss)/10.)
    noise=10.**(NOISE_POWER_DBM/10.)
    sinr=np.empty_like(rx)
    for i in range(len(rx)):
        sinr[i]=rx[i]/(noise+np.sum(np.delete(rx,i,axis=0),axis=0))
    snr_count=int(np.count_nonzero(np.max(snr,axis=0)>=threshold_db))
    sinr_count=int(np.count_nonzero(np.max(sinr,axis=0)>=10.**(threshold_db/10.)))
    total=len(ue_coords)
    energy=calculate_energy_consumption(uav_coords,min_alt=min_alt,max_alt=max_alt)
    overlap=calculate_interference_rate(snr,snr_th=threshold_db)
    c_snr,c_sinr=snr_count/total,sinr_count/total
    c=c_snr if coverage_quantity=='SNR' else c_sinr
    return dict(fitness=float(w[0]*c-w[1]*energy-w[2]*overlap),C=c,
                C_snr=c_snr,C_sinr=c_sinr,E=energy,I=overlap,
                ue_pass=snr_count if coverage_quantity=='SNR' else sinr_count,ue_total=total)
