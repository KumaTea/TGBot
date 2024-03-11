from bot.store import DictStore, IntListStore
from common.data import poll_groups_file, poll_candidates_file


enabled_groups = IntListStore(poll_groups_file)
poll_candidates = DictStore(poll_candidates_file)
