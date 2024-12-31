import 'package:flutter/material.dart';
import '../widgets/card_form.dart';
import '../widgets/card_preview.dart';

class CardDesignerScreen extends StatelessWidget {
  const CardDesignerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Design Birthday Card'),
      ),
      body: const Row(
        children: [
          Expanded(
            flex: 1,
            child: CardForm(),
          ),
          Expanded(
            flex: 2,
            child: CardPreview(),
          ),
        ],
      ),
    );
  }
}