import 'package:flutter/foundation.dart';

/// Backend base URL (no trailing slash).
///
/// Default behavior:
/// - Web/Chrome: `http://localhost:8001`
/// - Android emulator: `http://10.0.2.2:8001`
/// - Other mobile/desktop: `http://localhost:8001` (override with `API_BASE`)
///
/// Override anytime:
/// `flutter run --dart-define=API_BASE=http://YOUR_HOST:PORT`
const String _apiBaseFromEnv = String.fromEnvironment('API_BASE', defaultValue: '');

String get kApiBase {
  if (_apiBaseFromEnv.isNotEmpty) return _apiBaseFromEnv;
  if (kIsWeb) return 'http://localhost:8001';
  if (defaultTargetPlatform == TargetPlatform.android) {
    return 'http://10.0.2.2:8001';
  }
  return 'http://localhost:8001';
}
