#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:54:21 2019
Read raws, anonimize and save as BIDS
@author: sh254795
"""


#%%
import glob
import os.path as op
 
import mne
from mne_bids import write_raw_bids, make_bids_basename, write_anat
 
base_path = '/neurospin/meg/meg_tmp/Dynacomp_Ciuciu_2011/2019_MEG_Pipeline/MEG/'
subjects = ['SB01']
# subjects = ['SB01', 'SB02','SB03','SB04','SB05','SB06','SB07','SB08','SB09','SB10','SB11','SB12']

tasks = ['Localizer']

bids_root = '/neurospin/meg/meg_tmp/Dynacomp_Ciuciu_2011/2019_MEG_Pipeline/BIDS/'
subjects_dir = '/neurospin/meg/meg_tmp/Dynacomp_Ciuciu_2011/2019_MEG_Pipeline/MRI/'
trans_dir =  '/neurospin/meg/meg_tmp/Dynacomp_Ciuciu_2011/2019_MEG_Pipeline/MEG/trans/'
 
for ss, subject in enumerate(subjects):
    t1w = subjects_dir + "/%s/mri/T1.mgz" % subject
    trans = trans_dir + '/%s/Coregistration-trans.fif' % subject
    # Take care of MEG
    for task in tasks:
        raw_fname = op.join(base_path, subject, '%s_raw.fif' % task)
        raw = mne.io.read_raw_fif(raw_fname,allow_maxshield=True)
        raw.anonymize()
        raw.info['subject_info'] = dict(id=ss)
        bids_basename = make_bids_basename(subject=subject, task=task)
        events = mne.find_events(raw, min_duration=0.002, initial_event=True)
        write_raw_bids(raw, bids_basename,
                       output_path=bids_root,
                       events_data=events,
                       overwrite=True)
 
    # Take care of anatomy
    write_anat(bids_root, subject, t1w, acquisition="t1w",
               trans=trans, raw=raw, overwrite=True)        
