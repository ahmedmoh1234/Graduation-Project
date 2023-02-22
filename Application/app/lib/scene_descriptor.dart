import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';
import 'dart:async';
import 'dart:io';

class SceneDescriptor extends StatefulWidget {
  const SceneDescriptor({super.key});

  @override
  State<SceneDescriptor> createState() => _SceneDescriptorState();
}

class _SceneDescriptorState extends State<SceneDescriptor> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  late CameraDescription camera;

  @override
  void initState() {
    super.initState();
    camera = cameras[0];
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
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Scene Descriptor'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      // body: Column(
      //   children: [
      //     CameraPreview(
      //       _controller,
      //     ),
      //     const SizedBox(height: 50),
      //     FloatingActionButton(
      //       // Provide an onPressed callback.
      //       onPressed: () async {
      //         print('HERE');
      //         // Take the Picture in a try / catch block. If anything goes wrong,
      //         // catch the error.
      //         try {
      //           // Ensure that the camera is initialized.
      //           await _initializeControllerFuture;

      //           // Attempt to take a picture and then get the location
      //           // where the image file is saved.
      //           final image = await _controller.takePicture();
      //         } catch (e) {
      //           // If an error occurs, log the error to the console.
      //           print(e);
      //         }
      //       },
      //       backgroundColor: Colors.grey,
      //       child: const Icon(
      //         Icons.camera_alt,
      //         size: 27,
      //         color: Colors.white,
      //       ),
      //     )
      //   ],
      // ),
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
