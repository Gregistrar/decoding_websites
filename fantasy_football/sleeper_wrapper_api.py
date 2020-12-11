from sleeper_wrapper import League
from sleeper_wrapper import Stats


league = League(601091358869999616)
league.get_league()

league.get_users()


stats = Stats()
stats.get_all_stats("regular", "2020")
stats.get_week_stats("regular", "2020", "1")



