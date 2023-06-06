import 'package:flutter/material.dart';
import 'config.dart';

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
                    widget.changeLanguage();
                  } else {
                    useArabic = false;
                    widget.changeLanguage();
                  }
                },
              );
            },
          );
        },
      ),
    );
  }
}
