"""Static variables for generating data visualizations related to stop removal."""
__all__ = ("TOP_12_POSITIVE_DUMMY", "TOP_12_NEGATIVE_DUMMY",
           "TOP_12_POSITIVE_POP_DENSITY", "TOP_12_NEGATIVE_POP_DENSITY",
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
    ("Northern Lights", "Epic Staff C"),
    ("Woods", "Mid Town"),
    ("W Verona", "Westridge"),
    ("Airport", "Terminal Door 6"),
    ("E Verona", "Maple Grove"),
    ("Moorland", "Manor"),
    ("Mid Town", "Hawks Landing"),
    ("Cremer", "Park And Ride"),
    ("Mckee", "Commerce Park"),
    ("Mckee", "Seminole"),
    ("Pinehurst", "S Greenview"),
    ("Starr Grass", "S High Point"),
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

TOP_12_NEGATIVE_POP_DENSITY = [
    ("Northern Lights", "Epic Staff C"),
    ("Woods", "Mid Town"),
    ("Moorland", "Manor"),
    ("W Verona", "Westridge"),
    ("Airport", "Terminal Door 6"),
    ("E Verona", "Maple Grove"),
    ("Mckee", "Commerce Park"),
    ("Cremer", "Park And Ride"),
    ("Mid Town", "Hawks Landing"),
    ("Pinehurst", "S Greenview"),
    ("Starr Grass", "S High Point"),
    ("High Crossing", "Cross Hill"),
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
