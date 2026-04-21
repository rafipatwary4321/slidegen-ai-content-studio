import 'package:shared_preferences/shared_preferences.dart';

const _kUserId = 'urbanrelief_user_id';

class SessionStore {
  static Future<int?> getUserId() async {
    final p = await SharedPreferences.getInstance();
    final v = p.getInt(_kUserId);
    return v != null && v > 0 ? v : null;
  }

  static Future<void> setUserId(int id) async {
    final p = await SharedPreferences.getInstance();
    await p.setInt(_kUserId, id);
  }

  static Future<void> clearUserId() async {
    final p = await SharedPreferences.getInstance();
    await p.remove(_kUserId);
  }
}
