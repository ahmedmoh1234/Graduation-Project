import 'package:flutter/material.dart';
import 'config.dart';
import 'menu.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'dart:io' show Platform;

class Home extends StatefulWidget {
  @override
  State<Home> createState() => _HomeState();
}

enum TtsState { playing, stopped, paused, continued }

class _HomeState extends State<Home> {
  //===========================TEXT TO SPEECH===================================
  late FlutterTts flutterTts;
  double volume = 4;
  double pitch = 1.0;
  double rate = 0.5;
  final String _voiceText = '''Hi, this is the Home Page
  Please speak the module name to navigate to it''';
  TtsState ttsState = TtsState.stopped;

  get isPlaying => ttsState == TtsState.playing;
  get isStopped => ttsState == TtsState.stopped;
  get isPaused => ttsState == TtsState.paused;
  get isContinued => ttsState == TtsState.continued;

  bool get isIOS => !kIsWeb && Platform.isIOS;
  bool get isAndroid => !kIsWeb && Platform.isAndroid;
  bool get isWindows => !kIsWeb && Platform.isWindows;
  bool get isWeb => kIsWeb;

  Future _speak() async {
    await flutterTts.setVolume(volume);
    await flutterTts.setSpeechRate(rate);
    await flutterTts.setPitch(pitch);

    await flutterTts.speak(_voiceText);
  }

  Future _setAwaitOptions() async {
    await flutterTts.awaitSpeakCompletion(true);
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

  //===========================SPEECH TO TEXT===================================

  SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String _lastWords = '';
  String _currentWords = '';

  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize(
      onError: errorListener,
      onStatus: statusListener,
    );
    setState(() {});
  }

  void errorListener(SpeechRecognitionError error) {
    debugPrint(error.errorMsg.toString());
  }

  void statusListener(String status) async {
    debugPrint("status $status");
    if (status == "done" && _speechEnabled) {
      setState(
        () {
          _lastWords += " $_currentWords";
          _currentWords = "";
          _speechEnabled = false;
        },
      );
      await _startListening();
    }
  }

  /// Each time to start a speech recognition session
  Future _startListening() async {
    debugPrint("================START LISTENING==========================");
    await _stopListening();
    await Future.delayed(const Duration(milliseconds: 50));
    await _speechToText.listen(
      onResult: _onSpeechResult,
      listenMode: ListenMode.dictation,
    );
    setState(
      () {
        _speechEnabled = true;
      },
    );
  }

  /// Manually stop the active speech recognition session
  /// Note that there are also timeouts that each platform enforces
  /// and the SpeechToText plugin supports setting timeouts on the
  /// listen method.
  Future _stopListening() async {
    setState(
      () {
        _speechEnabled = false;
      },
    );
    await _speechToText.stop();
  }

  /// This is the callback that the SpeechToText plugin calls when
  /// the platform returns recognized words.
  void _onSpeechResult(SpeechRecognitionResult result) {
    debugPrint('Last Words = $_lastWords');
    setState(() {
      _lastWords = result.recognizedWords;
      // _sendText(_lastWords);
    });
  }

  //===========================WIDGET FUNCTIONS===================================

  @override
  void initState() {
    super.initState();
    initTts();
    _initSpeech();
    WidgetsBinding.instance.addPostFrameCallback(
      (_) async {
        await _speak();
        await _startListening();
      },
    );
  }

  @override
  void dispose() {
    super.dispose();
    flutterTts.stop();
    _speechToText.stop();
  }

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
