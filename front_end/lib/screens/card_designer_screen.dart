import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CardDesignerScreen extends StatefulWidget {
  const CardDesignerScreen({super.key});

  @override
  _CardDesignerScreenState createState() => _CardDesignerScreenState();
}

class _CardDesignerScreenState extends State<CardDesignerScreen> {
  final ApiService apiService = ApiService();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController relationshipController = TextEditingController();
  final TextEditingController memoryController = TextEditingController();

  String? message;
  String? frontImageUrl;
  String? bodyImageUrl;
  String? backImageUrl;

  Future<void> generateCard() async {
    try {
      final result = await apiService.generateCard(
        name: nameController.text,
        relationship: relationshipController.text,
        memory: memoryController.text,
      );
      setState(() {
        message = result['message'];
        frontImageUrl = result['frontImageUrl'];
        bodyImageUrl = result['bodyImageUrl'];
        backImageUrl = result['backImageUrl'];
      });
    } catch (e) {
      // Handle error
      print('Error generating card: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error generating card: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Card Designer'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: nameController,
              decoration: const InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: relationshipController,
              decoration: const InputDecoration(labelText: 'Relationship'),
            ),
            TextField(
              controller: memoryController,
              decoration: const InputDecoration(labelText: 'Memory'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: generateCard,
              child: const Text('Generate Card'),
            ),
            if (message != null) ...[
              const SizedBox(height: 20),
              Text('Message: $message'),
              if (frontImageUrl != null) Image.network(frontImageUrl!),
              if (bodyImageUrl != null) Image.network(bodyImageUrl!),
              if (backImageUrl != null) Image.network(backImageUrl!),
            ],
          ],
        ),
      ),
    );
  }
}