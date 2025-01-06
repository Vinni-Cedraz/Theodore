import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:5000';  // Flask backend

  Future<Map<String, dynamic>> generateCard({
    required String name,
    required String relationship,
    required String memory,
  }) async {
    final url = Uri.parse('$baseUrl/generate-card');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'relationship': relationship,
        'memory': memory,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to generate card');
    }
  }
}