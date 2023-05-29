import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:pocket_lens/currency_recognizer.dart';
import 'package:pocket_lens/document_reader.dart';
import 'package:pocket_lens/product-identifier.dart';
import 'config.dart';
import 'menu.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'dart:io' show Platform;
import 'package:alan_voice/alan_voice.dart';

import 'package:pocket_lens/ChangeIPAddress.dart';
import 'package:pocket_lens/barcode_reader.dart';
import 'package:pocket_lens/clothes_descriptor.dart';
import 'package:pocket_lens/emotion_recognizer.dart';
import 'scene_descriptor.dart';
import 'face_detector.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

enum TtsState { playing, stopped, paused, continued }

//===========================GO TO FUNCTIONS===================================

void _goToBarcodeReader(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const BarcodeReader();
      },
    ),
  );
}

void _goToSceneDescriptor(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const SceneDescriptor();
      },
    ),
  );
}

void _goToFaceDetector(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const FaceDetector();
      },
    ),
  );
}

void _goToChangeIPAddress(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const ChangeIPAddress();
      },
    ),
  );
}

void _goToEmotionRecognizer(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const EmotionRecognizer();
      },
    ),
  );
}

void _goToClothesDescriptor(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const ClothesDescriptor();
      },
    ),
  );
}

void _goToDocumentReader(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const DocumentReader();
      },
    ),
  );
}

void _goToCurrencyRecognizer(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const CurrencyRecognizer();
      },
    ),
  );
}

_goToProductIdentifier(BuildContext context) {
  Navigator.of(context).push(
    MaterialPageRoute(
      builder: (_) {
        return const ProductIdentifier();
      },
    ),
  );
}

_goToHome(BuildContext ctx) {
  Navigator.of(ctx).push(
    MaterialPageRoute(
      builder: (_) {
        return const Home();
      },
    ),
  );
}

class _HomeState extends State<Home> {
  //===========================TEXT TO SPEECH===================================
  late FlutterTts flutterTts;
  double volume = 4;
  double pitch = 1.0;
  double rate = 0.5;
  final String _greetingString =
      'Hi, this is the Home Page. Please speak the module name to navigate to it.';
  bool _greetingIsPlayed = false;
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

    await flutterTts.speak(_greetingString);
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

  final SpeechToText _speechToText = SpeechToText();
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

  //===========================ALAN FUNCTIONS===================================

  void _initAlan() {
    /// Init Alan Button with project key from Alan AI Studio
    AlanVoice.addButton(
        "95aec1209fe5ec07ce09fa461da220842e956eca572e1d8b807a3e2338fdd0dc/stage",
        buttonAlign: AlanVoice.BUTTON_ALIGN_RIGHT);

    /// Handle commands from Alan AI Studio
    AlanVoice.onCommand.add(
      (command) {
        debugPrint("got new command ${command.toString()}");
        var commandName = command.data["command"];
        if (commandName == 'Scene Descriptor') {
          _goToSceneDescriptor(context);
        } else if (commandName == 'Face Recognizer') {
          _goToFaceDetector(context);
        } else if (commandName == 'Emotion Recognizer') {
          _goToEmotionRecognizer(context);
        } else if (commandName == 'Barcode') {
          _goToBarcodeReader(context);
        } else if (commandName == 'Clothes') {
          _goToClothesDescriptor(context);
        } else if (commandName == 'Currency Recognizer') {
          _goToCurrencyRecognizer(context);
        } else if (commandName == 'Document Reader') {
          _goToDocumentReader(context);
        } else if (commandName == 'Product Identifier') {
          _goToProductIdentifier(context);
        } else if (commandName == 'Home') {
          _goToHome(context);
        } else if (commandName == 'Menu') {
          // Scaffold.of(context).openDrawer();
          _scaffoldKey.currentState!.openDrawer();
        } else if (commandName == 'Back') {
          debugPrint(
              '---------------------------------------------------------');
          debugPrint("I am inside ${context.widget.runtimeType}");
          debugPrint(
              '---------------------------------------------------------');
          if (Navigator.canPop(context)) {
            Navigator.pop(context);
          }
        } else if (commandName == 'Exit') {
          AlanVoice.deactivate();
          //Exit application
          SystemChannels.platform.invokeMethod('SystemNavigator.pop');
        }
      },
    );
  }

  void _greetingByAlan() {
    AlanVoice.onButtonState.add((state) {
      if (state.name == "ONLINE" && !_greetingIsPlayed) {
        _greetingIsPlayed = true;
        AlanVoice.activate();
        AlanVoice.playText(
          _greetingString,
        );
      }
    });
  }

  /// Deactivate Alan Button programmatically
  void _deactivateAlan() {
    AlanVoice.deactivate();
  }

  //===========================WIDGET FUNCTIONS===================================
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    initTts();
    _initSpeech();
    WidgetsBinding.instance.addPostFrameCallback(
      (_) async {
        await _speak();
        // await _startListening();
      },
    );

    _initAlan();
    // _greetingByAlan();
    // _deactivateAlan();
  }

  @override
  void dispose() {
    super.dispose();
    flutterTts.stop();
    _deactivateAlan();
    // _speechToText.stop();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
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
