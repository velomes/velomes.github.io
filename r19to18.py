
import json
import sys

team_codes = {
    "Ag2r La Mondiale": "ALM",
    "Astana Pro Team": "AST",
    "Bahrain-Merida": "TBM",
    "BMC Racing Team": "BMC",
    "BORA - hansgrohe": "BOH",
    "Bora-Hansgrohe": "BOH",
    "Groupama-FDJ": "GFC",
    "Lotto Soudal": "LTS",
    "Mitchelton-Scott": "MTS",
    "Movistar Team": "MOV",
    "Quick-Step Floors": "QST",
    "Deceuninck-Quick Step": "DQT",
    "Dimension Data": "DDD",
    "EF Education First-Drapac p/b Cannondale": "EFD",
    "Team Katusha - Alpecin": "TKA",
    "Team LottoNL-Jumbo": "TLJ",
    "Team Sky": "SKY",
    "Team Ineos": "INS",
    "Team Sunweb": "SUN",
    "Trek-Segafredo": "TFS",
    "UAE-Team Emirates": "UAD",
    "Fortuneo - Samsic": "FST",
    "Wanty - Groupe Gobert": "WGG",
    "Direct Energie": "TDE",
    "Cofidis Solutions Crédits": "COF",
    "Team Jumbo-Visma": "TJV",
    "EF Education First": "EF1",
    "CCC Team": "CCC",
    "UAE Team Emirates": "UAD",
    "Cofidis, solutions crédits": "COF",
    "Lotto-Soudal": "LTS",
    "Total Direct Energie": "TDE",
    "Team Katusha-Alpecin": "TKA",
    "Wanty-Gobert Cycling Team": "WGG",
    "Team Dimension Data": "TDD",
    "Team Arkéa-Samsic": "PCB"
}

def main():
    with open(sys.argv[1], 'r', encoding='utf8') as r:
        riders = json.load(r)

    riders18 = {}
    for team in riders:
        for rider in riders[team]:
            riders18[rider] = {'team': team_codes[team]}

    with open(sys.argv[1] + '.18', 'w') as w:
        json.dump(riders18, w)
    

if __name__ == '__main__':
    main()