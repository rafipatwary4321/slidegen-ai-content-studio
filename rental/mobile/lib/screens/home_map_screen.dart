import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../data/sample_properties.dart';
import '../models/map_property.dart';
import '../models/property_category.dart';
import '../services/api_service.dart';
import '../services/session_notifier.dart';
import '../services/session_store.dart';
import 'booking_summary_screen.dart';
import 'listing_detail_screen.dart';

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
  String? _selectedListingId;

  /// Pins shown on the map (loaded from backend /explore, with local fallback).
  List<MapProperty> _baseProperties = sampleMapProperties;
  bool _mapLoading = false;
  bool _usingRemoteListings = false;
  int? _sessionUserId;

  void _onSessionChanged() {
    _refreshSessionAndListings();
  }

  @override
  void initState() {
    super.initState();
    SessionNotifier.instance.addListener(_onSessionChanged);
    _refreshSessionAndListings();
  }

  @override
  void dispose() {
    SessionNotifier.instance.removeListener(_onSessionChanged);
    _mapController?.dispose();
    super.dispose();
  }

  Future<void> _refreshSessionAndListings() async {
    final id = await SessionStore.getUserId();
    if (!mounted) return;
    setState(() => _sessionUserId = id);
    await _reloadListingsFromApi();
  }

  Future<void> _reloadListingsFromApi() async {
    setState(() => _mapLoading = true);
    final remote = await fetchExploreListings(
      lat: _initialTarget.latitude,
      lon: _initialTarget.longitude,
      radiusKm: 80,
      category: _selectedCategory,
      userId: effectiveViewerForExplore(_sessionUserId),
    );
    if (!mounted) return;
    setState(() {
      _mapLoading = false;
      if (remote != null) {
        _baseProperties = remote;
        _usingRemoteListings = true;
      }
      if (_selectedListingId != null &&
          !_baseProperties.any((p) => p.id == _selectedListingId)) {
        _selectedListingId = null;
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
        infoWindow: InfoWindow(
          title: p.title,
          snippet: p.category == PropertyCategory.bachelor && p.matchScore != null
              ? '${p.category.apiValue} · ${p.matchScore!.toStringAsFixed(0)}% Match'
              : p.category.apiValue,
        ),
        icon: BitmapDescriptor.defaultMarkerWithHue(markerHueForCategory(p.category)),
        onTap: () {
          setState(() => _selectedListingId = p.id);
        },
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
    if (_usingRemoteListings) {
      // API applies category server-side; safety mode is local filter.
      if (_selectedListingId != null &&
          !_visibleProperties.any((p) => p.id == _selectedListingId)) {
        setState(() => _selectedListingId = null);
      }
    } else {
      _reloadListingsFromApi();
    }
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

  void _openSelectedListingDetails() {
    final id = int.tryParse(_selectedListingId ?? '');
    if (id == null) return;
    Navigator.of(context).push<void>(
      MaterialPageRoute<void>(
        builder: (_) => ListingDetailScreen(listingId: id),
      ),
    );
  }

  MapProperty? get _selectedProperty {
    final id = _selectedListingId;
    if (id == null) return null;
    for (final p in _visibleProperties) {
      if (p.id == id) return p;
    }
    return null;
  }

  Widget _buildCategoryFloating(ThemeData theme) {
    return Material(
      elevation: 4,
      borderRadius: BorderRadius.circular(14),
      color: theme.colorScheme.surface.withOpacity(0.95),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        child: Wrap(
          crossAxisAlignment: WrapCrossAlignment.center,
          spacing: 8,
          runSpacing: 8,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.tune, size: 18, color: theme.colorScheme.primary),
                const SizedBox(width: 6),
                Text(
                  'Category Filter',
                  style: theme.textTheme.labelLarge?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
            FilterChip(
              label: const Text('All'),
              selected: _selectedCategory == null,
              onSelected: (_) => _onCategorySelected(null),
            ),
            for (final c in PropertyCategory.values)
              FilterChip(
                label: Text(c.apiValue),
                selected: _selectedCategory == c,
                onSelected: (sel) => _onCategorySelected(sel ? c : null),
              ),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('Safety'),
                const SizedBox(width: 4),
                Switch.adaptive(
                  value: _safetyModeFemaleOnly,
                  onChanged: _onSafetyChanged,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailCard(BuildContext context, MapProperty p) {
    final theme = Theme.of(context);
    return Card(
      margin: EdgeInsets.zero,
      elevation: 6,
      clipBehavior: Clip.antiAlias,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(14, 14, 14, 12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              p.title,
              style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 6),
            Text(
              p.category.apiValue,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.primary,
              ),
            ),
            if (p.category == PropertyCategory.bachelor && p.matchScore != null) ...[
              const SizedBox(height: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: theme.colorScheme.primaryContainer,
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Text(
                  '${p.matchScore!.toStringAsFixed(0)}% Match',
                  style: theme.textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.w700,
                    color: theme.colorScheme.onPrimaryContainer,
                  ),
                ),
              ),
            ],
            if (p.category == PropertyCategory.tourism) ...[
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  if (p.hasGuide)
                    FilledButton.tonalIcon(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Guide option selected (placeholder)')),
                        );
                      },
                      icon: const Icon(Icons.hiking_outlined),
                      label: const Text('Book Guide'),
                    ),
                  FilledButton.tonalIcon(
                    onPressed: () {
                      final txt = p.gearRental.isEmpty ? 'No gear listed yet' : p.gearRental.join(', ');
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Gear: $txt')),
                      );
                    },
                    icon: const Icon(Icons.backpack_outlined),
                    label: const Text('Rent Gear'),
                  ),
                ],
              ),
            ],
            const SizedBox(height: 10),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _openSelectedListingDetails,
                    icon: const Icon(Icons.open_in_new),
                    label: const Text('View Details'),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  tooltip: 'Close',
                  onPressed: () => setState(() => _selectedListingId = null),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSidebar(BuildContext context) {
    final theme = Theme.of(context);
    void showPlaceholder(String name) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('$name coming soon')),
      );
    }

    return Container(
      width: 220,
      decoration: BoxDecoration(
        color: theme.colorScheme.surface,
        border: Border(right: BorderSide(color: theme.colorScheme.outlineVariant)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 18, 16, 8),
            child: Text(
              'UrbanRelief',
              style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.map_outlined),
            title: const Text('Map'),
            selected: true,
          ),
          ListTile(
            leading: const Icon(Icons.receipt_long_outlined),
            title: const Text('My Bookings'),
            onTap: () => showPlaceholder('My Bookings'),
          ),
          ListTile(
            leading: const Icon(Icons.badge_outlined),
            title: const Text('NID Verification'),
            onTap: () => showPlaceholder('NID Verification'),
          ),
          ListTile(
            leading: const Icon(Icons.person_outline),
            title: const Text('Profile'),
            onTap: () => showPlaceholder('Profile'),
          ),
        ],
      ),
    );
  }

  Widget _buildMapArea(bool isWide) {
    final theme = Theme.of(context);
    final selected = _selectedProperty;

    return Stack(
      children: [
        GoogleMap(
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
        if (_mapLoading)
          const Positioned(top: 0, left: 0, right: 0, child: LinearProgressIndicator(minHeight: 2)),
        Positioned(
          top: 14,
          left: 16,
          right: isWide ? 16 : 16,
          child: _buildCategoryFloating(theme),
        ),
        if (!isWide && selected != null)
          Positioned(
            left: 12,
            right: 12,
            bottom: 14,
            child: _buildDetailCard(context, selected),
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final selected = _selectedProperty;

    return Scaffold(
      appBar: AppBar(
        title: const Text('UrbanRelief'),
        actions: [
          IconButton(
            tooltip: 'Booking summary',
            icon: const Icon(Icons.receipt_long_outlined),
            onPressed: () => _openBookingSummary(context),
          ),
        ],
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth >= 1150;
          if (!isWide) {
            return _buildMapArea(false);
          }
          return Row(
            children: [
              _buildSidebar(context),
              Expanded(child: _buildMapArea(true)),
              Container(
                width: 360,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surface,
                  border: Border(
                    left: BorderSide(color: Theme.of(context).colorScheme.outlineVariant),
                  ),
                ),
                child: selected == null
                    ? Center(
                        child: Text(
                          'Click a marker to view details',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: Theme.of(context).colorScheme.onSurfaceVariant,
                              ),
                        ),
                      )
                    : Padding(
                        padding: const EdgeInsets.all(12),
                        child: _buildDetailCard(context, selected),
                      ),
              ),
            ],
          );
        },
      ),
    );
  }
}
