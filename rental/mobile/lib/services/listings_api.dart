import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/map_property.dart';
import '../models/property_category.dart';

/// Optional: `flutter run --dart-define=VIEWER_USER_ID=3` after `seed_demo.py` (id may differ).
const int kViewerUserIdForMap = int.fromEnvironment('VIEWER_USER_ID', defaultValue: 3);

PropertyCategory _categoryFromApi(String raw) {
  for (final c in PropertyCategory.values) {
    if (c.apiValue == raw) return c;
  }
  return PropertyCategory.shortStay;
}

/// Calls `GET /api/v1/listings/search`. Returns null on network/parse failure (caller may fallback).
Future<List<MapProperty>?> fetchListingsForMap({
  required double lat,
  required double lon,
  double radiusKm = 25,
  PropertyCategory? category,
  bool femaleOnly = false,
}) async {
  final params = <String, String>{
    'lat': '$lat',
    'lon': '$lon',
    'radius_km': '$radiusKm',
    if (category != null) 'category': category.apiValue,
    if (femaleOnly) 'female_only': 'true',
    if (kViewerUserIdForMap > 0) 'viewer_user_id': '$kViewerUserIdForMap',
  };
  final uri = Uri.parse('$kApiBase/api/v1/listings/search').replace(queryParameters: params);

  try {
    final res = await http.get(uri).timeout(const Duration(seconds: 12));
    if (res.statusCode != 200) return null;
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    final items = body['items'] as List<dynamic>? ?? [];
    return items.map((e) {
      final m = e as Map<String, dynamic>;
      final id = m['id'];
      return MapProperty(
        id: '$id',
        title: m['title'] as String? ?? 'Listing',
        latitude: (m['latitude'] as num).toDouble(),
        longitude: (m['longitude'] as num).toDouble(),
        category: _categoryFromApi(m['category'] as String? ?? ''),
        femaleOnlyHost: m['female_only_host'] as bool? ?? false,
      );
    }).toList();
  } catch (_) {
    return null;
  }
}
