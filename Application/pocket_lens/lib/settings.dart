import 'package:flutter/material.dart';
import 'config.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class LanguageSettingsPage extends StatefulWidget {
  final VoidCallback changeLanguage;
  const LanguageSettingsPage({required this.changeLanguage});

  @override
  _LanguageSettingsPageState createState() => _LanguageSettingsPageState();
}

class _LanguageSettingsPageState extends State<LanguageSettingsPage> {
  String? _selectedLanguage = null; // default language

  List<String> _languagesEnglish = [
    'English',
    'Arabic',
  ];

  List<String> _languagesArabic = [
    'الانجليزية',
    'العربية',
  ];

  Future<void> setLanguageServer(bool value) async {
    final url = Uri.parse('http://$IP_ADDRESS/set-language');
    final headers = {'Content-Type': 'application/json'};
    final body = json.encode(
      {'useArabic': value},
    );
    final response = await http.post(url, headers: headers, body: body);
    if (response.statusCode == 200) {
      final result = json.decode(response.body);
      print('Boolean value changed to $result');
    } else {
      print('Error changing boolean value: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          useArabic ? 'اختيار اللغة' : 'Language Settings',
        ),
      ),
      body: ListView.builder(
        itemCount: _languagesEnglish.length,
        itemBuilder: (context, index) {
          final language = _selectedLanguage == 'Arabic'
              ? _languagesArabic[index]
              : _languagesEnglish[index];
          return RadioListTile(
            title: Text(language),
            value: language,
            groupValue: _selectedLanguage,
            onChanged: (value) {
              setState(
                () {
                  _selectedLanguage = value.toString();
                  if (_selectedLanguage == 'Arabic') {
                    useArabic = true;
                  } else {
                    useArabic = false;
                  }
                  widget.changeLanguage();
                  setLanguageServer(useArabic);
                },
              );
            },
          );
        },
      ),
    );
  }
}
