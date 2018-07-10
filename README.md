# osm_report_addr

Bardzo prosta implementacja watchera danych osm.
Jako źródło danych używa bazy postgresql utworzonej przez osm2pgsql.
Opis utworzenia bazy znajduje się na stronie swith2osm:
https://switch2osm.org/manually-building-a-tile-server-18-04-lts/
Ekstrakt koniecznych kroków umieszczę później.

Watcher szuka uszkodzonych adresów w changesetach za ostatnią dobę według zadanych kryteriów i komentuje changesety w których zostały one uszkodzone

Wymagania:
- możliwość określenia zaufanych userów
- możliwość określenia zaufanych aplikacji
- komentarze mają być zrozumiałe dla userów żeby wiedzieli jednoznacznie jaki błąd popełnili
- komentarze powinny zawierać obiekty w których wykryto błędy
- sprawdzenie czy changeset zmieniał coś w adresacji czy tylko dotknął obiekt a adresacja była zepsuta wcześniej
- możliwość zapisania raportu html przed zakomentowaniem changesetu
- wysłanie maila z informacją o uszkodzonych changesetach 
