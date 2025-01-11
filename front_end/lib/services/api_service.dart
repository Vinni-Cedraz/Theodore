import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://127.0.0.1:5000';

  Future<Map<String, dynamic>> generateImages({
    required String relationship,
    required String memory,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/generate-images'),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: jsonEncode({
        'relationship': relationship,
        'memory': memory,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to generate images: ${response.statusCode}');
    }
  }

  Future<Map<String, dynamic>> generateBirthdayMessage({
    required String name,
    required String relationship,
    required String memory,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/generate-birthday-message'),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: jsonEncode({
        'name': name,
        'relationship': relationship,
        'memory': memory,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to generate message: ${response.statusCode}');
    }
  }
}
