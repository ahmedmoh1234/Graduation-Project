import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'dart:convert';
import 'config.dart';
import 'menu.dart';
import 'package:flutter_tts/flutter_tts.dart';

class Home extends StatefulWidget {
  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('This is the Home Page'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.max,
          children: [
            Image.asset(
              iconImagePath,
              color: Colors.white.withOpacity(0.2),
              colorBlendMode: BlendMode.modulate,
            ),
          ],
        ),
      ),
      drawer: Menu(
        name: 'Nader',
        email: 'naderyouhanna@gmail.com',
        gender: 'Male',
      ),
    );
  }
}
