import 'package:flutter/material.dart';
import 'config.dart';

class SceneDescriptor extends StatelessWidget {
  const SceneDescriptor({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Scene Descriptor'),
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
    );
  }
}
