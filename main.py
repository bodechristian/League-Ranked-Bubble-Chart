from riotwatcher import LolWatcher
from KEY import AUTHKEY
from collections import defaultdict
from bubble_chart import C

import matplotlib.pyplot as plt
import numpy as np

import os


def get_champion_frequencies(_mode: str, name: str, region: str = 'euw1') -> list:
    watcher = LolWatcher(AUTHKEY)
    player_profile = watcher.summoner.by_name(region, name)
    matches = []
    i = 0
    while True:
        # queueID:420 is ranked solo
        match_batch = watcher.match.matchlist_by_puuid(region, player_profile['puuid'], start=i, count=100, queue=420)
        if not match_batch:
            break
        matches.extend(match_batch)
        i += 100

    champion_freqs = defaultdict(int)
    champs = []
    for i, match_id in enumerate(matches):
        print(f"Getting match data of match number {i+1}/{len(matches)}.")
        match_details = watcher.match.by_id(region, match_id)
        participants = match_details["info"]["participants"]
        champ = [el for el in participants if el["puuid"] == player_profile['puuid']][0]["championName"]
        champs.append(champ)
        champion_freqs[champ] += 1
    return champs


def visualize_frequencies(_freqs: list, _name: str) -> None:
    lbls, count = np.unique(_freqs, return_counts=True)

    c = C(count, lbls)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    ax.axis("off")
    c.minimize()
    c.plot(ax)
    ax.relim()
    ax.autoscale_view()
    plt.title(f"Last {len(_freqs)} Ranked Games by {_name}")
    plt.savefig(os.path.join("images", f"{_name}_last{len(_freqs)}.png"))

    #plt.show()
    #vis_bar_plot(lbls, count)


def vis_bar_plot(_labels, _counts):
    # bar plot histogram style
    fig, ax = plt.subplots(figsize=(12, 6))
    plot = ax.bar(_labels, _counts, align='center')
    for i in range(0, len(_labels), 2):
        plot[i].set_color('r')
    ax.set_xticklabels(_labels)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(os.path.join("images", 'temp.png'))
    plt.show()


if __name__ == '__main__':
    names = ["theFFM", "Fresh Funky Papa", "Fresh Funky Mama", "McSwagster"]
    for name in names:
        freqs = get_champion_frequencies("ranked", name)
        visualize_frequencies(freqs, name)

