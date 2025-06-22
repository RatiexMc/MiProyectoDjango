from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

USERS = [
    ('andrea', 'andrea@gmail.com', 'andrea123'),
    ('ana', 'ana@gmail.com', 'ana123'),
    ('nuria', 'nuria@gmail.com', 'nuria123'),
    ('antonella', 'antonella@gmail.com', 'antonella123'),
    ('anabella', 'anabella@gmail.com', 'anabella123'),
    ('pedro', 'pedro@gmail.com', 'pedro123'),
    ('jose', 'jose@gmail.com', 'jose123'),
    ('marcos', 'marcos@gmail.com', 'marcos123'),
    ('junior', 'junior@gmail.com', 'junior123'),
    ('laura', 'laura@gmail.com', 'laura123'),
    ('paula', 'paula@gmail.com', 'paula123'),
    ('osmar', 'osmar@gmail.com', 'osmar123'),
    ('lourdes', 'lourdes@gmail.com', 'lourdes123'),
    ('daniel', 'daniel@gmail.com', 'daniel123'),
    ('kevin', 'kevin@gmail.com', 'kevin123'),
    ('maria', 'maria@gmail.com', 'maria123'),
    ('dahiana', 'dahiana@gmail.com', 'dahiana123'),
    ('cecilia', 'cecilia@gmail.com', 'cecilia123'),
    ('clarisse', 'clarisse@gmail.com', 'clarisse123'),
    ('larisa', 'larisa@gmail.com', 'larisa123'),
    ('yuri', 'yuri@gmail.com', 'yuri123'),
    ('vilma', 'vilma@gmail.com', 'vilma123'),
    ('agustina', 'agustina@gmail.com', 'agustina123'),
    ('Micaela', 'micaela@gmail.com', 'micaela123'),
    ('Francisco', 'francisco@gmail.com', 'francisco123'),
    ('Sofia', 'sofia@gmail.com', 'sofia123'),
    ('juan', 'juan@gmail.com', 'juan123'),
    ('fede', 'fede@gmail.com', 'fede123'),
    ('marta', 'marta@gmail.com', 'marta123'),
    ('fatima', 'fatima@gmail.com', 'fatima123'),
    ('blanca', 'blanca@gmail.com', 'blanca123'),
    ('mateo', 'mateo@gmail.com', 'mateo123'),
    ('lucas', 'lucas@gmail.com', 'lucas123'),
    ('richard', 'richard@gmail.com', 'richard123'),
    ('justin', 'justin@gmail.com', 'justin123'),
    ('tobias', 'tobias@gmail.com', 'tobias123'),
    ('roberto', 'roberto@gmail.com', 'roberto123'),
    ('lourdez', 'lourdez@gmail.com', 'lourdez123'),
    ('arturo', 'arturo@gmail.com', 'arturo123'),
    ('matias', 'matias@gmail.com', 'matias123')
]

class Command(BaseCommand):
    help = "Populate the database with predefined users"

    def handle(self, *args, **options):
        for user_data in USERS:
            if len(user_data) != 3:
                self.stdout.write(self.style.ERROR(f"Entrada inválida: {user_data}"))
                continue

            username, email, password = user_data

            if not username or not email or not password:
                self.stdout.write(self.style.ERROR(
                    f"Datos faltantes en: username='{username}', email='{email}', password='{password}'"
                ))
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists"))
                continue

            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}'"))
