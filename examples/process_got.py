import json


def get_json_from_file(file_name, top_element_remove=None):

    with open(file_name, "r") as in_file:
        result = json.load(in_file)

        if top_element_remove:
            result = result[top_element_remove]

    return result


def get_episodes():
    fn = "/Users/donaldferguson/Dropbox/000/000-Data/GoT/episodes.json"
    result = get_json_from_file(fn, "episodes")
    return result


def get_episodes_basics(episodes):

    basic_keys = ['seasonNum', 'episodeNum', 'episodeTitle', 'episodeLink',
                  'episodeAirDate', 'episodeDescription'
                  ]
    result = []

    for e in episodes:
        new_e = {k:e[k] for k in basic_keys}
        result.append(new_e)

    return result

def get_episodes_basics_location(episodes):

    result = []

    for e in episodes:
        locations = e.get('openingSequenceLocations', None)

        if locations:
            for l in locations:
                new_l = {
                    "seasonNum": e["seasonNum"],
                    "episodeNum": e["episodeNum"],
                    "openingSequenceLocation": l
                }
                result.append(new_l)

    return result

def get_episodes_basics_scenes(episodes):

    result = []

    for e in episodes:
        scenes = e.get('scenes', None)

        if scenes:
            for i in range(0, len(scenes)):
                t = scenes[i]
                new_s = {
                    "seasonNum": e["seasonNum"],
                    "episodeNum": e["episodeNum"],
                    "sceneNum": i,
                    "sceneStart": t["sceneStart"],
                    "sceneEnd": t["sceneEnd"],
                    "sceneLocation": t.get("location", None),
                    "sceneSubLocation": t.get("subLocation", None)

                }
                result.append(new_s)

    return result


def get_episodes_basics_scenes_characters(episodes):

    result = []

    for e in episodes:
        scenes = e.get('scenes', None)

        if scenes:
            for i in range(0, len(scenes)):
                t = scenes[i]
                characters = t.get('characters', None)

                for c in characters:
                    new_c = {
                        "seasonNum": e["seasonNum"],
                        "episodeNum": e["episodeNum"],
                        "sceneNum": i,
                        "characterName": c["name"]
                    }
                    result.append(new_c)

    return result



def process_episodes():
    episodes = get_episodes()
    episodes_basics = get_episodes_basics(episodes)
    with open("./episodes_basics.json", "w") as out_file:
        json.dump(episodes_basics, out_file, indent=2)

def process_locations():
    episodes = get_episodes()
    episodes_locations = get_episodes_basics_location(episodes)
    with open("./episodes_locations.json", "w") as out_file:
        json.dump(episodes_locations, out_file, indent=2)


def process_scenes():
    episodes = get_episodes()
    scenes = get_episodes_basics_scenes(episodes)
    with open("./episodes_scenes.json", "w") as out_file:
        json.dump(scenes, out_file, indent=2)


def process_characters():
    episodes = get_episodes()
    characters = get_episodes_basics_scenes_characters(episodes)
    with open("./episodes_characters.json", "w") as out_file:
        json.dump(characters, out_file, indent=2)


if __name__ == "__main__":
    process_episodes()
    process_locations()
    process_scenes()
    process_characters()
