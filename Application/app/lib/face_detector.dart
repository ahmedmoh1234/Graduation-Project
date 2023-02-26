import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:async/async.dart';
import 'package:path/path.dart';

class FaceDetector extends StatefulWidget {
  const FaceDetector({super.key});

  @override
  State<FaceDetector> createState() => _FaceDetectorState();
}

class _FaceDetectorState extends State<FaceDetector> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  late CameraDescription camera;

  Future<void> sendImagetoServer(XFile image) async {
    var stream = http.ByteStream(image.openRead());
    stream.cast();

    var length = await image.length();
    var url = Uri.parse('http://$IP_ADDRESS/face-detector');
    var request = http.MultipartRequest('POST', url);
    var multipartFile = await http.MultipartFile(
      'image',
      stream,
      length,
      filename: basename(image.path),
    );
    var pic = await http.MultipartFile.fromPath(
      'image',
      image.path,
    );
    request.files.add(multipartFile);
    request.files.add(pic);

    var response = await request.send();
    print(response.statusCode);
  }

  @override
  void initState() {
    super.initState();
    camera = cameras[1];
    _controller = CameraController(
      camera,
      ResolutionPreset.medium,
    );

    _initializeControllerFuture = _controller.initialize();
    // _controller.initialize().then((_) {
    //   if (!mounted) {
    //     return;
    //   }
    //   setState(() {});
    // }).catchError((Object e) {
    //   if (e is CameraException) {
    //     switch (e.code) {
    //       case 'CameraAccessDenied':
    //         // Handle access errors here.
    //         break;
    //       default:
    //         // Handle other errors here.
    //         break;
    //     }
    //   }
    // });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Scene Descriptor'),
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
      floatingActionButton: FloatingActionButton(
        // Provide an onPressed callback.
        onPressed: () async {
          // Take the Picture in a try / catch block. If anything goes wrong,
          // catch the error.
          try {
            // Ensure that the camera is initialized.
            await _initializeControllerFuture;

            // Attempt to take a picture and get the file `image`
            // where it was saved.
            final image = await _controller.takePicture();
            //image.saveTo('data/assets/images/scene.jpg');

            //print('IMAGE PATH: ${image.path}');

            //Send image to server
            sendImagetoServer(image);

            if (!mounted) return;

            // If the picture was taken, display it on a new screen.
            await Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => DisplayPictureScreen(
                  // Pass the automatically generated path to
                  // the DisplayPictureScreen widget.
                  imagePath: image.path,
                ),
              ),
            );
          } catch (e) {
            // If an error occurs, log the error to the console.
            print(e);
          }
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
