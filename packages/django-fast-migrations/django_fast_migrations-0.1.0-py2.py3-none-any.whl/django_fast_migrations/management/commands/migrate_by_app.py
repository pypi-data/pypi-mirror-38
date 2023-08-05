# -*- encoding: utf-8 -*-

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.migrations.loader import MigrationLoader
from django.db import DEFAULT_DB_ALIAS, connections


class Command(BaseCommand):
    """
    Check if there are pending migrations.
    If there are pending migrations it's possible apply them
    by executing this command with the param --execute
    """

    help = "Verify if there are migrations left and if so, execute them"

    def add_arguments(self, parser):

        parser.add_argument('--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
                            help='Nominates a database to synchronize. Defaults to the "default" database.')

        parser.add_argument('--execute', action='store_true', dest='execute', default=False,
                            help='Execute the migrations if pending, application by application')

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        self.stdout.write(' Verifying if the are migrations left '.center(100, '='))

        # Get the database we're operating from
        db = options.get('database')
        execute_if_pending = options.get('execute')
        connection = connections[db]

        # process the apps in order to see if there are pending applications
        pending_apps = self.verify_pending(connection)

        if not pending_apps:
            self.stdout.write(' End of the process: not apps pending '.center(100, '='))
            return

        if not execute_if_pending:
            # only warning that there are applications with pending migrations
            raise CommandError('There are this apps: {} with pending migrations'.format(pending_apps))

        # at this point apps with pending migrations exists and proceed to execute them
        self.stdout.write('Migrating the apps: {}'.format(pending_apps).center(100, '.'))
        for app_name in pending_apps:
            self.stdout.write('Custom migrating app: ==={}==='.format(app_name))
            call_command('migrate', app_name)

        self.stdout.write(' End of the process: applied migrations '.center(100, '='))

    def verify_pending(self, connection):
        """
        Obtains the ordered list of apps with pending migrations

        :param connection:
        :return:
        """
        # Load migrations from disk/DB
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        graph = loader.graph

        # Generate the plan
        plan = []
        seen = set()
        for target in graph.leaf_nodes():
            for migration in graph.forwards_plan(target):
                if migration not in seen:
                    node = graph.node_map[migration]
                    plan.append(node)
                    seen.add(migration)

        apps_by_order = []
        for node in plan:
            if node.key in loader.applied_migrations:
                continue
            app_name = node.key[0]
            if app_name not in apps_by_order:
                apps_by_order.append(app_name)

        if self.verbosity >= 2:
            self.stdout.write(' Showing pending apps by order '.center(100, '='))
            self.stdout.write('{}'.format(apps_by_order))
            if loader.applied_migrations:
                self.stdout.write(' Already applied '.center(100, '='))
                self.stdout.write('{}'.format(loader.applied_migrations))

        return apps_by_order
