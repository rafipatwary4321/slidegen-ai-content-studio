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

/// Marker tint mapping:
/// Bachelor = blue, Short-stay = green, Tourism = orange, Family = red.
double markerHueForCategory(PropertyCategory category) {
  return switch (category) {
    PropertyCategory.shortStay => BitmapDescriptor.hueGreen,
    PropertyCategory.bachelor => BitmapDescriptor.hueBlue,
    PropertyCategory.tourism => BitmapDescriptor.hueOrange,
    PropertyCategory.family => BitmapDescriptor.hueRed,
  };
}
