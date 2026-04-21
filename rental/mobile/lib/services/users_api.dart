import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/app_user.dart';

class UsersApiException implements Exception {
  UsersApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;

  @override
  String toString() => 'UsersApiException($statusCode): $message';
}

Future<AppUser> createUser({
  required String fullName,
  required String phone,
  required String email,
  String role = 'Guest',
}) async {
  final uri = Uri.parse('$kApiBase/api/v1/users');
  final body = jsonEncode({
    'full_name': fullName,
    'phone': phone,
    'email': email,
    'role': role,
  });
  final res = await http.post(
    uri,
    headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
    body: body,
  );
  if (res.statusCode == 201) {
    final map = jsonDecode(res.body) as Map<String, dynamic>;
    return AppUser.fromJson(map);
  }
  var detail = res.body;
  try {
    final err = jsonDecode(res.body) as Map<String, dynamic>;
    detail = err['detail']?.toString() ?? res.body;
  } catch (_) {}
  throw UsersApiException(detail, statusCode: res.statusCode);
}
