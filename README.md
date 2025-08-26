# Zines Database Project

## Overview
This project creates a SQLite database called `zines.db` to manage information about publications and events. The database contains two tables: `publications` and `events`. The `events` table is linked to the `publications` table via a foreign key.

---

## Data Model Summary

### `publications` Table
- **Purpose**: Stores information about publications.
- **Columns**:
  - `pub_id` (INTEGER, Primary Key): Unique identifier for each publication.
  - `pub_title` (TEXT, NOT NULL): Title of the publication.
  - `volume` (INTEGER, NOT NULL): Volume number of the publication.
  - `issue_number` (INTEGER, NOT NULL): Issue number within the volume.
  - `issue_date` (DATE): Full issue date (year, month, day).
  - `volume_title` (TEXT): Title of the volume (if applicable).

### `events` Table
- **Purpose**: Stores information about events linked to publications.
- **Columns**:
  - `event_id` (INTEGER, Primary Key): Unique identifier for each event.
  - `publication_id` (INTEGER, Foreign Key): Links to `publications.pub_id`.
  - `event_title` (TEXT, NOT NULL): Title of the event.
  - `event_type` (TEXT): Type of the event (e.g., conference, workshop).
  - `event_date` (DATE): Date of the event.
  - `location` (TEXT): Name of the venue or location.
  - `address` (TEXT): Address of the event location.
  - `city` (TEXT): City where the event is held.
  - `state` (TEXT): State or region where the event is held.
  - `country` (TEXT): Country where the event is held.
  - `description` (TEXT): Detailed description of the event.
  - `source_publication` (TEXT): Source publication for the event.

---

## Schema Diagram
+-------------------+          +-------------------+
|   publications    |          |      events       |
+-------------------+          +-------------------+
| pub_id (PK)       |<---------| event_id (PK)     |
| pub_title         |          | publication_id (FK)|
| volume            |          | event_title       |
| issue_number      |          | event_type        |
| issue_date        |          | event_date        |
| volume_title      |          | location          |
+-------------------+          | address           |
                               | city              |
                               | state             |
                               | country           |
                               | description       |
                               | source_publication|
                               +-------------------+


---

## Notes
- The `events` table references the `publications` table via the `publication_id` foreign key.
- **Cascade Delete**: If a publication is deleted, all associated events are also deleted.