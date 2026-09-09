# Feature Specification: Vergaderruimte Reservering

**Feature Branch**: `001-vergaderruimte-reservering`

**Created**: 2026-09-09

**Status**: Draft

**Input**: User description: "Reserveringssysteem voor vergaderruimtes: medewerkers kunnen beschikbare vergaderruimtes raadplegen, reserveren, wijzigen, annuleren en hun eigen reserveringen bekijken. Dubbele boekingen worden voorkomen. Beheerders kunnen ruimtes, capaciteit en locatie configureren." (bron: docs/original-plan.md)

## Clarifications

### Session 2026-09-09

- Q: Wat moet er gebeuren als een beheerder een ruimte probeert te verwijderen waarvoor nog toekomstige reserveringen bestaan? → A: Verwijderen wordt geblokkeerd zolang er actieve toekomstige reserveringen zijn.
- Q: Gelden er vaste openingstijden waarbinnen vergaderruimtes reserveerbaar zijn? → A: Ja, vaste kantooruren 08:00-18:00.
- Q: Mag een medewerker een reservering aanmaken met een begintijd die al in het verleden ligt? → A: Nee, de begintijd moet in de toekomst liggen.
- Q: Hoe lost het systeem twee gelijktijdige boekingspogingen voor dezelfde ruimte/tijdslot op? → A: Eerste aanvraag wint; de tweede krijgt een foutmelding (geborgd via een database-constraint).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Vergaderruimte reserveren (Priority: P1)

Als medewerker wil ik beschikbare vergaderruimtes kunnen raadplegen en een ruimte
reserveren voor een specifieke periode, zodat ik zeker weet dat de ruimte er is
wanneer ik hem nodig heb.

**Why this priority**: Dit is de kernwaarde van de applicatie; zonder deze
functionaliteit heeft het systeem geen bestaansrecht.

**Independent Test**: Kan volledig getest worden door als medewerker in te loggen,
een vrije ruimte te zoeken op tijdstip, deze te reserveren en de reservering
terug te zien in het eigen overzicht.

**Acceptance Scenarios**:

1. **Given** een medewerker is ingelogd, **When** hij een beschikbare ruimte
   selecteert met een begin- en eindtijd, **Then** wordt de reservering
   vastgelegd en verschijnt deze in zijn overzicht van eigen reserveringen.
2. **Given** een ruimte is al gereserveerd voor een tijdsinterval, **When** een
   andere medewerker dezelfde ruimte voor een overlappend interval probeert te
   reserveren, **Then** weigert het systeem de reservering en toont het een
   duidelijke foutmelding.
3. **Given** een medewerker kiest een eindtijd die vóór of gelijk aan de
   begintijd ligt, **When** hij de reservering probeert te bevestigen, **Then**
   weigert het systeem de reservering met een validatiemelding.

---

### User Story 2 - Reservering wijzigen of annuleren (Priority: P2)

Als medewerker wil ik een eigen reservering kunnen wijzigen of annuleren, zodat
mijn planning up-to-date blijft wanneer een vergadering verplaatst of komt te
vervallen.

**Why this priority**: Volgt direct op het aanmaken van reserveringen en is
noodzakelijk voor een bruikbaar systeem, maar de kernwaarde (P1) kan zonder
deze functie al gedemonstreerd worden.

**Independent Test**: Kan getest worden door een bestaande reservering te
wijzigen naar een ander (vrij) tijdstip, en apart door een reservering te
annuleren en te controleren dat de ruimte weer beschikbaar is.

**Acceptance Scenarios**:

1. **Given** een medewerker heeft een eigen actieve reservering, **When** hij de
   tijd wijzigt naar een tijdslot waarin de ruimte vrij is, **Then** wordt de
   reservering bijgewerkt.
2. **Given** een medewerker heeft een eigen actieve reservering, **When** hij
   deze annuleert, **Then** wordt de reservering als geannuleerd gemarkeerd en
   wordt de ruimte voor dat tijdslot weer beschikbaar voor anderen.
3. **Given** een medewerker probeert een reservering van een andere medewerker
   te wijzigen of annuleren, **When** hij deze actie uitvoert, **Then** weigert
   het systeem dit.

---

### User Story 3 - Eigen reserveringen overzien (Priority: P2)

Als medewerker wil ik een overzicht van al mijn (toekomstige en historische)
reserveringen kunnen bekijken, zodat ik weet welke afspraken ik heb vastgelegd.

**Why this priority**: Ondersteunt gebruiksgemak en controle, en is een
randvoorwaarde om reserveringen te kunnen wijzigen/annuleren (Story 2).

**Independent Test**: Kan getest worden door meerdere reserveringen aan te
maken en te controleren dat ze allemaal (inclusief geannuleerde en verlopen)
correct getoond worden in het overzicht.

**Acceptance Scenarios**:

1. **Given** een medewerker heeft meerdere reserveringen gemaakt, **When** hij
   zijn overzicht opent, **Then** ziet hij al zijn reserveringen met status
   (actief/gewijzigd/geannuleerd) en tijdstip.
2. **Given** een reservering ligt in het verleden, **When** de medewerker zijn
   overzicht bekijkt, **Then** blijft deze historische reservering raadpleegbaar.

---

### User Story 4 - Vergaderruimtes beheren (Priority: P3)

Als beheerder wil ik vergaderruimtes kunnen configureren (naam, capaciteit,
locatie), zodat medewerkers kunnen kiezen uit een actuele lijst van bruikbare
ruimtes.

**Why this priority**: Noodzakelijk voordat er iets te reserveren valt, maar in
een eerste demo kunnen ruimtes ook vooraf via een vast seed-bestand worden
aangemaakt; daarom lager geprioriteerd dan de medewerkersflows.

**Independent Test**: Kan getest worden door als beheerder in te loggen, een
nieuwe ruimte aan te maken met capaciteit en locatie, en te controleren dat
deze ruimte vervolgens zichtbaar en reserveerbaar is voor medewerkers.

**Acceptance Scenarios**:

1. **Given** een beheerder is ingelogd, **When** hij een nieuwe ruimte aanmaakt
   met naam, capaciteit en locatie, **Then** is deze ruimte beschikbaar voor
   medewerkers om te reserveren.
2. **Given** een beheerder past de capaciteit of locatie van een bestaande
   ruimte aan, **When** hij de wijziging opslaat, **Then** zijn bestaande
   reserveringen voor die ruimte onaangetast en zien medewerkers de bijgewerkte
   gegevens.

### Edge Cases

- Wat gebeurt er als een medewerker een reservering probeert te wijzigen naar
  een tijdslot dat inmiddels door iemand anders is geboekt? (Systeem moet dit
  weigeren, zelfde regel als bij aanmaken.)
- Een beheerder kan een ruimte met actieve toekomstige reserveringen niet
  verwijderen; het systeem weigert de verwijdering (zie Clarifications).
- Hoe gaat het systeem om met reserveringen die exact op elkaar aansluiten
  (eindtijd van de ene reservering = begintijd van de volgende)? Dit is
  toegestaan (geen overlap).
- Een reservering buiten kantooruren (vóór 08:00 of na 18:00) wordt geweigerd.
- Een reservering met een begintijd in het verleden wordt geweigerd.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Medewerkers MOETEN een lijst van vergaderruimtes met hun
  beschikbaarheid voor een gekozen periode kunnen raadplegen.
- **FR-002**: Medewerkers MOETEN een beschikbare ruimte kunnen reserveren door
  een begin- en eindtijd op te geven.
- **FR-003**: Het systeem MOET een reservering weigeren wanneer de gekozen
  ruimte voor (een deel van) het gevraagde tijdsinterval al gereserveerd is;
  bij gelijktijdige aanvragen voor hetzelfde tijdslot wint de eerst verwerkte
  aanvraag en krijgt de tweede een foutmelding.
- **FR-004**: Het systeem MOET vereisen dat de eindtijd van een reservering na
  de begintijd ligt.
- **FR-004a**: Het systeem MOET vereisen dat de begintijd van een reservering
  in de toekomst ligt (reserveren in het verleden is niet toegestaan).
- **FR-004b**: Het systeem MOET een reservering weigeren wanneer het gevraagde
  tijdsinterval buiten de kantooruren (08:00-18:00) valt.
- **FR-005**: Medewerkers MOETEN hun eigen reserveringen kunnen wijzigen,
  waarbij dezelfde overlap- en tijdvalidatie geldt als bij het aanmaken.
- **FR-006**: Medewerkers MOETEN hun eigen reserveringen kunnen annuleren.
- **FR-007**: Medewerkers MOGEN alleen hun eigen reserveringen wijzigen of
  annuleren, niet die van anderen.
- **FR-008**: Medewerkers MOETEN een overzicht kunnen bekijken van al hun
  reserveringen, inclusief historische (verlopen of geannuleerde) reserveringen.
- **FR-009**: Beheerders MOETEN vergaderruimtes kunnen aanmaken, wijzigen en
  configureren met minimaal naam, capaciteit en locatie.
- **FR-009a**: Het systeem MOET het verwijderen van een vergaderruimte weigeren
  zolang er nog actieve toekomstige reserveringen voor die ruimte bestaan.
- **FR-010**: Het systeem MOET onderscheid maken tussen de rol Medewerker en
  de rol Beheerder, waarbij beheerfunctionaliteit (ruimtes configureren)
  voorbehouden is aan Beheerders.
- **FR-011**: Het systeem MOET gebruikers laten inloggen via vooraf
  gedefinieerde demo-accounts (trainings-scope; zie Assumptions).

### Key Entities *(include if feature involves data)*

- **Vergaderruimte**: Een reserveerbare ruimte met naam, capaciteit en locatie.
- **Reservering**: Koppelt een medewerker aan een vergaderruimte voor een
  begin- en eindtijd; heeft een status (actief, gewijzigd, geannuleerd).
- **Gebruiker**: Een demo-account met een rol (Medewerker of Beheerder).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Een medewerker kan een vergaderruimte vinden en reserveren in
  minder dan 1 minuut.
- **SC-002**: Het systeem staat nooit twee overlappende actieve reserveringen
  voor dezelfde ruimte toe (0 dubbele boekingen bij gelijktijdig gebruik).
- **SC-003**: 100% van de historische reserveringen blijft na afloop
  raadpleegbaar in het overzicht van de medewerker.
- **SC-004**: Een beheerder kan een nieuwe vergaderruimte configureren en deze
  is direct (zonder herstart van het systeem) zichtbaar en reserveerbaar voor
  medewerkers.

## Assumptions

- Dit is een trainingsproject (zie `docs/original-plan.md`); authenticatie
  gebeurt via vaste demo-accounts per rol (Medewerker, Beheerder), geen echte
  identity-provider.
- De applicatie is Nederlandstalig en bedoeld voor lokaal/demo-gebruik; er
  gelden geen schaal- of performance-eisen buiten single-user/demo-gebruik.
- Werkplekreserveringen, check-in/check-out en integraties met Outlook, Teams
  en Microsoft Graph vallen buiten de scope van deze release, maar het
  datamodel houdt rekening met latere uitbreiding hiermee (zie constitution,
  principe III).
- Er is precies één type reserveerbare eenheid in deze release: de
  vergaderruimte (geen werkplekken).
