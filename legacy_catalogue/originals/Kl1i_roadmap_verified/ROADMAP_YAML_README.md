# BiBaZu-Posenroadmap: YAML-Übergabe

Die YAML-Datei enthält die physisch zusammengeführten Posen und alle aktuell
bekannten **gerichteten** direkten Übergänge. Eine Kante von `from_pose` nach
`to_pose` gilt nicht automatisch in Gegenrichtung.

## Posen

- `id` ist die Roadmap-ID und wird in `from_pose`/`to_pose` referenziert.
- Roadmap-IDs beginnen bei 0 und folgen der unter
  `classification.pose_ranking_method` gewählten Stabilitätsmetrik in
  absteigender Reihenfolge. `original_catalog_pose_id`
  und `equivalent_catalog_pose_ids` bewahren die ursprünglichen Katalog-IDs.
- `classification.robust_pose_ids` listet alle stabilen Zielposen direkt auf;
  `metastable_pose_ids` enthält die möglichen Zwischenlagen.
- `equivalent_catalog_pose_ids` sind durch praktische Rotationssymmetrie
  ununterscheidbare Darstellungen derselben physischen Pose.
- `stability: robust` kennzeichnet eine beobachtungsgeeignete stabile Zielpose.
- `stability: metastable` ist eine mögliche Zwischenlage; sie sollte nicht ohne
  experimentelle Bestätigung als dauerhafte Zielpose verwendet werden.
- Das Quaternion verwendet die Reihenfolge `[x, y, z, w]` und beschreibt die
  Orientierung vom Bauteil- ins feste Rutschenkoordinatensystem.

## Übergänge

- `type: actuated` kostet einen Luftimpuls; `passive_tip` kostet keinen Impuls.
- `axis`, `axis_vector_chute` und `direction` verwenden die feste Rutsche und die
  Rechte-Hand-Regel. Der Sollwert steht in `commanded_angle_deg`.
- `capture.interval_deg` und `capture.width_deg` beschreiben den geometrisch
  berechneten Einfangbereich. `geometry.geometric_score` ist **keine
  Erfolgswahrscheinlichkeit**.
- `geometry.passive_settling_via_catalog_pose_ids` nennt nicht als Knoten
  dargestellte instabile Kataloglagen, über die das Bauteil nach dem Impuls
  passiv in `to_pose` fällt. Ein leerer Wert kennzeichnet einen direkten
  Übergang.
- `classification.unresolved_metastable_pose_ids` bedeutet nur, dass aus der
  jeweiligen Pose **ohne Aktuierung** kein eindeutiges passives Kippen gefunden
  wurde. Aktuierte ausgehende Kanten können trotzdem vorhanden sein.
- Bei `surface_requirement` und `additional_requirement` müssen die genannten
  Aktuatorbedingungen erfüllt sein.

## Experimentelle Ergänzung

Der Block `experimental` jeder Kante ist zum manuellen oder automatischen
Ausfüllen vorgesehen:

- `trials`: Anzahl der Versuche,
- `successes`: erfolgreiche Übergänge zur angegebenen Zielpose,
- `empirical_success_rate`: `successes / trials` zwischen 0 und 1,
- `difficulty_rating`: frei wählbare gemeinsame Skala,
- `notes`: Beobachtungen, Fehlermodi oder Versuchsbedingungen.

Für die spätere Routenplanung sollte nach ausreichenden Versuchen bevorzugt
`empirical_success_rate` verwendet werden. Bis dahin kann der geometrische
Score als klar gekennzeichneter vorläufiger Ersatzwert dienen.
