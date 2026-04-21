import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

import '../models/listing_search_result.dart';
import '../models/property_category.dart';
import '../services/listings_api.dart';
import '../services/session_notifier.dart';
import '../services/session_store.dart';
import 'listing_detail_screen.dart';

/// List + filters mirroring map search (same API).
class ExploreScreen extends StatefulWidget {
  const ExploreScreen({super.key});

  @override
  State<ExploreScreen> createState() => _ExploreScreenState();
}

class _ExploreScreenState extends State<ExploreScreen> {
  static const LatLng _origin = LatLng(23.8103, 90.4125);

  PropertyCategory? _category;
  bool _femaleOnly = false;
  int? _sessionUserId;
  List<ListingSearchResult> _items = [];
  bool _loading = true;
  String? _error;

  void _onSessionChanged() => _bootstrap();

  @override
  void initState() {
    super.initState();
    SessionNotifier.instance.addListener(_onSessionChanged);
    _bootstrap();
  }

  @override
  void dispose() {
    SessionNotifier.instance.removeListener(_onSessionChanged);
    super.dispose();
  }

  Future<void> _bootstrap() async {
    final id = await SessionStore.getUserId();
    if (mounted) {
      setState(() => _sessionUserId = id);
    }
    await _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    final viewer = (_sessionUserId != null && _sessionUserId! > 0)
        ? _sessionUserId
        : (kViewerUserIdForMap > 0 ? kViewerUserIdForMap : null);
    final rows = await searchListings(
      lat: _origin.latitude,
      lon: _origin.longitude,
      radiusKm: 80,
      category: _category,
      femaleOnly: _femaleOnly,
      viewerUserId: viewer,
    );
    if (!mounted) return;
    setState(() {
      _loading = false;
      if (rows == null) {
        _error = 'Could not load listings. Check API_BASE and server.';
        _items = [];
      } else {
        _items = rows;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Explore'),
        actions: [
          IconButton(
            tooltip: 'Refresh',
            onPressed: _load,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 4),
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                FilterChip(
                  label: const Text('All'),
                  selected: _category == null,
                  onSelected: (_) {
                    setState(() => _category = null);
                    _load();
                  },
                ),
                for (final c in PropertyCategory.values)
                  FilterChip(
                    label: Text(c.apiValue),
                    selected: _category == c,
                    onSelected: (sel) {
                      setState(() => _category = sel ? c : null);
                      _load();
                    },
                  ),
                FilterChip(
                  avatar: Icon(
                    Icons.shield_outlined,
                    size: 18,
                    color: _femaleOnly ? theme.colorScheme.primary : null,
                  ),
                  label: const Text('Female-only hosts'),
                  selected: _femaleOnly,
                  onSelected: (v) {
                    setState(() => _femaleOnly = v);
                    _load();
                  },
                ),
              ],
            ),
          ),
          if (_loading) const LinearProgressIndicator(minHeight: 2),
          Expanded(
            child: _error != null
                ? Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text(_error!, textAlign: TextAlign.center),
                    ),
                  )
                : _items.isEmpty
                    ? Center(
                        child: Text(
                          'No listings in range.',
                          style: theme.textTheme.bodyLarge?.copyWith(
                            color: theme.colorScheme.onSurfaceVariant,
                          ),
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: _load,
                        child: ListView.separated(
                          padding: const EdgeInsets.all(16),
                          itemCount: _items.length,
                          separatorBuilder: (_, __) => const SizedBox(height: 10),
                          itemBuilder: (context, i) {
                            final it = _items[i];
                            return Card(
                              clipBehavior: Clip.antiAlias,
                              child: ListTile(
                                contentPadding: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                title: Text(
                                  it.title,
                                  style: const TextStyle(fontWeight: FontWeight.w600),
                                ),
                                subtitle: Text(
                                  '${it.category} · ${it.distanceKm.toStringAsFixed(1)} km · '
                                  'host ${it.hostReputationScore.toStringAsFixed(2)}'
                                  '${it.compatibilityPercent != null ? ' · ${it.compatibilityPercent!.toStringAsFixed(0)}% match' : ''}',
                                ),
                                isThreeLine: true,
                                trailing: it.femaleOnlyHost
                                    ? Icon(Icons.verified_user_outlined,
                                        color: theme.colorScheme.primary)
                                    : null,
                                onTap: () {
                                  Navigator.of(context).push<void>(
                                    MaterialPageRoute<void>(
                                      builder: (_) =>
                                          ListingDetailScreen(listingId: it.id),
                                    ),
                                  );
                                },
                              ),
                            );
                          },
                        ),
                      ),
          ),
        ],
      ),
    );
  }
}
