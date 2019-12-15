# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:39:45 2019

@author: jonkro
"""

from tulip import spec, synth
import pickle

#%%

env_vars = {
    'goal': 'boolean',
    'safe_stopped': 'boolean',
    'sensor_failure': 'boolean',
    'driving': 'boolean',
    'upp_2_response': ['none', 'success'],
    'sstp_available': (1,1),
}

env_init = {
    '!goal',
    '!safe_stopped',
    '!sensor_failure',
    '!driving',
    'upp_2_response = "none"',
    'sstp_available = 1',
}

env_safe = {
    "sensor_failure -> sensor_failure'",
    '''!upp_2_request -> (upp_2_response' = "none")''',
    '''upp_2_request -> 
        ((upp_2_response' = "success"))''',
    ''' active_path = "sstp" -> sstp_available' > 0 ''',
    '''(!(driving & active_path="upp2") & !goal) -> !goal' ''',
    '''(!driving & goal) -> goal' ''',
    '''(!driving & safe_stopped) -> safe_stopped' ''',
    '''(active_path!="sstp" & !safe_stopped) -> !safe_stopped' ''',
    '''driving' -> active_path != "none"''',
    'goal -> !driving',
    'safe_stopped -> !driving',
    '''(!driving & active_path = "sstp") -> safe_stopped' ''',
}

env_prog = {
    '(active_path!="upp2" | sensor_failure) | goal',
    '(active_path!="sstp" | sstp_available = 0) | safe_stopped',
}

#%%

sys_vars = {
    'upp_2_request': 'boolean',
    'active_path': ['none', 'upp2', 'sstp'],
    'upp_2_available': 'boolean',
}

sys_init = {
    '!upp_2_request',
    'active_path = "none"',
    '!upp_2_available',
}

sys_safe = {
    '''active_path="sstp" -> sstp_available > 0''',
    '''(upp_2_response = "success") -> upp_2_available' ''',
    '''(upp_2_response != "success") -> (upp_2_available' <-> upp_2_available) ''',
    '''active_path = "upp2" -> (upp_2_available | upp_2_response = "success")''',
    '''safe_stopped -> (sensor_failure)''',
    '''safe_stopped -> !goal''',
    '''(active_path = "upp2" & driving') -> active_path' != "none" ''',
    '''goal -> active_path="none"''',
}

sys_prog = {
    'goal | safe_stopped',
    '!driving',
}

#%%

specs = spec.GRSpec(env_vars, sys_vars,
                    env_init, sys_init,
                    env_safe, sys_safe,
                    env_prog, sys_prog)
specs.qinit = '\E \A'
specs.moore = False
specs.plus_one = False

#%%

ctrl = synth.synthesize(specs, ignore_sys_init=False, ignore_env_init=False)

#%%

ctrl._transition_dot_label_format['separator'] = r'\n'
ctrl.save('supervisor_simple_sstp.pdf')


#%%

with open('synthesized_controller_simple_sstp.pickle', 'wb') as f:
    pickle.dump(ctrl, f)