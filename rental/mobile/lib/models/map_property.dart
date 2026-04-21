import 'property_category.dart';

/// Map listing used on the home screen.
/// When wired to the API, set [femaleOnlyHost] from e.g. `amenities['female_only'] == true`.
class MapProperty {
  const MapProperty({
    required this.id,
    required this.title,
    required this.latitude,
    required this.longitude,
    required this.category,
    this.femaleOnlyHost = false,
    this.matchScore,
    this.hasGuide = false,
    this.gearRental = const [],
  });

  final String id;
  final String title;
  final double latitude;
  final double longitude;
  final PropertyCategory category;

  /// Host opted into female-only / Safety Mode listings (client filter).
  final bool femaleOnlyHost;

  /// Bachelor match score from backend explore/search endpoint.
  final double? matchScore;

  /// Tourism-specific flags for detail actions.
  final bool hasGuide;
  final List<String> gearRental;
}
