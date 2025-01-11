import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dart:convert';

class CardDesignerScreen extends StatefulWidget {
  const CardDesignerScreen({super.key});
  @override
  State<CardDesignerScreen> createState() => _CardDesignerScreenState();
}

class _CardDesignerScreenState extends State<CardDesignerScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController relationshipController = TextEditingController();
  final TextEditingController memoryController = TextEditingController();

  String? bottomImage;
  String? topImage;
  String? birthdayMessage;
  bool isLoading = false;

  Future<void> generateCard() async {
    setState(() => isLoading = true);
    try {
      // Step 1: Generate images
      final imagesResult = await _apiService.generateImages(
        relationship: relationshipController.text,
        memory: memoryController.text,
      );
      setState(() {
        bottomImage = imagesResult['bottom_image'];
        topImage = imagesResult['top_image'];
      });

      // Step 2: Generate birthday message
      final messageResult = await _apiService.generateBirthdayMessage(
        name: nameController.text,
        relationship: relationshipController.text,
        memory: memoryController.text,
      );
      setState(() => birthdayMessage = messageResult['message']);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Card Designer')),
      body: Padding(
        padding: const EdgeInsets.all(16),
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
            if (isLoading)
              const CircularProgressIndicator()
            else
              ElevatedButton(
                onPressed: generateCard,
                child: const Text('Generate Card'),
              ),
            const SizedBox(height: 20),
            Expanded(
              child: Stack(
                children: [
                  Positioned.fill(
                    child: Image.asset(
                      'assets/images/placeholders/body.png',
                      fit: BoxFit.contain,
                    ),
                  ),
                  if (bottomImage != null)
                    Positioned(
                      left: 256,
                      bottom: 256,
                      child: Image.memory(
                        base64Decode(bottomImage!),
                        width: 512,
                        height: 512,
                      ),
                    ),
                  if (topImage != null)
                    Positioned(
                      right: 256,
                      top: 256,
                      child: Image.memory(
                        base64Decode(topImage!),
                        width: 512,
                        height: 512,
                      ),
                    ),
                  if (birthdayMessage != null)
                    Positioned(
                      left: 256,
                      top: 256,
                      child: Container(
                        constraints: BoxConstraints(
                          maxWidth: MediaQuery.of(context).size.width - 512,
                        ),
                        padding: const EdgeInsets.all(8.0),
                        color: Colors.white.withAlpha(
                            179), // Background color to ensure readability
                        child: Text(
                          birthdayMessage!,
                          style: TextStyle(
                            fontSize: 40, // Adjust font size
                            color: Colors.grey.shade800,
                            height: 1.2,
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
