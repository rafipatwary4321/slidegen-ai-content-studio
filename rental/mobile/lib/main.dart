import 'package:flutter/material.dart';

import 'screens/main_shell.dart';

void main() {
  runApp(const UrbanReliefApp());
}

class UrbanReliefApp extends StatelessWidget {
  const UrbanReliefApp({super.key});

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xFF0D9488);
    return MaterialApp(
      title: 'UrbanRelief',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: seed,
          brightness: Brightness.dark,
        ),
        fontFamily: 'Roboto',
        navigationBarTheme: NavigationBarThemeData(
          indicatorColor: seed.withOpacity(0.35),
        ),
      ),
      home: const MainShell(),
    );
  }
}
