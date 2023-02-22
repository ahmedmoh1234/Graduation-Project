import 'package:flutter/material.dart';
import 'config.dart';
import 'package:camera/camera.dart';
import 'main.dart';

class SceneDescriptor extends StatefulWidget {
  const SceneDescriptor({super.key});

  @override
  State<SceneDescriptor> createState() => _SceneDescriptorState();
}

class _SceneDescriptorState extends State<SceneDescriptor> {
  late CameraController controller;

  @override
  void initState() {
    super.initState();
    controller = CameraController(cameras[0], ResolutionPreset.max);
    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    }).catchError((Object e) {
      if (e is CameraException) {
        switch (e.code) {
          case 'CameraAccessDenied':
            // Handle access errors here.
            break;
          default:
            // Handle other errors here.
            break;
        }
      }
    });
  }

  @override
  void dispose() {
    controller.dispose();
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
      body: CameraPreview(controller),
    );
  }
}
