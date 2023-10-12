import logging
from mod_poll import *
from func_general import *
from func_private import *
from bot_auth import ensure_not_bl


group_functions = [
    repeat,
    title,
    enable_group,
    disable_group,
    apply_add_to_candidates,
    apply_delete_from_candidates
]

private_functions = [
    private_start,
    private_forward,
    private_help,
    # restart,
    private_get_file_id,
    private_unknown
]

universal_functions = [
    debug,
    delay
]

all_functions = group_functions + private_functions + universal_functions

for function in all_functions:
    logging.info(f'Function {function.__name__} adding decorator "ensure_not_bl"')
    function = ensure_not_bl(function)
