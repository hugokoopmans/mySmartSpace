# Data Model: Vergaderruimte Reservering

Afgeleid uit de Key Entities en Functional Requirements in [spec.md](spec.md).

## Entiteit: Gebruiker

| Veld | Type | Regels |
|---|---|---|
| id | integer (PK) | — |
| naam | string | verplicht |
| rol | enum: `medewerker` \| `beheerder` | verplicht (FR-010) |
| demo_account_code | string (uniek) | vast, seed-data; geen zelfregistratie (FR-011) |

## Entiteit: Vergaderruimte

| Veld | Type | Regels |
|---|---|---|
| id | integer (PK) | — |
| naam | string | verplicht, uniek |
| capaciteit | integer | verplicht, > 0 |
| locatie | string | verplicht (FR-009) |
| verwijderd | boolean | default `false`; wordt nooit hard verwijderd zolang er actieve toekomstige reserveringen bestaan (FR-009a) |

**Verwijderregel (FR-009a)**: verwijderen van een ruimte is alleen toegestaan
wanneer er geen `Reservering` met status `actief` bestaat waarvan `eindtijd`
in de toekomst ligt voor deze ruimte.

## Entiteit: Reservering

| Veld | Type | Regels |
|---|---|---|
| id | integer (PK) | — |
| ruimte_id | integer (FK → Vergaderruimte) | verplicht |
| medewerker_id | integer (FK → Gebruiker) | verplicht; moet rol `medewerker` hebben |
| begintijd | datetime | verplicht; MOET in de toekomst liggen (FR-004a) |
| eindtijd | datetime | verplicht; MOET na `begintijd` liggen (FR-004) |
| status | enum: `actief` \| `gewijzigd` \| `geannuleerd` | initieel `actief` |
| aangemaakt_op | datetime | audit/historie (ondersteunt FR-008) |

**Validatieregels (afgedwongen in `reservation_service.py`, niet alleen in UI)**:

1. `begintijd < eindtijd` (FR-004).
2. `begintijd` ligt in de toekomst t.o.v. serverklok (FR-004a).
3. `begintijd` en `eindtijd` liggen beide binnen kantooruren 08:00–18:00
   (FR-004b).
4. Geen overlap: voor dezelfde `ruimte_id` mag geen andere reservering met
   status `actief` bestaan waarvan het interval `[begintijd, eindtijd)`
   overlapt met het gevraagde interval. Aansluitende intervallen (eindtijd A
   = begintijd B) zijn toegestaan (geen overlap; zie Edge Cases in spec.md).
5. Bij gelijktijdige aanvragen voor hetzelfde overlappende interval wint de
   eerst door de database verwerkte transactie; de tweede aanvraag krijgt een
   conflictfoutmelding (FR-003).
6. Wijzigen/annuleren is alleen toegestaan door de `medewerker_id` die de
   reservering heeft aangemaakt (FR-007).
7. Geannuleerde en verlopen reserveringen blijven raadpleegbaar in het
   overzicht van de medewerker (FR-008); records worden nooit hard verwijderd.

## State Transitions (Reservering.status)

```text
actief ──(wijzigen, nieuwe tijd geldig)──▶ gewijzigd
actief ──(annuleren)──▶ geannuleerd
gewijzigd ──(annuleren)──▶ geannuleerd
```

Geannuleerde reserveringen zijn eindstatus (geen verdere overgangen).
