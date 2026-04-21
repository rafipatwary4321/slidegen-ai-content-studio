import 'dart:convert';

import 'property_category.dart';

class ListingDetail {
  const ListingDetail({
    required this.id,
    required this.ownerId,
    required this.title,
    this.description,
    required this.category,
    required this.latitude,
    required this.longitude,
    this.priceDaily,
    this.priceMonthly,
    this.amenities,
  });

  final int id;
  final int ownerId;
  final String title;
  final String? description;
  final String category;
  final double latitude;
  final double longitude;
  final double? priceDaily;
  final double? priceMonthly;
  final Object? amenities;

  PropertyCategory get categoryEnum {
    for (final c in PropertyCategory.values) {
      if (c.apiValue == category) return c;
    }
    return PropertyCategory.shortStay;
  }

  factory ListingDetail.fromJson(Map<String, dynamic> json) {
    return ListingDetail(
      id: (json['id'] as num).toInt(),
      ownerId: (json['owner_id'] as num).toInt(),
      title: json['title'] as String? ?? '',
      description: json['description'] as String?,
      category: json['category'] as String? ?? '',
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      priceDaily: (json['price_daily'] as num?)?.toDouble(),
      priceMonthly: (json['price_monthly'] as num?)?.toDouble(),
      amenities: json['amenities'],
    );
  }

  String amenitiesSummary() {
    final a = amenities;
    if (a == null) return '';
    if (a is Map) return jsonEncode(a);
    if (a is List) return jsonEncode(a);
    return a.toString();
  }
}
