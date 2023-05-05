import 'package:flutter/material.dart';
import 'startup.dart';
import 'package:camera/camera.dart';

List<CameraDescription> cameras;
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();

  runApp(
    MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      // theme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: StartUp(),
    ),
  );
}
