import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

import '../config/api_config.dart';

class AuthApiException implements Exception {
  AuthApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;

  @override
  String toString() => 'AuthApiException($statusCode): $message';
}

/// Multipart NID upload → 202 Accepted.
Future<Map<String, dynamic>> verifyNid({
  required int userId,
  required List<int> fileBytes,
  String filename = 'nid.jpg',
}) async {
  final uri = Uri.parse('$kApiBase/api/v1/auth/verify-nid');
  final lower = filename.toLowerCase();
  final MediaType mediaType = lower.endsWith('.png')
      ? MediaType('image', 'png')
      : lower.endsWith('.pdf')
          ? MediaType('application', 'pdf')
          : MediaType('image', 'jpeg');

  final request = http.MultipartRequest('POST', uri)
    ..fields['user_id'] = '$userId'
    ..files.add(
      http.MultipartFile.fromBytes(
        'file',
        fileBytes,
        filename: filename,
        contentType: mediaType,
      ),
    );

  final streamed = await request.send();
  final res = await http.Response.fromStream(streamed);
  if (res.statusCode == 202) {
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
  var detail = res.body;
  try {
    final err = jsonDecode(res.body) as Map<String, dynamic>;
    detail = err['detail']?.toString() ?? res.body;
  } catch (_) {}
  throw AuthApiException(detail, statusCode: res.statusCode);
}
