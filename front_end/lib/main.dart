import 'package:flutter/material.dart';
import 'screens/card_designer_screen.dart';

void main() {
  runApp(const BirthdayCardApp());
}

class BirthdayCardApp extends StatelessWidget {
  const BirthdayCardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Birthday Card Designer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const CardDesignerScreen(),
    );
  }
}