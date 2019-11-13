# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:24:37 2019

@author: jonkro
"""

from tulip import spec, synth
import pickle

#%%

env_vars = {
    'goal': 'boolean',
    'safe_stopped': 'boolean',
    'emergency_stopped': 'boolean',
    'sensor_failure': 'boolean',
    'driving': 'boolean',
    'sstp_available': (0,1),
}

env_init = {
    '!goal',
    '!safe_stopped',
    '!emergency_stopped',
    '!sensor_failure',
    '!driving',
    'sstp_available = 1',
}

env_safe = {
    "sensor_failure -> sensor_failure'",
    ''' active_path = "sstp" -> sstp_available' > 0 ''',
    '''(!(driving & active_path="upp2") & !goal) -> !goal' ''',
    '''(!driving & goal) -> goal' ''',
    '''(!driving & safe_stopped) -> safe_stopped' ''',
    '''(active_path!="sstp" & !safe_stopped) -> !safe_stopped' ''',
    '''(!driving & emergency_stopped) -> emergency_stopped' ''',
    '''(active_path!="aeb" & !emergency_stopped) -> !emergency_stopped' ''',
    '''driving' -> active_path != "none"''',
    'goal -> !driving',
    'safe_stopped -> !driving',
    'emergency_stopped -> !driving',
    '''(!driving & active_path = "sstp") -> safe_stopped' ''',
    '''(!driving & active_path = "aeb") -> emergency_stopped' ''',
}

env_prog = {
    '(active_path!="upp2" | sensor_failure) | goal',
    '(active_path!="sstp" | sstp_available = 0) | safe_stopped',
    'active_path!="aeb" | emergency_stopped',
}

#%%

sys_vars = {
    'active_path': ['none', 'upp2', 'sstp', 'aeb'],
}

sys_init = {
    'active_path = "none"',
}

sys_safe = {
    '''active_path="sstp" -> sstp_available > 0''',
    '''safe_stopped -> (sensor_failure)''',
    '''safe_stopped -> !goal''',
    '''emergency_stopped -> (sensor_failure)''',
    '''emergency_stopped -> !goal''',
    '''emergency_stopped -> !safe_stopped''',
    '''(active_path = "upp2") -> active_path' != "none" '''
}

sys_prog = {
    'goal | safe_stopped | emergency_stopped',
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
ctrl.save('supervisor_simple_aeb.pdf')


#%%

with open('synthesized_controller_simple_aeb.pickle', 'wb') as f:
    pickle.dump(ctrl, f)