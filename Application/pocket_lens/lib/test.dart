import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'dart:convert';
import 'config.dart';
import 'package:flutter_tts/flutter_tts.dart';

class Test extends StatefulWidget {
  const Test({super.key});

  @override
  State<Test> createState() => _TestState();
}

class _TestState extends State<Test> {
  Future<void> sendImagetoServer() async {
    //Send to the endpoint test
    var url = Uri.parse('http://$IP_ADDRESS/test');
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    final extractedMyInfo = json.decode(response.body) as Map<String, dynamic>;
    debugPrint(extractedMyInfo.toString());
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Clothes Descriptor'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      floatingActionButton: FloatingActionButton.large(
        // Provide an onPressed callback.
        onPressed: () async {
          await sendImagetoServer();
        },
        child: const Icon(Icons.car_repair_sharp),
      ),
    );
  }
}

class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Display the Picture')),
      // The image is stored as a file on the device. Use the `Image.file`
      // constructor with the given path to display the image.
      body: Image.file(File(imagePath)),
    );
  }
}
