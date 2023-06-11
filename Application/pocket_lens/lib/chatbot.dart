import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart';
import 'package:speech_to_text/speech_recognition_error.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'dart:convert';
import 'config.dart';

class ChatBot extends StatefulWidget {
  const ChatBot({super.key});

  @override
  State<ChatBot> createState() => _ChatBotState();
}

class _ChatBotState extends State<ChatBot> {
  final SpeechToText _speechToText = SpeechToText();
  bool _speechEnabled = false;
  String _lastWords = '';
  String _currentWords = '';

  @override
  void initState() {
    super.initState();
    // _initSpeech();
  }

  void _initSpeech() async {
    _speechEnabled = await _speechToText.initialize(
      onError: errorListener,
      onStatus: statusListener,
    );
    setState(() {});
  }

  /// Each time to start a speech recognition session
  // void _startListening() async {
  //   await _speechToText.listen(
  //     onResult: _onSpeechResult,
  //     // listenFor: const Duration(seconds: 100),
  //     // pauseFor: const Duration(seconds: 100),
  //     listenMode: ListenMode.dictation,
  //   );
  //   setState(() {});
  // }

  void errorListener(SpeechRecognitionError error) {
    debugPrint(error.errorMsg.toString());
  }

  /// Each time to start a speech recognition session
  Future _startListening() async {
    debugPrint("=================================================");
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
      // await _startListening();
    }
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
    setState(() {
      _lastWords = result.recognizedWords;
      // _sendText(_lastWords);
    });
  }

  // Future<void> _sendText(String text) async {
  //   var url = Uri.parse('http://$IP_ADDRESS/command');
  //   var response = await http.post(
  //     url,
  //     headers: <String, String>{
  //       'Content-Type': 'application/json; charset=UTF-8',
  //     },
  //     body: jsonEncode(
  //       <String, String>{
  //         "command": text,
  //       },
  //     ),
  //   );

  //   // print('Response status: ${response.statusCode}');
  //   debugPrint('Response body: ${response.body}');
  // }

  @override
  void dispose() {
    _speechToText.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Chatbot'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // Container(
            //   padding: const EdgeInsets.all(16),
            //   child: const Text(
            //     'Recognized words:',
            //     style: TextStyle(fontSize: 20.0),
            //   ),
            // ),
            // Expanded(
            //   child: Container(
            //     padding: const EdgeInsets.all(16),
            //     child: Text(
            //       // If listening is active show the recognized words
            //       _speechToText.isListening
            //           ? _lastWords
            //           // If listening isn't active but could be tell the user
            //           // how to start it, otherwise indicate that speech
            //           // recognition is not yet ready or not supported on
            //           // the target device
            //           : _speechEnabled
            //               ? _lastWords == ''
            //                   ? 'Tap the microphone to start listening...'
            //                   : _lastWords
            //               : 'Speech not available',
            //     ),
            //   ),
            // ),
          ],
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed:
      //       // If not yet listening for speech start, otherwise stop
      //       _speechToText.isNotListening ? _startListening : _stopListening,
      //   tooltip: 'Listen',
      //   child: Icon(_speechToText.isNotListening ? Icons.mic_off : Icons.mic),
      // ),
    );
  }
}
