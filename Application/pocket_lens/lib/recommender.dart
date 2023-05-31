// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

import 'package:flutter_tts/flutter_tts.dart';

enum TtsState { playing, stopped, paused, continued }

class Recommender extends StatefulWidget {
  const Recommender({super.key});

  @override
  State<Recommender> createState() => _RecommenderState();
}

class _RecommenderState extends State<Recommender> {
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

      _speak('Do you like this ?');

      // Show Dialog Box
      var choice1 = await showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: const Text(
            'Recommender',
          ),
          content: const Text(
            'Do you like this ?',
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

      if (choice1 == 'Yes') {
        _speak('Do you want to add this to the Database ?');

        // Show Dialog Box
        var choice2 = await showDialog(
          context: context,
          builder: (BuildContext context) => AlertDialog(
            title: const Text(
              'Recommender',
            ),
            content: const Text(
              'Do you want to add this ?',
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

        debugPrint('=====Choice = $choice2 =============');

        if (choice2 == 'Yes') {
          _speak('Adding this to Database');
        }
      }

      Navigator.pop(context);
    } catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Recommender'),
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

// class RecommendDialog extends StatelessWidget {
//   const RecommendDialog({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return const TextButton();
//   }
// }
