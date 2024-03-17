from bot.store import DictStore, IntSetStore
from common.data import poll_groups_file, poll_candidates_file


enabled_groups = IntSetStore(poll_groups_file)
poll_candidates = DictStore(poll_candidates_file)
