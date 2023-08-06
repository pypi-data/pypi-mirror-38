import csv

from django.core.management.base import BaseCommand
from election.models import Race, CandidateElection
from itertools import chain


class Command(BaseCommand):
    def handle(self, *args, **options):
        races = Race.objects.filter(
            cycle__slug="2018", special=False
        ).order_by("office__label")

        scorecard = []
        tossups = []

        for race in races:
            print(race)
            rating = race.ratings.latest("created_date")
            rating_party = rating.category.label.split(" ")[-1]

            try:
                election = race.elections.get(election_day__slug="2018-11-06")
            except:
                continue

            candidate_elections = CandidateElection.objects.filter(
                election=election
            )
            winner = None
            for ce in candidate_elections:
                print(ce.candidate.person.full_name)

                try:
                    ce.votes.get(division__level__name="state")
                except:
                    continue

                if ce.votes.get(division__level__name="state").winning:
                    winner = ce.candidate.party.label

            if winner == "Independent":
                winner = "Democrat"

            if not winner:
                continue

            if rating_party != "Toss-Up":
                scorecard.append(
                    {
                        "race": race.office.label,
                        "rating": rating_party,
                        "winner": winner,
                        "correct": rating_party == winner,
                    }
                )
            else:
                tossups.append({"race": race.office.label, "winner": winner})

        correct = [r["race"] for r in scorecard if r["correct"]]

        dem_tossups = [r["race"] for r in tossups if r["winner"] == "Democrat"]
        gop_tossups = [
            r["race"] for r in tossups if r["winner"] == "Republican"
        ]

        print(len(correct), len(scorecard))
        print(dem_tossups, gop_tossups)

        with open("scorecard.csv", "w") as f:
            fieldnames = ["race", "rating", "winner", "correct"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for row in scorecard:
                writer.writerow(row)
