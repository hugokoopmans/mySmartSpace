# SmartSpace - Reserveringssysteem voor vergaderruimtes en werkplekken

## Achtergrond

Binnen de organisatie bestaat behoefte aan een centrale oplossing voor het reserveren van vergaderruimtes en op termijn mogelijk ook flexwerkplekken.

De AI-training wordt gebruikt om niet alleen kennis op te doen met Spec-Driven Development en AI-assisted softwareontwikkeling, maar tevens om een eerste versie van de productspecificatie, architectuur en implementatievoorstellen voor deze oplossing op te stellen.

De casus heeft daarmee een daadwerkelijk bedrijfsdoel en is geen puur fictieve trainingsopdracht.

## Doelstelling

Tijdens de trainingsdagen werken deelnemers gezamenlijk aan:

- een gevalideerde productspecificatie;
- een eerste systeemontwerp;
- een backlog;
- een technisch prototype;
- een set architectuur- en ontwerpbeslissingen.

De opgeleverde artefacten moeten na afloop bruikbaar zijn als startpunt voor een eventuele daadwerkelijke realisatie.

## Productvisie

Ontwikkel een webapplicatie waarmee medewerkers:

- beschikbare vergaderruimtes kunnen raadplegen;
- vergaderruimtes kunnen reserveren;
- reserveringen kunnen wijzigen of annuleren;
- een overzicht van eigen reserveringen kunnen bekijken.

De oplossing moet zodanig worden ontworpen dat later ook werkplekken kunnen worden opgenomen binnen hetzelfde platform.

## Eerste Release Scope

### Vergaderruimtes

Functionaliteit:

- Beschikbare ruimtes bekijken
- Reservering aanmaken
- Reservering wijzigen
- Reservering annuleren
- Eigen reserveringen bekijken
- Voorkomen van dubbele boekingen

### Beheer

- Ruimtes configureren
- Capaciteit vastleggen
- Locatie vastleggen

## Mogelijke Vervolguitbreiding

Niet in de eerste release maar wel meenemen in ontwerp- en architectuurkeuzes:

- Werkplekreserveringen
- Check-in / check-out
- Integratie met Outlook
- Integratie met Microsoft Teams
- Koppeling met Microsoft Graph
- Bezettingsrapportages
- Capaciteitsanalyse

## Belangrijkste Businessregels

- Een ruimte kan slechts eenmaal tegelijk gereserveerd zijn.
- Een reservering heeft een begin- en eindtijd.
- De eindtijd moet na de begintijd liggen.
- Dubbele reserveringen zijn niet toegestaan.
- Historische reserveringen blijven raadpleegbaar.
