import 'package:flutter/material.dart';
import '../models/birthday_card.dart';

class CardPreview extends StatelessWidget {
  final BirthdayCard? cardData;
  
  const CardPreview({
    super.key,
    this.cardData,
  });

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Container(
        color: Colors.grey[200],
        child: Column(
          children: [
            const TabBar(
              tabs: [
                Tab(text: 'Front Cover'),
                Tab(text: 'Inside Message'),
                Tab(text: 'Back Cover'),
              ],
            ),
            Expanded(
              child: TabBarView(
                children: [
                  _buildCoverPreview(),
                  _buildMessagePreview(),
                  _buildBackCoverPreview(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCoverPreview() {
    return Center(
      child: AspectRatio(
        aspectRatio: 0.7,
        child: Card(
          elevation: 8,
          child: cardData?.coverImageUrl != null
              ? Image.network(cardData!.coverImageUrl!)
              : Image.asset('assets/images/placeholders/front.jpg', fit: BoxFit.cover),
        ),
      ),
    );
  }

  Widget _buildMessagePreview() {
    return Center(
      child: AspectRatio(
        aspectRatio: 1.4,
        child: Card(
          elevation: 8,
          child: cardData?.message != null
              ? Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(cardData!.message!),
                )
              : Image.asset('assets/images/placeholders/body.jpg', fit: BoxFit.cover),
        ),
      ),
    );
  }

  Widget _buildBackCoverPreview() {
    return Center(
      child: AspectRatio(
        aspectRatio: 0.7,
        child: Card(
          elevation: 8,
          child: cardData?.backCoverText != null
              ? Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(cardData!.backCoverText!),
                )
              : Image.asset('assets/images/placeholders/back.jpg', fit: BoxFit.cover),
        ),
      ),
    );
  }
}