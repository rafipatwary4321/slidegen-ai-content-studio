import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../data/sample_properties.dart';
import '../models/map_property.dart';
import '../models/property_category.dart';
import '../services/listings_api.dart';
import 'booking_summary_screen.dart';

/// Home map + category chips + Safety Mode (female-only hosts).
///
/// Setup: run `flutter create .` in `mobile/`, then add a Maps SDK key:
/// - Android: `android/app/src/main/AndroidManifest.xml` inside `<application>`:
///   `<meta-data android:name="com.google.android.geo.API_KEY" android:value="YOUR_KEY"/>`
/// - iOS: see `google_maps_flutter` README (AppDelegate + key in `AppDelegate.swift`).
class HomeMapScreen extends StatefulWidget {
  const HomeMapScreen({super.key});

  @override
  State<HomeMapScreen> createState() => _HomeMapScreenState();
}

class _HomeMapScreenState extends State<HomeMapScreen> {
  static const LatLng _initialTarget = LatLng(23.8103, 90.4125);

  PropertyCategory? _selectedCategory;
  bool _safetyModeFemaleOnly = false;
  GoogleMapController? _mapController;

  /// Pins shown on the map (API applies category + Safety Mode server-side when used).
  List<MapProperty> _baseProperties = sampleMapProperties;
  bool _mapLoading = false;
  bool _usingRemoteListings = false;

  @override
  void initState() {
    super.initState();
    _reloadListingsFromApi();
  }

  Future<void> _reloadListingsFromApi() async {
    setState(() => _mapLoading = true);
    final remote = await fetchListingsForMap(
      lat: _initialTarget.latitude,
      lon: _initialTarget.longitude,
      radiusKm: 80,
      category: _selectedCategory,
      femaleOnly: _safetyModeFemaleOnly,
    );
    if (!mounted) return;
    setState(() {
      _mapLoading = false;
      if (remote != null) {
        _baseProperties = remote;
        _usingRemoteListings = true;
      }
    });
    await _fitToVisible();
  }

  Iterable<MapProperty> get _visibleProperties {
    if (_usingRemoteListings) {
      return _baseProperties;
    }
    var list = _baseProperties;
    if (_selectedCategory != null) {
      list = list.where((p) => p.category == _selectedCategory).toList();
    }
    if (_safetyModeFemaleOnly) {
      list = list.where((p) => p.femaleOnlyHost).toList();
    }
    return list;
  }

  Set<Marker> get _markers {
    return _visibleProperties.map((p) {
      return Marker(
        markerId: MarkerId(p.id),
        position: LatLng(p.latitude, p.longitude),
        infoWindow: InfoWindow(title: p.title, snippet: p.category.apiValue),
        icon: BitmapDescriptor.defaultMarkerWithHue(markerHueForCategory(p.category)),
      );
    }).toSet();
  }

  Future<void> _fitToVisible() async {
    final controller = _mapController;
    if (controller == null) return;
    final props = _visibleProperties.toList();
    if (props.isEmpty) {
      await controller.animateCamera(
        CameraUpdate.newCameraPosition(
          const CameraPosition(target: _initialTarget, zoom: 11),
        ),
      );
      return;
    }
    if (props.length == 1) {
      final p = props.first;
      await controller.animateCamera(
        CameraUpdate.newLatLngZoom(LatLng(p.latitude, p.longitude), 14),
      );
      return;
    }
    double minLat = props.first.latitude;
    double maxLat = minLat;
    double minLng = props.first.longitude;
    double maxLng = minLng;
    for (final p in props) {
      minLat = minLat < p.latitude ? minLat : p.latitude;
      maxLat = maxLat > p.latitude ? maxLat : p.latitude;
      minLng = minLng < p.longitude ? minLng : p.longitude;
      maxLng = maxLng > p.longitude ? maxLng : p.longitude;
    }
    await controller.animateCamera(
      CameraUpdate.newLatLngBounds(
        LatLngBounds(
          southwest: LatLng(minLat, minLng),
          northeast: LatLng(maxLat, maxLng),
        ),
        72,
      ),
    );
  }

  void _onCategorySelected(PropertyCategory? category) {
    setState(() => _selectedCategory = category);
    _reloadListingsFromApi();
  }

  void _onSafetyChanged(bool value) {
    setState(() => _safetyModeFemaleOnly = value);
    _reloadListingsFromApi();
  }

  Future<void> _openBookingSummary(BuildContext context) async {
    final id = await showDialog<int>(
      context: context,
      builder: (ctx) {
        final tc = TextEditingController(text: '1');
        void close([int? value]) {
          tc.dispose();
          Navigator.pop(ctx, value);
        }

        return AlertDialog(
          title: const Text('Booking summary'),
          content: TextField(
            controller: tc,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Booking ID',
              hintText: 'From your reservation',
            ),
          ),
          actions: [
            TextButton(onPressed: () => close(), child: const Text('Cancel')),
            FilledButton(
              onPressed: () => close(int.tryParse(tc.text.trim())),
              child: const Text('Open'),
            ),
          ],
        );
      },
    );
    if (!context.mounted || id == null) return;
    await Navigator.of(context).push<void>(
      MaterialPageRoute<void>(
        builder: (_) => BookingSummaryScreen(bookingId: id),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('UrbanRelief'),
        backgroundColor: theme.colorScheme.inversePrimary,
        actions: [
          IconButton(
            tooltip: 'Booking summary',
            icon: const Icon(Icons.receipt_long_outlined),
            onPressed: () => _openBookingSummary(context),
          ),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (_mapLoading)
            const LinearProgressIndicator(minHeight: 2),
          Material(
            color: theme.colorScheme.surfaceContainerHighest.withOpacity(0.35),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                children: [
                  Icon(Icons.shield_outlined, color: theme.colorScheme.primary, size: 22),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Safety Mode',
                          style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600),
                        ),
                        Text(
                          'Show female-only host listings',
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: theme.colorScheme.onSurfaceVariant,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Switch.adaptive(
                    value: _safetyModeFemaleOnly,
                    onChanged: _onSafetyChanged,
                  ),
                ],
              ),
            ),
          ),
          SizedBox(
            height: 52,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              children: [
                Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: FilterChip(
                    label: const Text('All'),
                    selected: _selectedCategory == null,
                    onSelected: (_) => _onCategorySelected(null),
                  ),
                ),
                for (final c in PropertyCategory.values)
                  Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: FilterChip(
                      label: Text(c.apiValue),
                      selected: _selectedCategory == c,
                      onSelected: (sel) => _onCategorySelected(sel ? c : null),
                    ),
                  ),
              ],
            ),
          ),
          Expanded(
            child: GoogleMap(
              initialCameraPosition: const CameraPosition(
                target: _initialTarget,
                zoom: 11,
              ),
              markers: _markers,
              myLocationButtonEnabled: false,
              myLocationEnabled: false,
              zoomControlsEnabled: true,
              mapToolbarEnabled: false,
              onMapCreated: (c) {
                _mapController = c;
                _fitToVisible();
              },
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }
}
