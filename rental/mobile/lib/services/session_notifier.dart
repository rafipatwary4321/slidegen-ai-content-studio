import 'package:flutter/foundation.dart';

/// Fired after sign-in / sign-out on Account tab so Map/Explore can refresh viewer id.
class SessionNotifier extends ChangeNotifier {
  SessionNotifier._();
  static final SessionNotifier instance = SessionNotifier._();

  void notifySessionChanged() => notifyListeners();
}
