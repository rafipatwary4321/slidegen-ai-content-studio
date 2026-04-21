import 'map_property.dart';
import 'property_category.dart';

class ListingSearchResult {
  const ListingSearchResult({
    required this.id,
    required this.title,
    required this.category,
    required this.latitude,
    required this.longitude,
    required this.distanceKm,
    required this.hostReputationScore,
    this.compatibilityPercent,
    this.femaleOnlyHost = false,
    this.priceDaily,
    this.priceMonthly,
  });

  final int id;
  final String title;
  final String category;
  final double latitude;
  final double longitude;
  final double distanceKm;
  final double hostReputationScore;
  final double? compatibilityPercent;
  final bool femaleOnlyHost;
  final double? priceDaily;
  final double? priceMonthly;

  factory ListingSearchResult.fromJson(Map<String, dynamic> json) {
    return ListingSearchResult(
      id: (json['id'] as num).toInt(),
      title: json['title'] as String? ?? 'Listing',
      category: json['category'] as String? ?? '',
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      distanceKm: (json['distance_km'] as num).toDouble(),
      hostReputationScore: (json['host_reputation_score'] as num).toDouble(),
      compatibilityPercent: (json['compatibility_percent'] as num?)?.toDouble(),
      femaleOnlyHost: json['female_only_host'] as bool? ?? false,
      priceDaily: (json['price_daily'] as num?)?.toDouble(),
      priceMonthly: (json['price_monthly'] as num?)?.toDouble(),
    );
  }

  PropertyCategory get categoryEnum {
    for (final c in PropertyCategory.values) {
      if (c.apiValue == category) return c;
    }
    return PropertyCategory.shortStay;
  }

  MapProperty toMapProperty() {
    return MapProperty(
      id: '$id',
      title: title,
      latitude: latitude,
      longitude: longitude,
      category: categoryEnum,
      femaleOnlyHost: femaleOnlyHost,
    );
  }
}
