import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/listing_detail.dart';
import '../models/listing_search_result.dart';
import '../models/map_property.dart';
import '../models/property_category.dart';

/// Compile-time fallback when no signed-in user (`SessionStore`).
const int kViewerUserIdForMap = int.fromEnvironment('VIEWER_USER_ID', defaultValue: 3);

Future<List<ListingSearchResult>?> searchListings({
  required double lat,
  required double lon,
  double radiusKm = 25,
  PropertyCategory? category,
  bool femaleOnly = false,
  int? viewerUserId,
}) async {
  final params = <String, String>{
    'lat': '$lat',
    'lon': '$lon',
    'radius_km': '$radiusKm',
    if (category != null) 'category': category.apiValue,
    if (femaleOnly) 'female_only': 'true',
    if (viewerUserId != null && viewerUserId > 0) 'viewer_user_id': '$viewerUserId',
  };
  final uri = Uri.parse('$kApiBase/api/v1/listings/search').replace(queryParameters: params);

  try {
    final res = await http.get(uri).timeout(const Duration(seconds: 12));
    if (res.statusCode != 200) return null;
    final body = jsonDecode(res.body) as Map<String, dynamic>;
    final items = body['items'] as List<dynamic>? ?? [];
    return items
        .map((e) => ListingSearchResult.fromJson(e as Map<String, dynamic>))
        .toList();
  } catch (_) {
    return null;
  }
}

/// Resolves viewer: [sessionUserId], else compile-time [kViewerUserIdForMap] if > 0.
int? _effectiveViewer(int? sessionUserId) {
  if (sessionUserId != null && sessionUserId > 0) return sessionUserId;
  if (kViewerUserIdForMap > 0) return kViewerUserIdForMap;
  return null;
}

Future<List<MapProperty>?> fetchListingsForMap({
  required double lat,
  required double lon,
  double radiusKm = 25,
  PropertyCategory? category,
  bool femaleOnly = false,
  int? sessionUserId,
}) async {
  final rows = await searchListings(
    lat: lat,
    lon: lon,
    radiusKm: radiusKm,
    category: category,
    femaleOnly: femaleOnly,
    viewerUserId: _effectiveViewer(sessionUserId),
  );
  if (rows == null) return null;
  return rows.map((r) => r.toMapProperty()).toList();
}

Future<ListingDetail?> fetchListingDetail(int listingId) async {
  final uri = Uri.parse('$kApiBase/api/v1/listings/$listingId');
  try {
    final res = await http.get(uri).timeout(const Duration(seconds: 12));
    if (res.statusCode != 200) return null;
    final map = jsonDecode(res.body) as Map<String, dynamic>;
    return ListingDetail.fromJson(map);
  } catch (_) {
    return null;
  }
}
