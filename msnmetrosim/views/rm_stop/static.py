"""Static variables for generating data visualizations related to stop removal."""
__all__ = ("TOP_12_POSITIVE_DUMMY", "TOP_12_NEGATIVE_DUMMY",
           "TOP_12_POSITIVE_POP_DENSITY",
           "IMPACT_REPORT_HEADER")

TOP_12_POSITIVE_DUMMY = [
    ("W Terrace", "5117"),
    ("N Thompson", "Jana"),
    ("W Terrace", "Eastpark"),
    ("N Thompson", "Westwynn"),
    ("S Whitney", "Gilbert"),
    ("Hathaway", "Greenwich"),
    ("Commercial", "North Lawn"),
    ("Oak", "E Washington"),
    ("S Gammon", "Gammon"),
    ("Fish Hatchery", "W Badger"),
    ("Caddis", "Cahill"),
    ("Anniversary", "Forest Run")
]

TOP_12_NEGATIVE_DUMMY = [
    ("Starr Grass", "S High Point"),
    ("Pinehurst", "S Greenview"),
    ("Mckee", "Seminole"),
    ("Mckee", "Commerce Park"),
    ("Cremer", "Park And Ride"),
    ("Mid Town", "Hawks Landing"),
    ("Moorland", "Manor"),
    ("E Verona", "Maple Grove"),
    ("Airport", "Terminal Door 6"),
    ("W Verona", "Westridge"),
    ("Woods", "Mid Town"),
    ("Northern Lights", "Epic Staff C"),
]

TOP_12_POSITIVE_POP_DENSITY = [
    ("W Terrace", "Eastpark"),
    ("Waldorf", "Mansion Hill"),
    ("N Thompson", "Jana"),
    ("N Fair Oaks", "Lexington"),
    ("N Thompson", "Westwynn"),
    ("Eastpark", "Broadview"),
    ("S Whitney", "Gilbert"),
    ("North Transfer Point", "Huxley"),
    ("Rayovac", "Exact"),
    ("S Whitney", "Kroncke"),
    ("Anniversary", "Forest Run"),
    ("Hathaway", "Schroeder")
]

IMPACT_REPORT_HEADER = [
    "rank",
    "cross_1",
    "cross_2",
    "impact_index",
    "generated_time",
    "agent_range",
    "agent_interval"
]
