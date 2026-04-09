import 'dart:ui' show FontFeature;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import '../models/booking_summary.dart';
import '../services/booking_api.dart';

/// Shows digital key (OTP), directions to the listing, and n8n agreement download link.
class BookingSummaryScreen extends StatefulWidget {
  const BookingSummaryScreen({super.key, required this.bookingId});

  final int bookingId;

  @override
  State<BookingSummaryScreen> createState() => _BookingSummaryScreenState();
}

class _BookingSummaryScreenState extends State<BookingSummaryScreen> {
  late Future<BookingSummary> _future;

  @override
  void initState() {
    super.initState();
    _future = fetchBookingSummary(widget.bookingId);
  }

  Future<void> _reload() async {
    setState(() {
      _future = fetchBookingSummary(widget.bookingId);
    });
    await _future;
  }

  Future<void> _openDirections(double lat, double lng) async {
    final uri = Uri.parse(
      'https://www.google.com/maps/dir/?api=1&destination=$lat,$lng',
    );
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open Maps')),
        );
      }
    }
  }

  Future<void> _openAgreement(String url) async {
    final uri = Uri.parse(url);
    if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open agreement link')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Booking #${widget.bookingId}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () async {
              try {
                await _reload();
              } catch (e) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Refresh failed: $e')),
                  );
                }
              }
            },
          ),
        ],
      ),
      body: FutureBuilder<BookingSummary>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.error_outline, size: 48, color: theme.colorScheme.error),
                    const SizedBox(height: 16),
                    Text(
                      snapshot.error.toString(),
                      textAlign: TextAlign.center,
                      style: theme.textTheme.bodyMedium,
                    ),
                    const SizedBox(height: 24),
                    FilledButton(onPressed: _reload, child: const Text('Retry')),
                  ],
                ),
              ),
            );
          }
          final s = snapshot.data!;

          return ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Text(
                s.listingTitle,
                style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text('Status: ${s.status}', style: theme.textTheme.titleMedium),
              const SizedBox(height: 4),
              Text('${s.checkIn} → ${s.checkOut}'),
              Text('Total: ${s.totalAmount}'),
              const SizedBox(height: 28),
              Text(
                'Digital key (OTP)',
                style: theme.textTheme.titleSmall?.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: 8),
              if (s.digitalKey != null)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(
                            s.digitalKey!,
                            style: theme.textTheme.displaySmall?.copyWith(
                              letterSpacing: 8,
                              fontWeight: FontWeight.w600,
                              fontFeatures: const [FontFeature.tabularFigures()],
                            ),
                          ),
                        ),
                        IconButton(
                          tooltip: 'Copy OTP',
                          icon: const Icon(Icons.copy),
                          onPressed: () async {
                            await Clipboard.setData(ClipboardData(text: s.digitalKey!));
                            if (context.mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('OTP copied')),
                              );
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                )
              else
                Text(
                  'No OTP yet — booking must be Confirmed (host payment / POST /api/v1/bookings/{id}/confirm).',
                  style: theme.textTheme.bodyMedium?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: () => _openDirections(s.listingLatitude, s.listingLongitude),
                icon: const Icon(Icons.directions),
                label: const Text('Get directions'),
              ),
              const SizedBox(height: 12),
              if (s.agreementDocumentUrl != null && s.agreementDocumentUrl!.isNotEmpty)
                OutlinedButton.icon(
                  onPressed: () => _openAgreement(s.agreementDocumentUrl!),
                  icon: const Icon(Icons.description_outlined),
                  label: const Text('Download digital rental agreement'),
                )
              else
                Text(
                  'Agreement link appears here after n8n returns a URL (confirm booking with webhook configured).',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                ),
            ],
          );
        },
      ),
    );
  }
}
