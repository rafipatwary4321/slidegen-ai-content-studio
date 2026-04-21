import 'package:flutter/material.dart';

import '../services/booking_api.dart';
import '../services/session_store.dart';
import 'booking_summary_screen.dart';

class CreateBookingScreen extends StatefulWidget {
  const CreateBookingScreen({
    super.key,
    required this.listingId,
    required this.listingTitle,
    this.suggestedDaily,
  });

  final int listingId;
  final String listingTitle;
  final double? suggestedDaily;

  @override
  State<CreateBookingScreen> createState() => _CreateBookingScreenState();
}

class _CreateBookingScreenState extends State<CreateBookingScreen> {
  DateTime _checkIn = DateTime.now().add(const Duration(days: 1));
  DateTime _checkOut = DateTime.now().add(const Duration(days: 3));
  final _amountCtrl = TextEditingController();
  bool _submitting = false;

  @override
  void initState() {
    super.initState();
    if (widget.suggestedDaily != null) {
      final nights = _checkOut.difference(_checkIn).inDays.clamp(1, 365);
      _amountCtrl.text =
          (widget.suggestedDaily! * nights).toStringAsFixed(2);
    }
  }

  @override
  void dispose() {
    _amountCtrl.dispose();
    super.dispose();
  }

  String _isoDate(DateTime d) {
    return '${d.year.toString().padLeft(4, '0')}-'
        '${d.month.toString().padLeft(2, '0')}-'
        '${d.day.toString().padLeft(2, '0')}';
  }

  void _recalcAmount() {
    if (widget.suggestedDaily == null) return;
    final nights = _checkOut.difference(_checkIn).inDays.clamp(1, 365);
    _amountCtrl.text =
        (widget.suggestedDaily! * nights).toStringAsFixed(2);
  }

  Future<void> _pickCheckIn() async {
    final d = await showDatePicker(
      context: context,
      initialDate: _checkIn,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (d != null && mounted) {
      setState(() {
        _checkIn = d;
        if (!_checkOut.isAfter(_checkIn)) {
          _checkOut = _checkIn.add(const Duration(days: 1));
        }
        _recalcAmount();
      });
    }
  }

  Future<void> _pickCheckOut() async {
    final d = await showDatePicker(
      context: context,
      initialDate: _checkOut,
      firstDate: _checkIn.add(const Duration(days: 1)),
      lastDate: DateTime.now().add(const Duration(days: 400)),
    );
    if (d != null && mounted) {
      setState(() {
        _checkOut = d;
        _recalcAmount();
      });
    }
  }

  Future<void> _submit() async {
    final userId = await SessionStore.getUserId();
    if (userId == null) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Register or sign in on the Account tab first.'),
          ),
        );
      }
      return;
    }
    final amount = _amountCtrl.text.trim();
    if (amount.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Enter total amount')),
      );
      return;
    }

    setState(() => _submitting = true);
    try {
      final id = await createBooking(
        userId: userId,
        listingId: widget.listingId,
        checkInIso: _isoDate(_checkIn),
        checkOutIso: _isoDate(_checkOut),
        totalAmount: amount,
      );
      if (!mounted) return;
      await showDialog<void>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Booking created'),
          content: Text('Booking #$id is pending. Open summary to confirm when ready.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('OK'),
            ),
            FilledButton(
              onPressed: () {
                Navigator.pop(ctx);
                Navigator.of(context).pushReplacement<void, void>(
                  MaterialPageRoute<void>(
                    builder: (_) => BookingSummaryScreen(bookingId: id),
                  ),
                );
              },
              child: const Text('View summary'),
            ),
          ],
        ),
      );
      if (mounted) Navigator.of(context).pop();
    } on BookingApiException catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.message)),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$e')),
        );
      }
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('New booking')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            widget.listingTitle,
            style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w600),
          ),
          const SizedBox(height: 20),
          ListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Check-in'),
            subtitle: Text(_isoDate(_checkIn)),
            trailing: const Icon(Icons.chevron_right),
            onTap: _pickCheckIn,
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Check-out'),
            subtitle: Text(_isoDate(_checkOut)),
            trailing: const Icon(Icons.chevron_right),
            onTap: _pickCheckOut,
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _amountCtrl,
            decoration: const InputDecoration(
              labelText: 'Total amount',
              border: OutlineInputBorder(),
              prefixText: '৳ ',
            ),
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
          ),
          const SizedBox(height: 28),
          FilledButton(
            onPressed: _submitting ? null : _submit,
            child: _submitting
                ? const SizedBox(
                    height: 22,
                    width: 22,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Create booking'),
          ),
        ],
      ),
    );
  }
}
