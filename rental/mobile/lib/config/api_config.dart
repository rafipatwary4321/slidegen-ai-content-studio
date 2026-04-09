/// Backend base URL (no trailing slash).
/// Android emulator: `flutter run --dart-define=API_BASE=http://10.0.2.2:8000`
/// If port 8000 is already in use, run API on another port and set `API_BASE` accordingly.
/// Physical device: use your machine LAN IP + port.
/// Optional Bachelor match on map search: `--dart-define=VIEWER_USER_ID=<guest id>`
/// (printed by `python scripts/seed_demo.py`).
const String kApiBase = String.fromEnvironment(
  'API_BASE',
  defaultValue: 'http://127.0.0.1:8000',
);
