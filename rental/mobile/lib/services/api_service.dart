import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/map_property.dart';
import '../models/property_category.dart';
import 'listings_api.dart';

PropertyCategory _categoryFromApi(String raw) {
  for (final c in PropertyCategory.values) {
    if (c.apiValue == raw) return c;
  }
  return PropertyCategory.shortStay;
}

/// Fetches listings from backend `/api/v1/listings/explore`.
Future<List<MapProperty>?> fetchExploreListings({
  required double lat,
  required double lon,
  double radiusKm = 25,
  PropertyCategory? category,
  int? userId,
}) async {
  final params = <String, String>{
    if (category != null) 'category': category.apiValue,
    'lat': '$lat',
    'lon': '$lon',
    'radius_km': '$radiusKm',
    if (userId != null && userId > 0) 'user_id': '$userId',
  };

  final uriPrimary = Uri.parse('$kApiBase/explore').replace(queryParameters: params);
  final uriFallback = Uri.parse('$kApiBase/api/v1/listings/explore').replace(queryParameters: params);
  try {
    http.Response res = await http.get(uriPrimary).timeout(const Duration(seconds: 12));
    if (res.statusCode != 200) {
      res = await http.get(uriFallback).timeout(const Duration(seconds: 12));
      if (res.statusCode != 200) return null;
    }
    final arr = jsonDecode(res.body) as List<dynamic>;
    return arr.map((e) {
      final m = e as Map<String, dynamic>;
      final rawGear = m['gear_rental'] ?? m['gear_available'] ?? m['available_gear'];
      final gear = rawGear is List
          ? rawGear
              .map((g) => g is Map<String, dynamic> ? (g['name']?.toString() ?? '') : g.toString())
              .where((x) => x.isNotEmpty)
              .toList()
          : <String>[];
      return MapProperty(
        id: '${m['id']}',
        title: m['title'] as String? ?? 'Listing',
        latitude: (m['latitude'] as num).toDouble(),
        longitude: (m['longitude'] as num).toDouble(),
        category: _categoryFromApi(m['category'] as String? ?? ''),
        femaleOnlyHost: (m['amenities'] is Map<String, dynamic>)
            ? ((m['amenities'] as Map<String, dynamic>)['female_only'] == true)
            : false,
        matchScore: (m['match_score'] as num?)?.toDouble(),
        hasGuide: m['has_guide'] as bool? ?? false,
        gearRental: gear,
      );
    }).toList();
  } catch (_) {
    return null;
  }
}

int? effectiveViewerForExplore(int? sessionUserId) {
  if (sessionUserId != null && sessionUserId > 0) return sessionUserId;
  if (kViewerUserIdForMap > 0) return kViewerUserIdForMap;
  return null;
}

