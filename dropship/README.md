# Dropship Bundles Platform

Applicazione Django che permette di presentare e vendere bundle tematici in dropshipping, pensata per utenti senza background tecnico.

## Funzionalità principali
- Registrazione utenti con nome, cognome, email e numero di telefono.
- Invio email di conferma con link di attivazione e attivazione dell'account.
- Recupero password tramite email.
- Catalogo di bundle con dettaglio dei prodotti inclusi, pensato per combinare articoli da marketplace differenti.
- Interfaccia responsive con palette colori blu/teal per trasmettere affidabilità.

## Requisiti
- Python 3.11+
- Pip

## Installazione
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

L'applicazione usa per default il backend email `console`, che stampa il contenuto delle email nel terminale. Per utilizzare un provider reale imposta le variabili d'ambiente:

```bash
export EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
export EMAIL_HOST="smtp.example.com"
export EMAIL_HOST_USER="user@example.com"
export EMAIL_HOST_PASSWORD="your-password"
export EMAIL_PORT=587
export EMAIL_USE_TLS=True
export DEFAULT_FROM_EMAIL="Dropship Bundles <noreply@example.com>"
export SITE_DOMAIN="dropship.example.com"
export USE_HTTPS=True
```

## Creazione di dati demo
Puoi caricare un set di esempio e accedere al pannello admin per personalizzarlo:
```bash
python manage.py loaddata bundles/fixtures/sample_bundles.json
python manage.py createsuperuser
```

Poi accedi a `http://localhost:8000/admin/` per inserire nuovi bundle e articoli o modificarli.

## Esecuzione dei test
```bash
python manage.py test
```
