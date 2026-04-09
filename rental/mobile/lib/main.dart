import 'package:flutter/material.dart';

import 'screens/home_map_screen.dart';

void main() {
  runApp(const UrbanReliefApp());
}

class UrbanReliefApp extends StatelessWidget {
  const UrbanReliefApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UrbanRelief',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const HomeMapScreen(),
    );
  }
}
