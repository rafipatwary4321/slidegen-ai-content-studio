import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/booking_summary.dart';

class BookingApiException implements Exception {
  BookingApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;

  @override
  String toString() => 'BookingApiException($statusCode): $message';
}

Future<BookingSummary> fetchBookingSummary(int bookingId) async {
  final uri = Uri.parse('$kApiBase/api/v1/bookings/$bookingId/summary');
  final response = await http.get(uri, headers: {'Accept': 'application/json'});
  if (response.statusCode == 200) {
    final map = json.decode(response.body) as Map<String, dynamic>;
    return BookingSummary.fromJson(map);
  }
  String detail = response.body;
  try {
    final err = json.decode(response.body) as Map<String, dynamic>;
    detail = err['detail']?.toString() ?? response.body;
  } catch (_) {}
  throw BookingApiException(detail, statusCode: response.statusCode);
}

Future<int> createBooking({
  required int userId,
  required int listingId,
  required String checkInIso,
  required String checkOutIso,
  required String totalAmount,
}) async {
  final uri = Uri.parse('$kApiBase/api/v1/bookings');
  final body = jsonEncode({
    'user_id': userId,
    'listing_id': listingId,
    'check_in': checkInIso,
    'check_out': checkOutIso,
    'total_amount': totalAmount,
  });
  final res = await http.post(
    uri,
    headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
    body: body,
  );
  if (res.statusCode == 201) {
    final map = jsonDecode(res.body) as Map<String, dynamic>;
    return (map['id'] as num).toInt();
  }
  var detail = res.body;
  try {
    final err = jsonDecode(res.body) as Map<String, dynamic>;
    detail = err['detail']?.toString() ?? res.body;
  } catch (_) {}
  throw BookingApiException(detail, statusCode: res.statusCode);
}

Future<BookingSummary> confirmBooking(int bookingId) async {
  final uri = Uri.parse('$kApiBase/api/v1/bookings/$bookingId/confirm');
  final res = await http.post(uri, headers: {'Accept': 'application/json'});
  if (res.statusCode == 200) {
    final map = jsonDecode(res.body) as Map<String, dynamic>;
    final summary = map['summary'] as Map<String, dynamic>;
    return BookingSummary.fromJson(summary);
  }
  var detail = res.body;
  try {
    final err = jsonDecode(res.body) as Map<String, dynamic>;
    detail = err['detail']?.toString() ?? res.body;
  } catch (_) {}
  throw BookingApiException(detail, statusCode: res.statusCode);
}
