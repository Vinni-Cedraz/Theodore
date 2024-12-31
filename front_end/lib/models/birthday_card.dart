class BirthdayCard {
  final String recipientName;
  final String relationship;
  final String memory;
  String? coverImageUrl;
  String? message;
  String? backCoverText;  // New field

  BirthdayCard({
    required this.recipientName,
    required this.relationship,
    required this.memory,
    this.coverImageUrl,
    this.message,
    this.backCoverText,
  });
}