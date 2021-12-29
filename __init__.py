from os.path import join, dirname

import radiosoma
from ovos_utils.parse import fuzzy_match
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    MediaType, PlaybackType, ocp_search, MatchConfidence, ocp_featured_media


class SomaFMSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__("SomaFM")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.MUSIC,
                                MediaType.RADIO]
        self.skill_icon = join(dirname(__file__), "ui", "somafm.png")

    @ocp_featured_media()
    def featured_media(self):
        return [{
            "match_confidence": 90,
            "media_type": MediaType.RADIO,
            "uri": ch.direct_stream,
            "playback": PlaybackType.AUDIO,
            "image": ch.image,
            "bg_image": ch.image,
            "skill_icon": self.skill_icon,
            "title": ch.title,
            "author": "SomaFM",
            "length": 0
        } for ch in radiosoma.get_stations()]

    @ocp_search()
    def ocp_somafm_playlist(self, phrase):
        phrase = self.remove_voc(phrase, "radio")
        if self.voc_match(phrase, "somafm", exact=True):
            yield {
                "match_confidence": 100,
                "media_type": MediaType.RADIO,
                "playlist": self.featured_media(),
                "playback": PlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "image": "https://somafm.com/img3/LoneDJsquare400.jpg",
                "bg_image": "https://somafm.com/about/pics/IMG_0974.jpg",
                "title": "SomaFM (All stations)",
                "author": "SomaFM"
            }

    @ocp_search()
    def search_somafm(self, phrase, media_type):
        base_score = 0

        if media_type == MediaType.RADIO:
            base_score += 20
        else:
            base_score -= 30

        if self.voc_match(phrase, "radio"):
            base_score += 10
            phrase = self.remove_voc(phrase, "radio")

        if self.voc_match(phrase, "somafm"):
            base_score += 30  # explicit request
            phrase = self.remove_voc(phrase, "somafm")

        for ch in radiosoma.get_stations():
            score = base_score + \
                    fuzzy_match(ch.title.lower(), phrase.lower()) * 100
            if score <= MatchConfidence.AVERAGE_LOW:
                continue
            yield {
                "match_confidence": min(100, score),
                "media_type": MediaType.RADIO,
                "uri": ch.direct_stream,
                "playback": PlaybackType.AUDIO,
                "image": ch.image,
                "bg_image": ch.image,
                "skill_icon": self.skill_icon,
                "title": ch.title,
                "author": "SomaFM",
                "length": 0
            }


def create_skill():
    return SomaFMSkill()
