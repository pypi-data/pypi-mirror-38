from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Calls all upstream bootstrap commands and election commands"

    def handle(self, *args, **options):
        print("Bootstrapping election")
        call_command("bootstrap_geography")
        call_command("bootstrap_jurisdictions")
        call_command("bootstrap_fed")
        call_command("bootstrap_offices")
        call_command("bootstrap_parties")
        call_command("bootstrap_election_events")
        call_command("schedule_elections")
