from bot.store import IntListStore, DictStore
from common.data import poll_groups_file, poll_candidates_file


enabled_groups = IntListStore(poll_groups_file)
poll_candidates = DictStore(poll_candidates_file)
