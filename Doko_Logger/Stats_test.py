from Pages.Datahandling.global_stats import Stats

stats = Stats(f".\\Test_Sessions\\")

print(stats.session_stats.keys())
print(stats.session_stats["A"])
print(stats.global_stats)