class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';  // Future Django backend

  Future<Map<String, dynamic>> generateCard({
    required String name,
    required String relationship,
    required String memory,
  }) async {
    // TODO: Implement API call to backend
    return {
      'imageUrl': 'placeholder_url',
      'message': 'placeholder message',
    };
  }
}