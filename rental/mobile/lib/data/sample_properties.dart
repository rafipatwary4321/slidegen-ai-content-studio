import '../models/map_property.dart';
import '../models/property_category.dart';

/// Demo pins around Dhaka — replace with `/api/v1/listings/search` results.
final List<MapProperty> sampleMapProperties = [
  const MapProperty(
    id: '1',
    title: 'Gulshan Short Stay',
    latitude: 23.7925,
    longitude: 90.4078,
    category: PropertyCategory.shortStay,
    femaleOnlyHost: false,
  ),
  const MapProperty(
    id: '2',
    title: 'Uttara Bachelor Mess',
    latitude: 23.8759,
    longitude: 90.3796,
    category: PropertyCategory.bachelor,
    femaleOnlyHost: false,
  ),
  const MapProperty(
    id: '3',
    title: "Women's Floor — Banani",
    latitude: 23.7948,
    longitude: 90.4042,
    category: PropertyCategory.bachelor,
    femaleOnlyHost: true,
  ),
  const MapProperty(
    id: '4',
    title: 'Dhanmondi Family Flat',
    latitude: 23.7465,
    longitude: 90.3760,
    category: PropertyCategory.family,
    femaleOnlyHost: false,
  ),
  const MapProperty(
    id: '5',
    title: 'Sylhet Home-Stay (demo)',
    latitude: 24.8949,
    longitude: 91.8687,
    category: PropertyCategory.tourism,
    femaleOnlyHost: false,
  ),
  const MapProperty(
    id: '6',
    title: 'Female-Host Tourism Cottage',
    latitude: 24.3105,
    longitude: 91.7296,
    category: PropertyCategory.tourism,
    femaleOnlyHost: true,
  ),
];
