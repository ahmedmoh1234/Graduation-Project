import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'dart:convert';
import 'package:flutter_tts/flutter_tts.dart';

enum TtsState { playing, stopped, paused, continued }

class ClothesDescriptor extends StatefulWidget {
  const ClothesDescriptor({super.key});

  @override
  State<ClothesDescriptor> createState() => _ClothesDescriptorState();
}

class _ClothesDescriptorState extends State<ClothesDescriptor> {
  late CameraController _controller;
  late FlutterTts flutterTts;
  double volume = 3;
  double pitch = 1.0;
  double rate = 0.5;
  late Future<void> _initializeControllerFuture;
  late CameraDescription camera;
  TtsState ttsState = TtsState.stopped;

  get isPlaying => ttsState == TtsState.playing;
  get isStopped => ttsState == TtsState.stopped;
  get isPaused => ttsState == TtsState.paused;
  get isContinued => ttsState == TtsState.continued;

  bool get isIOS => !kIsWeb && Platform.isIOS;
  bool get isAndroid => !kIsWeb && Platform.isAndroid;
  bool get isWindows => !kIsWeb && Platform.isWindows;
  bool get isWeb => kIsWeb;

  late var detectedClothesList = [];
  late var detectedClothesDict = {};
  late var clothesDetected = false;
  Future _speak(voiceText) async {
    await flutterTts.setVolume(volume);
    await flutterTts.setSpeechRate(rate);
    await flutterTts.setPitch(pitch);

    await flutterTts.speak(voiceText);
  }

  Future _setAwaitOptions() async {
    await flutterTts.awaitSpeakCompletion(true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
    flutterTts.stop();
  }

  initTts() {
    flutterTts = FlutterTts();

    _setAwaitOptions();

    if (isAndroid) {
      _getDefaultEngine();
      _getDefaultVoice();
    }

    flutterTts.setStartHandler(() {
      setState(() {
        print("Playing");
        ttsState = TtsState.playing;
      });
    });

    if (isAndroid) {
      flutterTts.setInitHandler(() {
        setState(() {
          print("TTS Initialized");
        });
      });
    }

    flutterTts.setCompletionHandler(() {
      setState(() {
        print("Complete");
        ttsState = TtsState.stopped;
      });
    });

    flutterTts.setCancelHandler(() {
      setState(() {
        print("Cancel");
        ttsState = TtsState.stopped;
      });
    });

    flutterTts.setPauseHandler(() {
      setState(() {
        print("Paused");
        ttsState = TtsState.paused;
      });
    });

    flutterTts.setContinueHandler(() {
      setState(() {
        print("Continued");
        ttsState = TtsState.continued;
      });
    });

    flutterTts.setErrorHandler((msg) {
      setState(() {
        print("error: $msg");
        ttsState = TtsState.stopped;
      });
    });

    flutterTts.setLanguage('en-US').then((_) {
      setState(() {});
    });
  }

  Future _getDefaultEngine() async {
    var engine = await flutterTts.getDefaultEngine;
    if (engine != null) {
      print(engine);
    }
  }

  Future _getDefaultVoice() async {
    var voice = await flutterTts.getDefaultVoice;
    if (voice != null) {
      print(voice);
    }
  }

  Future<void> sendImagetoServer(XFile image) async {
    var stream = http.ByteStream(image.openRead());
    stream.cast();

    var length = await image.length();
    var url = Uri.parse('http://$IP_ADDRESS/clothes-descriptor');
    var request = http.MultipartRequest('POST', url);
    var multipartFile = http.MultipartFile(
      'image',
      stream,
      length,
      filename: basename(image.path),
    );

    request.files.add(multipartFile);

    var streamedResponse = await request.send();

    var response = await http.Response.fromStream(streamedResponse);
    debugPrint('************************ Response: ${response}');
    debugPrint('************************ Response: ${response.body}');

    var extractedInfo = json.decode(response.body) as Map<String, dynamic>;
    var responseString = extractedInfo['response_string'] as String;
    await _speak(responseString);

    if (responseString == 'No clothes detected') {
      clothesDetected = false;
      return;
    }
    clothesDetected = true;

    detectedClothesList = extractedInfo['detected_clothes'] as List<dynamic>;
    detectedClothesDict['type'] = detectedClothesList[0];
    detectedClothesDict['texture'] = detectedClothesList[1];
    detectedClothesDict['color'] = detectedClothesList[2];
    debugPrint('************************ ${detectedClothesDict}');
    debugPrint('************************ ${clothesDetected}');
  }

  Future<void> _addPreference(Map<dynamic, dynamic> detectedClothes) async {
    var url = Uri.parse('http://$IP_ADDRESS/apparel-pref');
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode({
        'color': detectedClothes['color'],
        'texture': detectedClothes['texture'],
        'clothesType': detectedClothes['type'],
      }),
    );

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    // final extractedMyInfo = json.decode(response.body) as Map<String, dynamic>;
    // debugPrint(extractedMyInfo.toString());
  }

  Future<void> _addToDatabase(Map<dynamic, dynamic> detectedClothes) async {
    var url = Uri.parse('http://$IP_ADDRESS/apparel-pref');
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode({
        'color': detectedClothes['color'],
        'texture': detectedClothes['texture'],
        'clothesType': detectedClothes['type'],
      }),
    );

    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');

    final extractedMyInfo = json.decode(response.body) as Map<String, dynamic>;
    debugPrint(extractedMyInfo.toString());
  }

  Future<void> captureImage(BuildContext context) async {
    try {
      //Initialize camera
      await _initializeControllerFuture;

      // Take a picture
      final image = await _controller.takePicture();

      if (!mounted) return;

      //Display image on a new screen
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (context) => DisplayPictureScreen(
            imagePath: image.path,
          ),
        ),
      );

      //Send image to server
      await sendImagetoServer(image);

      if (clothesDetected) {
        debugPrint(
            '=====Detected Clothes = $detectedClothesDict =============');
        _speak('Do you want to add this to your preferences ?');

        // Show Dialog Box
        // ignore: use_build_context_synchronously
        var choice1 = await showDialog(
          context: context,
          builder: (BuildContext context) => AlertDialog(
            title: const Text(
              'Future Recommendations',
            ),
            content: const Text(
              'Do you want to add this to your preferences ?',
              textAlign: TextAlign.center,
            ),
            actions: <Widget>[
              TextButton(
                onPressed: () {
                  debugPrint('Yes');
                  Navigator.pop(context, 'Yes');
                },
                child: const Text(
                  'Yes',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.green,
                    fontSize: 18,
                  ),
                ),
              ),
              TextButton(
                onPressed: () {
                  debugPrint('No');
                  Navigator.pop(context, 'No');
                },
                child: const Text(
                  'No',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                    fontSize: 18,
                  ),
                ),
              ),
            ],
            alignment: Alignment.center,
            icon: const Icon(
              Icons.recommend_rounded,
              color: Colors.green,
              size: 30,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
            actionsAlignment: MainAxisAlignment.spaceEvenly,
          ),
        );
        debugPrint('=====Choice = $choice1 =============');

        if (choice1 == 'No') {
          _speak('Do you want to add this to the Wardrobe ?');
          _addPreference(detectedClothesDict);
          // Show Dialog Box
          // ignore: use_build_context_synchronously
          var choice2 = await showDialog(
            context: context,
            builder: (BuildContext context) => AlertDialog(
              title: const Text(
                'Future Recommendations',
              ),
              content: const Text(
                'Do you want to add this to the Wardrobe ?',
                textAlign: TextAlign.center,
              ),
              actions: <Widget>[
                TextButton(
                  onPressed: () {
                    debugPrint('Yes');
                    Navigator.pop(context, 'Yes');
                  },
                  child: const Text(
                    'Yes',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.green,
                      fontSize: 18,
                    ),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    debugPrint('No');
                    Navigator.pop(context, 'No');
                  },
                  child: const Text(
                    'No',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.red,
                      fontSize: 18,
                    ),
                  ),
                ),
              ],
              alignment: Alignment.center,
              icon: const Icon(
                Icons.man,
                color: Colors.blue,
                size: 30,
              ),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
              actionsAlignment: MainAxisAlignment.spaceEvenly,
            ),
          );

          debugPrint('=====Choice = $choice2 =============');

          if (choice2 == 'Yes') {
            _speak('Adding this to Database');
            _addToDatabase(detectedClothesDict);
          }
        }
      }
      Navigator.pop(context);
    } catch (e) {
      print(e);
    }
  }

  @override
  void initState() {
    super.initState();
    camera = cameras[0];
    _controller = CameraController(
      camera,
      ResolutionPreset.medium,
    );

    _initializeControllerFuture = _controller.initialize();

    initTts();
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
      body: FutureBuilder<void>(
        future: _initializeControllerFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done) {
            // If the Future is complete, display the preview.
            return CameraPreview(_controller);
          } else {
            // Otherwise, display a loading indicator.
            return const Center(child: CircularProgressIndicator());
          }
        },
      ),
      floatingActionButton: FloatingActionButton.large(
        // Provide an onPressed callback.
        onPressed: () async {
          await captureImage(context);
        },
        child: const Icon(Icons.camera_alt),
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
