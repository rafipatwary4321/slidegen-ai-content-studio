import 'package:flutter/material.dart';

import '../models/listing_detail.dart';
import '../services/listings_api.dart';
import 'create_booking_screen.dart';

class ListingDetailScreen extends StatefulWidget {
  const ListingDetailScreen({super.key, required this.listingId});

  final int listingId;

  @override
  State<ListingDetailScreen> createState() => _ListingDetailScreenState();
}

class _ListingDetailScreenState extends State<ListingDetailScreen> {
  late Future<ListingDetail?> _future;

  @override
  void initState() {
    super.initState();
    _future = fetchListingDetail(widget.listingId);
  }

  Future<void> _reload() async {
    setState(() {
      _future = fetchListingDetail(widget.listingId);
    });
    await _future;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Listing #${widget.listingId}'),
        actions: [
          IconButton(onPressed: _reload, icon: const Icon(Icons.refresh)),
        ],
      ),
      body: FutureBuilder<ListingDetail?>(
        future: _future,
        builder: (context, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final d = snap.data;
          if (d == null) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.home_work_outlined, size: 48),
                    const SizedBox(height: 16),
                    const Text('Listing not found or API unreachable.'),
                    const SizedBox(height: 16),
                    FilledButton(onPressed: _reload, child: const Text('Retry')),
                  ],
                ),
              ),
            );
          }

          final amenities = d.amenitiesSummary();
          return LayoutBuilder(
            builder: (context, constraints) {
              final isWide = constraints.maxWidth >= 1000;
              final summary = Card(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        d.title,
                        style: theme.textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        d.categoryEnum.apiValue,
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: theme.colorScheme.primary,
                        ),
                      ),
                      const SizedBox(height: 16),
                      if (d.priceDaily != null)
                        Text(
                          'From ${d.priceDaily!.toStringAsFixed(0)} / day',
                          style: theme.textTheme.titleMedium,
                        ),
                      if (d.priceMonthly != null)
                        Text(
                          '${d.priceMonthly!.toStringAsFixed(0)} / month',
                          style: theme.textTheme.bodyMedium,
                        ),
                      const SizedBox(height: 20),
                      FilledButton.icon(
                        onPressed: () {
                          Navigator.of(context).push<void>(
                            MaterialPageRoute<void>(
                              builder: (_) => CreateBookingScreen(
                                listingId: d.id,
                                listingTitle: d.title,
                                suggestedDaily: d.priceDaily,
                              ),
                            ),
                          );
                        },
                        icon: const Icon(Icons.calendar_month_outlined),
                        label: const Text('Book this stay'),
                      ),
                    ],
                  ),
                ),
              );

              final details = Card(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (d.description != null && d.description!.isNotEmpty) ...[
                        Text('Description', style: theme.textTheme.titleSmall),
                        const SizedBox(height: 6),
                        Text(d.description!, style: theme.textTheme.bodyLarge),
                      ],
                      if (amenities.isNotEmpty) ...[
                        if (d.description != null && d.description!.isNotEmpty) const SizedBox(height: 20),
                        Text('Amenities', style: theme.textTheme.titleSmall),
                        const SizedBox(height: 6),
                        Text(
                          amenities,
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: theme.colorScheme.onSurfaceVariant,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              );

              if (!isWide) {
                return ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    summary,
                    const SizedBox(height: 12),
                    details,
                  ],
                );
              }

              return SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 1200),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(flex: 5, child: summary),
                      const SizedBox(width: 16),
                      Expanded(flex: 6, child: details),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
