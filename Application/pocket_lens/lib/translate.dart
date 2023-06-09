import 'package:flutter/material.dart';
import 'package:alan_voice/alan_voice.dart';

class Translate extends StatefulWidget {
  const Translate({super.key});

  @override
  State<Translate> createState() => _TranslateState();
}

class _TranslateState extends State<Translate> {
  String _userInput = '';
  String _translatedText = '';

  void _translate() {
    setState(() {
      AlanVoice.sendText(_userInput);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Send Text To Alan'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            TextField(
              onChanged: (value) {
                _userInput = value;
              },
              decoration: InputDecoration(
                hintText: 'Enter text to translate',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: _translate,
              child: Text('Send Text To Alan'),
            ),
            SizedBox(height: 16.0),
            Text(
              _translatedText,
              style: TextStyle(fontSize: 18.0),
            ),
          ],
        ),
      ),
    );
  }
}
