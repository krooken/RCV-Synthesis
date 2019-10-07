# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 10:16:43 2019

@author: jonkro
"""

from tulip import spec, synth
import pickle


#%%

env_vars = {
    'goal': 'boolean',
    'upp_2_response': ['none', 'success'],
    'driving': 'boolean',
}

env_init = {
    '!goal',
    'upp_2_response = "none"',
    '!driving',
}

env_safe = {
    '''!upp_2_request->(upp_2_response' = "none")''',
    '''upp_2_request->((upp_2_response' = "success"))''',
    '''(!driving & !goal) -> !goal' ''',
    '''(!driving & goal) -> goal' ''',
    '''driving' -> active_path != "none"''',
    '''goal -> !driving''',
}

env_prog = {
    'active_path != "upp2" | goal',
}


#%%

sys_vars = {
    'upp_2_request': 'boolean',
    'active_path': ['none', 'upp2'],
    'upp_2_available': 'boolean',
}

sys_init = {
    '!upp_2_request',
    'active_path = "none"',
    '!upp_2_available',
}

sys_safe = {
    "upp_2_request->!upp_2_request'",
    '''(upp_2_response="success") -> upp_2_available' ''',
    '''(upp_2_response!="success") -> (upp_2_available'<->upp_2_available) ''',
    '''active_path="upp2" -> (upp_2_available | upp_2_response="success")''',
}

sys_prog = {
    'goal',
    '!driving',
}


#%%

specs = spec.GRSpec(env_vars, sys_vars,
                    env_init, sys_init,
                    env_safe, sys_safe,
                    env_prog, sys_prog)
specs.qinit = '\E \A'
specs.moore = False
specs.plus_one = True


#%%

ctrl = synth.synthesize(specs, ignore_sys_init=False, ignore_env_init=False)

#%%

ctrl._transition_dot_label_format['separator'] = r'\n'
ctrl.save('supervisor_simple_upp2.pdf')


#%%

with open('synthesized_controller_simple_upp2.pickle', 'wb') as f:
    pickle.dump(ctrl, f)
