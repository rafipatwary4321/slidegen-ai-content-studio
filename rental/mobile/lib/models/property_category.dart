import 'package:google_maps_flutter/google_maps_flutter.dart';

/// Aligns with backend `ListingCategory` string values.
enum PropertyCategory {
  shortStay('Short-Stay'),
  bachelor('Bachelor'),
  family('Family'),
  tourism('Tourism');

  const PropertyCategory(this.apiValue);
  final String apiValue;
}

/// Marker tint: Tourism = green, Bachelor = blue (per product brief).
double markerHueForCategory(PropertyCategory category) {
  return switch (category) {
    PropertyCategory.tourism => BitmapDescriptor.hueGreen,
    PropertyCategory.bachelor => BitmapDescriptor.hueBlue,
    PropertyCategory.shortStay => BitmapDescriptor.hueOrange,
    PropertyCategory.family => BitmapDescriptor.hueViolet,
  };
}
