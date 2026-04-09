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
